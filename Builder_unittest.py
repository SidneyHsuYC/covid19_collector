import unittest
from pathlib import Path
import os
from dataset_builder import Xray_dataset, COVID_builder, IEEE8023_builder, Farjan_builder, Sirm_builder

dataset_size = {
    'ieee8032': 647,
    'farjan': 48,
    'sirm': 63
}

class TestDatasetSize(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        root_dir = Path.cwd()
        print(root_dir)
        ieee0832_path = root_dir / 'ieee8032_repo'
        os.chdir(ieee0832_path)
        ieee_builder = IEEE8023_builder('metadata.csv')
        ieee_builder._load_dataset()
        cls.ieee_dataset = ieee_builder._dataset

        farjan_path = root_dir / 'farjan_repo' 
        os.chdir(farjan_path)
        farjan_builder = Farjan_builder()
        farjan_builder._load_dataset()
        cls.farjan_dataset = farjan_builder._dataset

        sirm_path = root_dir / 'sirm_repo'
        os.chdir(sirm_path)
        sirm_builder = Sirm_builder()
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
        for data in self.ieee_dataset:
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