import logging
import os
import hashlib
import abc

from pathlib import Path
from Classes.IEEE8023_builder import IEEE8023_builder
from Classes.Farjan_builder import Farjan_builder
from Classes.Sirm_builder import Sirm_builder

# from readme_module import add_key, get_readme_dict

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('imageloader.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# class Director:
#     def __init__(self):
#         self._builder = None

#     def construct(self, builder):
#         self._builder = builder
#         self._builder._load_dataset()
        # self._builder._sanity_check(index, row)

def main():

    ieee0832_path = Path.cwd() / 'ieee8032_repo' / 'covid-chestxray-dataset'
    os.chdir(ieee0832_path)
    ieee_builder = IEEE8023_builder('metadata.csv')

    ieee_builder._load_dataset()
    ieee_dataset = ieee_builder._dataset
    print(f"ieee dataset images quantity: {len(ieee_dataset)}")

    farjan_path = Path.cwd().parent / 'farjan_repo' 
    os.chdir(farjan_path)
    farjan_builder = Farjan_builder()
    farjan_builder._load_dataset()
    farjan_dataset = farjan_builder._dataset
    print(f"farjan dataset images quantity: {len(farjan_dataset)}")

    sirm_path = Path.cwd().parent / 'sirm_repo' 
    os.chdir(sirm_path)
    sirm_builder = Sirm_builder(logger)
    sirm_builder._load_dataset()
    sirm_dataset = sirm_builder._dataset
    print(f"sirm_path dataset images quantity: {len(sirm_dataset)}")
    print(len(sirm_dataset))

if __name__ == '__main__':
    main()

