import logging
import csv
import os
import hashlib
from pathlib import Path
from collections import namedtuple
import xray_dataset, ourlogger

logger = logging.getLogger(__name__)

fields = ('patientid', 'offset', 'sex', 'age', 'finding', 'view', 'date')
Labels = namedtuple('Labels', fields, defaults=(None,) * len(fields))

class Farjan_builder(xray_dataset.COVID_builder):
	def __init__(self, filepath):
		super().__init__(filepath)
	
	def _load_dataset(self):
		rootdir = self.filepath / 'covid_chestXray_dataset/covid_19 dataset'
		try:
			dirs = os.listdir(rootdir)
			label_from_folder = ['COVID-19' if i == 'covid19' else i for i in dirs]

			for index, sub_dir in enumerate(dirs):
				sub_path = rootdir / sub_dir
				for file in os.listdir(sub_path):
					if self._sanity_check(sub_path / file):
						self._dataset.images.append(str(sub_path / file))
						self._dataset.labels.append(Labels(finding=label_from_folder[index]))
		except Exception as e:
			raise e

	def _sanity_check(self, file_path):
		if file_path.name in self._dataset.imgname_set:
			logger.info(f"Dataset Farjan, {file_path.name} has duplicate name in dataset.")
			return None
		# Check imagine checksum existed in database
		checksum = 0
		try:
			with open(file_path, 'rb') as f:
				image_file = f.read()
				checksum = hashlib.md5(image_file).hexdigest()
		except FileNotFoundError:
			logger.info(f"Dataset Farjan, {file_path} does not existed.")
			return None
		except Exception as e:
			logger.exception(f"{e}")
		
		if (not checksum) or (checksum in self._dataset.imgsum_set):
			logger.info(f"Dataset Farjan, {file_path} has duplicate checksum in dataset.")
			return None

		# Update set status
		self._dataset.imgname_set.add(file_path.name)
		self._dataset.imgsum_set.add(checksum)
		return True


if __name__ == '__main__':

	farjan_path = Path.cwd() / 'farjan_repo'

	farjan_builder = Farjan_builder(farjan_path)
	farjan_builder._load_dataset()
	farjan_dataset = farjan_builder._dataset
	farjan_dataset.print_summary()
