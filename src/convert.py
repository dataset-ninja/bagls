import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_ext, get_file_name
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    train_path = "/home/alex/DATASETS/TODO/Automatic Glottis Segmentation/training"
    test_path = "/home/alex/DATASETS/TODO/Automatic Glottis Segmentation/test"
    ds_name = "ds"
    images_ext = ".png"
    masks_ext = "_seg.png"
    ann_ext = ".meta"
    batch_size = 30

    ds_name_to_pathes = {"train": train_path, "test": test_path}

    def create_ann(image_path):
        labels = []
        tags = []

        tags_file_path = image_path.replace(images_ext, ann_ext)
        if file_exists(tags_file_path):
            tags_data = load_json_file(tags_file_path)
            video_id_value = tags_data.get("Video Id")
            if video_id_value is not None:
                video_id = sly.Tag(video_id_meta, value=int(video_id_value))
                tags.append(video_id)

            # color_value = tags_data.get("Color")
            # if color_value == "true" or color_value == "True":
            #     color = sly.Tag(color_meta)
            #     tags.append(color)

            age_value = tags_data.get("Age range (yrs)")
            if len(age_value) > 0:
                age = sly.Tag(age_meta, value=age_value)
                tags.append(age)

            sex_value = tags_data.get("Subject sex")
            if len(sex_value) > 0:
                sex_meta = value_to_sex_meta[sex_value]
                sex = sly.Tag(sex_meta)
                tags.append(sex)

            status_value = tags_data.get("Subject disorder status")
            if len(status_value) > 0:
                status = sly.Tag(status_meta, value=status_value)
                tags.append(status)

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        mask_path = image_path.replace(images_ext, masks_ext)
        if file_exists(mask_path):
            ann_np = sly.imaging.image.read(mask_path)[:, :, 2]
            obj_mask = ann_np == 255
            if len(np.unique(obj_mask)) > 1:
                curr_bitmap = sly.Bitmap(obj_mask)
                curr_label = sly.Label(curr_bitmap, obj_class)
                labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    obj_class = sly.ObjClass("glottis", sly.Bitmap)

    video_id_meta = sly.TagMeta("video id", sly.TagValueType.ANY_NUMBER)
    # color_meta = sly.TagMeta("color", sly.TagValueType.NONE)
    age_meta = sly.TagMeta("age range", sly.TagValueType.ANY_STRING)
    man_meta = sly.TagMeta("man", sly.TagValueType.NONE)
    woman_meta = sly.TagMeta("woman", sly.TagValueType.NONE)
    status_meta = sly.TagMeta("status", sly.TagValueType.ANY_STRING)

    value_to_sex_meta = {"M": man_meta, "m": man_meta, "w": woman_meta, "W": woman_meta}

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class],
        tag_metas=[video_id_meta, age_meta, man_meta, woman_meta, status_meta],
    )
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, data_path in ds_name_to_pathes.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_names = [
            im_name
            for im_name in os.listdir(data_path)
            if get_file_ext(im_name) == images_ext and len(im_name.split("_")) == 1
        ]

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(data_path, image_path) for image_path in img_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]

            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))

    return project
