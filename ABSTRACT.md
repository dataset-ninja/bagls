The **BAGLS: Automatic Glottis Segmentation Dataset** is the first large-scale, publicly available dataset of endoscopic high-speed video with frame-wise segmentation annotations. It has been collected in a collaboration of seven institutions and features a total of 59,250 frames. The BAGLS dataset aims to provide a baseline as robust as possible. Therefore, it was created in such a way that it contains diverse samples from a variety of data sources.

## Motivation

Laryngeal videoendoscopy stands as a pivotal component in both clinical evaluations of voice disorders and voice research endeavors. While high-speed videoendoscopy enables comprehensive visualization of vocal fold oscillations, the subsequent processing of these recordings often demands meticulous segmentation of the glottal area by skilled professionals. Despite the introduction of automated techniques and the suitability of the task for deep learning approaches, the absence of publicly available datasets and benchmarks poses a significant challenge. Such resources are crucial for method comparison and facilitating the training of deep learning models capable of generalization.

## Dataset acquisition

In a collaborative effort among researchers from seven institutions spanning the EU and USA, the creation of BAGLS—a substantial, multi-hospital dataset—has come to fruition. This dataset comprises 59,250 high-speed videoendoscopy frames meticulously annotated with segmentation masks. These frames stem from 640 recordings featuring both healthy individuals and those with disorders, captured using varied technical setups by diverse clinicians.

The primary objective of the BAGLS dataset is to facilitate an impartial evaluation of glottis segmentation methodologies, offering interested researchers the opportunity to train models and compare approaches. Emphasizing robustness, the dataset is meticulously curated to encompass diverse samples from a multitude of data sources, meticulously detailed in this section.

Furthermore, segmentation masks for the data were meticulously crafted by a panel of experts employing specially designed software tools. To establish a baseline and validate the benchmark data, the authors conducted training on a state-of-the-art deep learning segmentation network using the BAGLS dataset.

<img src="https://github.com/dataset-ninja/bagls/assets/120389559/52138e63-326d-4ec9-bd81-3e1eff74d56c" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;"> Workflow for creating the BAGLS dataset. Subjects with varying age, gender and health status were examined at different hospitals with differing equipment (camera, light source, endoscope type). The recorded image data is diverse in terms of resolutions and quality. Next, the glottis was segmented using manual or semi-automatic techniques and the segmentation was crosschecked. The segmented videos were split into a training and a test set. The test set features equal amounts of frames from each hospital. The authors validated BAGLS by training a deep neural network and found that it provides segmentations closely matching the manual expert segmentations.</span>

Several imaging techniques have been developed to capture the high-frequency, small-scale oscillations of the vocal folds, with laryngeal endoscopy emerging as a primary diagnostic tool for voice disorders. Among these techniques, videostroboscopy, videokymography, and high-speed videoendoscopy (HSV) are the most prevalent. Clinicians typically review videos obtained through these techniques to aid in diagnosis or to advance research efforts aimed at understanding the phonatory process.

Glottal area segmentation has long been established as a method to quantify vocal fold oscillation and extract additional insights from HSV recordings. Numerous studies have demonstrated significant correlations between various disorders and parameters computed from segmentation data, such as cepstral peak prominence. Common signals derived from glottal segmentation include the glottal area waveform (GAW), vocal fold trajectories, and phonovibrogram. Parameters derived from these signals offer a potential for increased objectivity compared to the subjective metrics still prevalent in clinical practice.

Despite the clear benefits of glottis segmentation, it remains a labor-intensive and time-consuming task that necessitates skilled expertise. And, although the binary segmentation into the classes background and glottal area might seem rather simple, in practice, there are several factors impeding completion of the task:

* Videos often feature a reduced image quality due to the technical requirements of HSV, such as a lower resolution and brief exposure time due to the high sampling rate.
* Videos are often ill-lit, affected by patient movement and artifacts such as reflections caused by mucus and thus require additional image processing.
* Parts of the glottis are often concealed due to the spatial limitations and parts of the anatomy such as the arytenoid cartilages covering others.
* Video quality and features vary noticeably depending on recording setup and subject.

Trained experts anecdotally require about 15 minutes to segment a 1,000 frames long HSV recording using specifcally developed sofware. Therefore, several previous works have explored the possibility of performing an automated segmentation of the glottal area. The BAGLS benchmark dataset will be essential in testing segmentation alhgorithms practical applicability as it:

