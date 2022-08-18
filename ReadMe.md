
# FiftyOne utility

This project allows you to download any dataset from fiftyone , with advanced option like choose the category or the id of images. And then vizualize it into fiftyone , you can also compare the results of two models.

## Environments installation

```
	conda create --name FO python==3.8
	conda activate FO
	pip install fiftyone
```		

## Get started

1. To download a dataset from fiftyone , run download_dataset.py with first argument the directory where you to downloaded it, second argument is the prefixe ( "coco-2017" "open-images-v6") , third is the split and fourth the classes you want to filter
For example if you want to downloaded 100 images of open-images-v6 train split with only category Cat :
```
python download_dataset.py dataset open-images-v6 train --classes Cat
```		
2. To analyze dataset downloaded from fiftyone with the dataset in the azure machine use analyze_FO, by just giving in argument path to both dataset images  and path to file to store result

```
python analyze_FO.py path_dataset_fo path_dataset_azure output_file
```		

 3. To vizualize your predictions from your model in fiftyone and compare it with the original result, use FO_load_dataset.py by giving in argument path were the images are , and path of both annotations from predictions and original in COCO FORMAT

 ```
 python FO_load_dataset.py path_to_images path_annotations_pred path_annotations_orig
 ```		
