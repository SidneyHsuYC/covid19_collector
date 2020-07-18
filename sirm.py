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

class Sirm_builder(xray_dataset.COVID_builder):
	def __init__(self, filepath):
		super().__init__(filepath)

	def _load_dataset(self):
		rootdir = self.filepath
		try:
			files = [i for i in os.listdir(rootdir) if i.startswith('COVID')]
			for file in files:
				if self._sanity_check(rootdir / file):
					self._dataset.images.append(str(rootdir / file))
					self._dataset.labels.append(Labels(finding='COVID-19'))
		except Exception as e:
			logger.exception(f"e")

	def _sanity_check(self, file_path):
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


if __name__ == '__main__':
	sirm_path = Path.cwd() / 'sirm_repo'

	sirm_builder = Sirm_builder(sirm_path)
	sirm_builder._load_dataset()
	sirm_dataset = sirm_builder._dataset
	sirm_dataset.print_summary()