* Provides the data necessary to train state-of-the-art deep learning methods for the task.
* Allows an objective quantification of the quality of automatic segmentation methods.
* Provides the data diversity necessary to achieve robustness in the clinical routine, where algorithms that are trained on data from one source usually do not perform well on data from another source.

Videoendoscopy is a widely employed imaging modality, and, thus, the differing recording hardware, sofware and varying clinicians introduce great variability to the data. To ensure that an automatic segmentation method actually performs well on the whole range of data, it is essential to also test it on a diverse dataset. This is one of the core motivations of this work and the provided data show a great diversity in the following respects:

* The HSV recordings were collected at seven different institutions from the USA and Europe.
* The data were collected using a variety of cameras, light sources, image resolutions, sampling rates and endoscope types.
* The data contain samples with both healthy and disordered phonation, presenting with both functional and organic dysphonia.
* The dataset is comprised of recordings from all age groups except young children and contains large amounts of samples from male and female subjects.
* The data contain pre-dominantly grayscale, but also color images (RGB).

## Data diversity


In the realm of deep learning, essential for cutting-edge segmentation algorithms, the diversity of data holds paramount importance. Trained networks often reflect underlying biases present in the data, posing significant challenges. However, in the context of glottis segmentation, this issue is somewhat mitigated since these methods aren't intended to yield diagnostic outcomes. Furthermore, any segmentation errors are relatively easy to identify.

Nevertheless, to ensure optimal performance across a wide spectrum of data and to address underrepresented scenarios, it's imperative to include diverse cases in the dataset. Accordingly, the dataset is meticulously curated to encompass various image acquisition modalities, deliberately avoiding standardization of the acquisition procedure, which naturally differs across hospitals and countries.

To achieve this diversity, the authors collaborated internationally, with each group contributing data that aligns with the diverse clinical and research settings encountered in their respective regions.

| Institution                         | # in training | # in test |
|-------------------------------------|---------------|-----------|
| Boston University                   | 10            | 10        |
| Louisiana State University          | 15            | 10        |
| New York University                 | 14            | 10        |
| Sint-Augustinus Hospital, Wilrijk  | 30            | 10        |
| University of California, Los Angeles | 20          | 10        |
| University Hospital Erlangen        | 458           | 10        |
| University Hospital of Munich (LMU) | 23           | 10        |
| Total Number of Videos             | 570           | 70        |
| Total Number of Frames             | 55750         | 3500      |

<span style="font-size: smaller; font-style: italic;">Composition of the dataset in relation to origin; the training data featured 50 or 100 frames per video depending on video length and test data 50 frames per video.</span>

As the availability of data differs between groups, it was not possible to balance the training data such that each group is represented equally. The test data, however, is split equally among groups ensuring that a method has to perform well on data from all or most of the institutions to achieve good scores on the benchmark. The authors provide individual frames of the videos that are discontinuous and randomly selected to enhance data diversity as consecutive frames typically show little variation. For each video in the test dataset, 50 frames were randomly selected leading to a total of 3500 frames from 70 videos. For the training data, either 50 or 100 frames (some videos were too short for more than 50 discontinuous frames) were randomly selected and a total of 55750 frames was selected from 570 HSV recordings. The authors provide a detailed breakdown of the provided data in terms of ***age range***, sex(***man***, ***woman***) and disorder ***status*** to emphasize the data diversity and give a detailed overview of the data. The frames and videos contained in the BAGLS dataset are provided with corresponding metadata.

<img src="https://github.com/dataset-ninja/bagls/assets/120389559/fb931ea9-2c0a-4295-b785-23aa99e2582d" alt="image" width="500">

<span style="font-size: smaller; font-style: italic;">Age distribution of subjects in the BAGLS dataset.</span>

| Disorder                           | # of videos | Disorder                          | # of videos |
|-----------------------------------|-------------|----------------------------------|-------------|
| Healthy                           | 380         | Contact granuloma                | 5           |
| Muscle tension dysphonia          | 139         | Paresis                          | 4           |
| Muscle thyroarythaenoideus atrophy| 25          | Laryngitis                       | 4           |
| Vocal insufficiency               | 18          | Papilloma                        | 1           |
| Edema                             | 14          | Leucoplacia                      | 1           |
| Insufficient glottis closure      | 14          | Carcinoma                        | 1           |
| Nodules                           | 13          | Other                            | 8           |
| Polyp                             | 9           | Unknown status                   | 50          |
| Cyst                              | 6           |                                  |             |


