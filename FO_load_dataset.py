import glob
import fiftyone as fo
import os
import fiftyone.zoo as foz
import pandas as pd
import json
from argparse import ArgumentParser



def view_fo_args():
    parser = ArgumentParser()
    parser.add_argument('path_to_images', help='path images', type=str)
    parser.add_argument('annot_pred', help='annotations from predicton model', type=str)
    parser.add_argument('annot_orig', help='annoatations original', type=str)
    args = parser.parse_args()
    return args


class_coco = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic_light',
              'fire_hydrant',
              'stop_sign', 'parking_meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
              'zebra', 'giraffe',
              'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports_ball',
              'kite', 'baseball_bat',
              'baseball_glove', 'skateboard', 'surfboard', 'tennis_racket', 'bottle', 'wine_glass', 'cup', 'fork',
              'knife', 'spoon', 'bowl',
              'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot_dog', 'pizza', 'donut', 'cake',
              'chair', 'couch', 'potted_plant',
              'bed', 'dining_table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell_phone', 'microwave',
              'oven', 'toaster',
              'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy_bear', 'hair_drier', 'toothbrush']

class_prosegur = [None, 'cat', 'dog', 'person']

def get_all_annotations(filename):
    # get all annotations of same filename
    list_id_pred = list(set(images_pred[images_pred['file_name'] == filename]['id']))
    list_id_orig = list(set(images_orig[images_orig['file_name'] == filename]['id']))
    annot_pred = annotations_pred[annotations_pred['image_id'].isin(list_id_pred)]
    annot_orig = annotations_orig[annotations_orig['image_id'].isin(list_id_orig)]
    width = images_pred[images_pred['file_name'] == filename]['width'].values[0]
    height = images_pred[images_pred['file_name'] == filename]['height'].values[0]
    return annot_orig, annot_pred, width, height

def fill_detections_fo(annot,width,height):
    # fill list detections with detection in format fiftyone
    detections = []
    for index, raw in annot.iterrows():
        label = class_prosegur[int(raw["category_id"])]

        # Bounding box coordinates should be relative values
        # in [0, 1] in the following format:
        # [top-left-x, top-left-y, width, height]
        x1, y1, w, h = raw["bbox"]
        x2 = x1 + w
        y2 = y1 + h
        bounding_box = [x1 / width, y1 / height, (x2 - x1) / width, (y2 - y1) / height]
        detections.append(
            fo.Detection(label=label, bounding_box=bounding_box)
        )
    return detections

if __name__ == "__main__":
    args= view_fo_args()
    dataset_dir = args.path_to_images
    annot_path_orig = args.annot_orig
    annot_path_pred = args.annot_pred

    # load annotations
    with open(annot_path_pred, ) as f:
        data_pred = json.load(f)
    with open(annot_path_orig, ) as f:
        data_orig = json.load(f)
    annotations_pred = pd.DataFrame.from_dict(data_pred['annotations'])
    images_pred = pd.DataFrame.from_dict(data_pred['images'])
    annotations_orig = pd.DataFrame.from_dict(data_orig['annotations'])
    images_orig = pd.DataFrame.from_dict(data_orig['images'])

    samples = []
    for filename in set(images_pred['file_name']):
        filepath = os.path.join(dataset_dir, filename)
        # file sample with images
        sample = fo.Sample(filepath=filepath)
        # get annotations
        annot_orig, annot_pred, width, height = get_all_annotations(filename)
        # fill detections in FiftyOne format
        detections_pred = fill_detections_fo(annot_pred,width,height)
        detections_orig = fill_detections_fo(annot_orig,width,height)
        # Store detections in a field name of your choice
        sample["ground_truth"] = fo.Detections(detections=detections_orig)
        sample['predictions_swin'] = fo.Detections(detections=detections_pred)

        samples.append(sample)

    # Create dataset
    coco_dataset = fo.Dataset("my-detection-dataset")
    coco_dataset.add_samples(samples)

    session = fo.launch_app(coco_dataset)
    session.wait()
