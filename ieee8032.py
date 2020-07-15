import logging
import csv
import os
import hashlib
from pathlib import Path
from collections import namedtuple

import xray_dataset, ourlogger
logger = logging.getLogger(__name__)
logger = ourlogger.setuplogger(logger)

fields = ('patientid', 'offset', 'sex', 'age', 'finding', 'view', 'date')
Labels = namedtuple('Labels', fields, defaults=(None,) * len(fields))

class IEEE8023_builder(xray_dataset.COVID_builder):
	def __init__(self, metadata, filepath):
		super().__init__(filepath)
		self.metadata = metadata

	def _load_dataset(self):
		# logger = self.logger
		rootdir = self.filepath / 'covid-chestxray-dataset'
		try:
			metafilepath = rootdir / self.metadata

			with open(metafilepath, newline='') as csvfile:
				# print('loading')
				spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
				self.header = next(spamreader)
				self.__load_index(self.header)

				for index, row in enumerate(spamreader):
					finding = row[self.finding_index]
					# Check if multiple values have COVID-19, otherwise skip
					if ',' in finding:  # Check multiple value in finding colum
						cat_list = [cat.strip() for cat in finding.split(',')]
						if 'COVID-19' in cat_list:
							finding_val = 'COVID-19'
						else:
							continue
					else:       # Check single value
						if row[self.finding_index] == 'todo':
							continue
						if row[self.finding_index] == 'No Finding':
							finding_val = 'normal'
						elif row[self.finding_index] == 'COVID-19':
							finding_val = 'COVID-19'
						else:
							finding_val = 'others'

					if self._sanity_check(index, row):
						self._dataset.images.append(os.path.join(rootdir, row[self.folder_index], row[self.filename_index]))
						self._dataset.labels.append(Labels._make([row[self.patientid_index],
																row[self.offset_index],
																row[self.sex_index],
																row[self.age_index],
																finding_val,
																row[self.view_index],
																row[self.date_index]
																]))
		except Exception as e:
			logger.warning(e)

	def _sanity_check(self, index, row):
		# logger = self.logger
		rootdir = self.filepath / 'covid-chestxray-dataset'

		# Check file name existed in dataset
		if row[self.filename_index] in self._dataset.imgname_set:
			logger.info(f"Dataset IEEE8023, image of row #{index} has duplicate name in dataset.")
			return None
		
		# Check imagine checksum existed in database
		checksum = 0
		try:
			filename = f"{row[self.folder_index ]}/{row[self.filename_index]}"
			#print(f" {filename}")
			with open(rootdir/filename, 'rb') as f:
				image_file = f.read()
				checksum = hashlib.md5(image_file).hexdigest()
		except FileNotFoundError:
			logger.info(f"Dataset IEEE8023, image of row #{index} does not existed.")
			return None
		except Exception as e:
			logger.warning(f"{e}")

		if (not checksum) or (checksum in self._dataset.imgsum_set):
			logger.info(f"Dataset IEEE8023, image of row #{index} has duplicate checksum in dataset.")
			return None

		# Update set status
		self._dataset.imgname_set.add(row[self.filename_index])
		self._dataset.imgsum_set.add(checksum)
		return True

	def __load_index(self, header):
		self.patientid_index = self.header.index('patientid')
		self.offset_index = self.header.index('offset')
		self.sex_index = self.header.index('sex')
		self.age_index = self.header.index('age')
		self.finding_index = self.header.index('finding')
		self.view_index = self.header.index('view')
		self.date_index = self.header.index('date')
		self.folder_index = self.header.index('folder')
		self.filename_index = self.header.index('filename')


if __name__ == '__main__':
	ieee0832_path = Path.cwd() / 'ieee8032_repo'
	ieee_builder = IEEE8023_builder('metadata.csv', ieee0832_path)

	ieee_builder._load_dataset()
	ieee_dataset = ieee_builder._dataset
	ieee_dataset.print_summary()
