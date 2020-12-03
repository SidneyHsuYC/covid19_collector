import unittest
import logging
from pathlib import Path
import os
from Classes.IEEE8023_builder import IEEE8023_builder
from Classes.Farjan_builder import Farjan_builder
from Classes.Sirm_builder import Sirm_builder
from Classes.xray_dataset import Xray_dataset
from Classes.COVID_builder import COVID_builder

dataset_size = {
    'ieee8032': 637,
    'farjan': 48,
    'sirm': 63
}

class TestDatasetSize(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.WARNING)
        root_dir = Path.cwd()
        print(root_dir)
        ieee0832_path = root_dir / 'ieee8032_repo' / 'covid-chestxray-dataset'
        os.chdir(ieee0832_path)
        ieee_builder = IEEE8023_builder('metadata.csv', logger)
        ieee_builder._load_dataset()
        cls.ieee_dataset = ieee_builder._dataset
        os.chdir(ieee0832_path.parent)

        farjan_path = root_dir / 'farjan_repo' 
        os.chdir(farjan_path)
        farjan_builder = Farjan_builder(logger)
        farjan_builder._load_dataset()
        cls.farjan_dataset = farjan_builder._dataset

        sirm_path = root_dir / 'sirm_repo'
        os.chdir(sirm_path)
        sirm_builder = Sirm_builder(logger)
        sirm_builder._load_dataset()
        cls.sirm_dataset = sirm_builder._dataset

    def test_dataset_size(self):
        print("Asserting test dataset size...")
        self.assertEqual(len(self.ieee_dataset), dataset_size.get('ieee8032'))
        self.assertEqual(len(self.farjan_dataset), dataset_size.get('farjan'))
        self.assertEqual(len(self.sirm_dataset), dataset_size.get('sirm'))

    def test_dataset_iter(self):
        print("Asserting test dataset iterator size...")
        ieee_count = 0
        farjan_count = 0
        sirm_count = 0
        ieee_iter = iter(self.ieee_dataset)
        for data in self.ieee_dataset:
            # next(ieee_iter)
            ieee_count += 1
        for data in self.farjan_dataset:
            farjan_count += 1
        for data in self.sirm_dataset:
            sirm_count += 1
        self.assertEqual(ieee_count, dataset_size.get('ieee8032')) 
        self.assertEqual(farjan_count, dataset_size.get('farjan')) 
        self.assertEqual(sirm_count, dataset_size.get('sirm')) 

if __name__ == '__main__':
    unittest.main()