<span style="font-size: smaller; font-style: italic;">Overview of voice disorders represented in the BAGLS dataset, multiple disorders per video are possible.</span>

Overall, the dataset features great variability and diverse representation in terms of ***age range***, sex(***man***, ***woman***), and disorder ***status***. Furthermore, as it comprises data from seven institutions, a multitude of clinicians were involved in the acquisition of the recordings, which further broadened the diversity of the dataset.

## Technical equipment


The dataset exhibits diversity not only in terms of the clinicians and subjects involved but also in the equipment and recording setups utilized across the represented institutions. This diversity extends to a wide range of cameras, light sources, endoscopes, and imaging settings, including sampling rates and image resolutions. Sampling rates vary from 1000Hz to 10000Hz, offering a broad spectrum of temporal resolutions. Likewise, the dataset encompasses a range of image resolutions, with sizes ranging from 256×120 pixels as the smallest to 512×512 pixels as the largest. It's important to note that the aspect ratios of the images also exhibit variation, further contributing to the dataset's diversity.

| Sampling rate [Hz] | # of videos | Resolution | # of videos |
|--------------------|-------------|------------|-------------|
| 1000               | 21          | 256×120    | 15          |
| 2000               | 17          | 256×256    | 88          |
| 3000               | 30          | 288×128    | 7           |
| 4000               | 542         | 320×256    | 33          |
| 5000               | 1           | 352×208    | 30          |
| 6000               | 2           | 352×256    | 11          |
| 8000               | 26          | 512×96     | 1           |
| 10000              | 1           | 512×128    | 22          |
|                    |             | 512×256    | 431         |
|                    |             | 512×512    | 2           |

<span style="font-size: smaller; font-style: italic;">Overview of the sampling rates and resolutions of the recorded HSV data in the dataset.</span>

Five different cameras were used for the HSV recordings with three different light sources. The dataset contains recordings acquired with rigid oral endoscopes at an angle of 70° and 90° as well as flexible nasal endoscopes with two diferent diameters. Overall, 618 videos contained grayscale data and 22 featured RGB data.

| Camera                           | # of videos |
|---------------------------------|-------------|
| KayPentax HSV 9700 (Photron)   | 16          |
| KayPentax HSV 9710 (Photron)   | 495         |
| HERS 5562 Endocam Wolf         | 79          |
| Phantom v210                    | 30          |
| FASTCAM Mini AX100 540K-C-16GB | 20          |

<span style="font-size: smaller; font-style: italic;">Overview of cameras used to record the HSV.</span>

| Endoscope type   | # of videos | Light source         | # of videos |
|------------------|-------------|----------------------|-------------|
| Oral 70°         | 543         | Kay Pentax Model 7152B | 491         |
| Oral 90°         | 46          | Xenon Light          |             |
| Nasal 2.4mm      | 9           | Wolf 300W Xenon      | 79          |
| Nasal 3.5mm      | 12          | CUDA Surgical E300 Xenon | 40        |
| N/A              | 30          | N/A                  | 30          |

<span style="font-size: smaller; font-style: italic;">Overview of the utilized light sources and endoscopes to record the HSV data.</span>


## Expert annotations 

Three experts in glottis segmentation created the segmentations for the dataset. Previous studies have shown that inter- and intra-rater variability in voice research can be a concern. The BAGLS dataset aims to compensate for this by using segmentations that were crosschecked by multiple experts. The authors further validated these segmentations. Two different software tools were used to ensure a high quality of the segmentation mask, especially in the test data. The detailed segmentation procedure was as follows:

1. Videos were inspected to judge which software tool, either the Glottis Analysis Tools (GAT) software or the Pixel-Precise Annotator (PiPrA) software, was appropriate for the segmentation (both are described in the following).
2. Each video was segmented by one expert using the selected software.
3. After an additional inspection of the video, the segmentation was either refined using the PiPrA software or kept as is.
4. After segmentation of all videos, videos were randomly split into test and training sets so that each group contributed ten videos to the test data and the rest to the training data.
5. As scores rely on the test data segmentations, they were checked once by another expert and, when necessary, adjustments were made using the PiPrA software.


