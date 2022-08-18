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
    parser.add_argument('FO_dataset', help='images in fo dataset', type=str)
    parser.add_argument('azure_dataset', help='images in azure machine to compare with FiftyOne', type=str)
    parser.add_argument("output_file", help="output file to store the images in common ")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
   

    args= fo_args()
    # list images downloaded with fiftyone
    list_images_fo = os.listdir(args.FO_dataset)
    list_images_fo.sort()
    # list images inside azure machine
    list_images_azure = os.listdir(args.azure_dataset)
    list_images_azure.sort()

    # find common images in both list
    common_images = set(list_images_azure).intersection(set(list_images_fo))
    with open(args.output_file,'w') as f:
        f.write(f"len images in azure : {len(list_images_azure)} \n")
        f.write(f"len images in FiftyOne : {len(list_images_fo)} \n")
        f.write(f"len of intersection {len(common_images)} \n")
        f.write(str(common_images))


