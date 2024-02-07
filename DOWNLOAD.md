Dataset **BAGLS: Images** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/w/M/P1/yNj7mNBKdLipLYfsWn6QIdhz6HH4gpobpmS9YzG4VDC1o2VG9YoMJtVPdNfFHEOUWlBov1RA9rJFsWjII7GQc5XOe8k9TDR100L36rAozqVCnG9keXVbjLUNsN3G.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='BAGLS: Images', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/gomezp/benchmark-for-automatic-glottis-segmentation/download?datasetVersionNumber=2).