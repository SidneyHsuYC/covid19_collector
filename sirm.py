import logging
import csv
import os
import hashlib
from pathlib import Path

import xray_dataset, ourlogger

class Sirm_builder(xray_dataset.COVID_builder):
	def __init__(self, filepath, logger=None):
		super().__init__(filepath, logger)

	def _load_dataset(self):
		rootdir = self.filepath
		try:
			files = [i for i in os.listdir(rootdir) if i.startswith('COVID')]
			for file in files:
				if self._sanity_check(rootdir / file):
					self._dataset.images.append(str(rootdir / file))
					self._dataset.labels.append('COVID-19')
					self._dataset.views.append('')
		except Exception as e:
			self.logger.exception(f"e")

	def _sanity_check(self, file_path):
		logger = self.logger
		if file_path.name in self._dataset.imgname_set:
			logger.info(f"Dataset Sirm, {file_path.name} has duplicate name in dataset.")
			return None
		# Check imagine checksum existed in database
		checksum = 0
		try:
			with open(file_path, 'rb') as f:
				image_file = f.read()
				checksum = hashlib.md5(image_file).hexdigest()
		except FileNotFoundError:
			logger.info(f"Dataset Sirm, {file_path} does not existed.")
			return None
		except Exception as e:
			logger.exception(f"{e}")
		
		if (not checksum) or (checksum in self._dataset.imgsum_set):
			logger.info(f"Dataset Sirm, {file_path} has duplicate checksum in dataset.")
			return None

		# Update set status
		self._dataset.imgname_set.add(file_path.name)
		self._dataset.imgsum_set.add(checksum)
		return True

		sirm_path = Path.cwd() / 'sirm_repo' 
		os.chdir(sirm_path)
		sirm_builder = sirm.Sirm_builder(logger)
		sirm_builder._load_dataset()
		sirm_dataset = sirm_builder._dataset
		print(f"sirm_path dataset images quantity: {len(sirm_dataset)}")
		print(len(sirm_dataset))
		for i in sirm_dataset:
			print(i)

if __name__ == '__main__':
	logger = ourlogger.setuplogger('imageloader.log')

	sirm_path = Path.cwd() / 'sirm_repo'

	sirm_builder = Sirm_builder(sirm_path, logger)
	sirm_builder._load_dataset()
	sirm_dataset = sirm_builder._dataset
	print(f"sirm_path dataset images quantity: {len(sirm_dataset)}")
	print(len(sirm_dataset))
	for i in sirm_dataset:
		print(i)
