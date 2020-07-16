from Xray_dataset import Xray_dataset
import logging
import csv
import os
import hashlib
import abc

from pathlib import Path
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
class COVID_builder(metaclass=abc.ABCMeta):

    def __init__(self):
        self._dataset = Xray_dataset()

    @abc.abstractmethod
    def _load_dataset():
        pass

    @abc.abstractmethod
    def _sanity_check():
        pass
