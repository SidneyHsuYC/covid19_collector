import unittest
from pathlib import Path
import os
import xray_dataset
import ieee8032, farjan, sirm
from ieee8032_verifer import ieee8032_pdreader

dataset_size = {
    'ieee8032': 637,
    'farjan': 48,
    'sirm': 63
}

class TestDatasetSize(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        root_dir = Path.cwd()

        ieee0832_path = Path.cwd() / 'ieee8032_repo'
        ieee_builder = ieee8032.IEEE8023_builder('metadata.csv', ieee0832_path)
        ieee_builder._load_dataset()
        cls.ieee_dataset = ieee_builder._dataset

        farjan_path = root_dir / 'farjan_repo' 
        farjan_builder = farjan.Farjan_builder(farjan_path)
        farjan_builder._load_dataset()
        cls.farjan_dataset = farjan_builder._dataset

        sirm_path = root_dir / 'sirm_repo'
        sirm_builder = sirm.Sirm_builder(sirm_path)
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

        # for data in self.ieee_dataset:
        #     next(ieee_iter)
        #     print(ieee_iter)
        #     ieee_count += 1
        for data in self.farjan_dataset:
            farjan_count += 1
        for data in self.sirm_dataset:
            sirm_count += 1
        self.assertEqual(ieee_count, dataset_size.get('ieee8032')) 
        self.assertEqual(farjan_count, dataset_size.get('farjan')) 
        self.assertEqual(sirm_count, dataset_size.get('sirm')) 

    def test_ieee8032(self):
        pd_finding = ieee8032_pdreader()
        self.assertEqual(pd_finding, self.ieee_dataset.summary_dict().get('COVID-19'))

if __name__ == '__main__':
    unittest.main()