import fiftyone as fo
import os
import fiftyone.zoo as foz
from argparse import ArgumentParser

"""
[12:16 PM] Daniel María García-ocaña Hernández
Tarea 4
Utilidad para descargar los datasets de interés de OpenImages usando fiftyone.
Pruebas:
Descargar un solo dataset (cat)Descargar más de un dataset (cat y dog)
Estas dos pruebas pueden hacerse en local. Si funcionan, quedará validada la herramienta y se podrán descargar los 3 datasets desde una máquina Azure. 
Entrada: la clase o la lista de clases que queremos descargar, el path donde queremos guardar el/los dataset/s descargado/s y el prefijo que queremos ponerle a cada dataset (en este caso, “open-images-v6”)Salida: los datasets descargados, guardados en el path especificado como argumento de entrada. El nombre de cada dataset debe ser “open-images-v6_<clase>”.

[12:16 PM] Daniel María García-ocaña Hernández
Nota 1: Una vez descargados person, cat y dog de nuevo, comprobar si dentro de las carpetas de imágenes viene la carpeta labels/ 
que tenemos en los datasets almacenados en Azure.  Si está la carpeta labels/, mirar en la web OpenImages a ver si mencionan algo sobre esta carpeta y el formato que tiene.
Nota 2: Una vez descargados person, cat y dog de nuevo, comprobar que las imágenes para las que tenemos anotaciones son 
las mismas que están en las carpetas de imágenes (no como ahora, que hay anotaciones de imágenes que no tenemos descargadas).

"""


def fo_args():
    parser = ArgumentParser()
    parser.add_argument('output_dir', help='path to store the dataset', type=str)
    parser.add_argument('prefixe', help='prefixe of dataset', type=str)
    parser.add_argument('split', help='split', type=str)
    parser.add_argument('--classes', nargs="+", help="list of class we want to keep")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = fo_args()
    # configure path to store dataset
    fo.config.dataset_zoo_dir =args.output_dir
    # download dataset
    if args.classes:
        dataset = foz.load_zoo_dataset(args.prefixe, classes=args.classes, split=args.split, label_types = "detections")
    else:
        dataset = foz.load_zoo_dataset(args.prefixe, split=args.split, label_types = "detections")



