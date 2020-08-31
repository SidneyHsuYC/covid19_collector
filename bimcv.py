import logging
import csv
import os, re
import hashlib
import h5py
from pathlib import Path
from collections import namedtuple

import xray_dataset

# Handle "_csv.Error: field larger than field limit (131072)"
import sys
csv.field_size_limit(sys.maxsize)

fields = ('patientid', 'offset', 'sex', 'age', 'modality', 'finding', 'view', 'date')
Labels = namedtuple('Labels', fields, defaults=(None,) * len(fields))

Part_label = namedtuple('Part_label', ['modality_dicom', 'age', 'gender'])

class BIMCV_builder(xray_dataset.COVID_builder):
	def __init__(self, metadata, filepath, logger=None):
		super().__init__(filepath)
		self.metadata = metadata
		self.logger = logger or logging.getLogger(__name__)

	def _load_dataset(self):
		logger = self.logger
		metadata_path = self.filepath / 'bimcv_metadata.csv'
		hdf5_path = self.filepath / 'bimcv_metadata.hdf5'
		# partition_dict = self.__load_participant()

		with open(metadata_path, encoding="utf8", newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"', skipinitialspace=True)
			# 47 fields
			self.header = next(spamreader)
			self.__load_index(self.header)
			# for i in spamreader:
			count = 0
			with h5py.File(str(hdf5_path), "r") as h5:

				for index, row in enumerate(spamreader):
					patientid = row[self.patientid_index]
					sex = row[self.gender_index]
					age =  int(row[self.age_index][1:-1]) if row[self.age_index] else None
					# age = row[self.age_index]
					modality = row[self.modality_index]
					labels = row[self.labels_index]
					view = row[self.view_index]
					h5_image_index = int(row[self.h5_index])
					labels = [label.strip() for label in row[self.labels_index].split(',') if label.strip()]
					images = h5['images'][h5_image_index]
					# print(index, ' :: ','patientid', ' :: ',patientid, type(patientid))
					# print(index, ' :: ', 'sex', ' :: ', sex, type(sex))
					# print(index, ' :: ', 'age', ' :: ', age, type(age))
					# print(index, ' :: ', 'modality', ' :: ', modality, type(modality))
					# print(index, ' :: ', 'labels', ' :: ', labels, type(labels))
					# print(index, ' :: ', 'h5_image_index', ' :: ', h5_image_index, type(h5_image_index))
					# print(index, ' :: ', 'view', ' :: ', view, type(view))

					if images.any() and self._sanity_check(h5_image_index, images):

						# Replace "COVID 19" to COVID-19 
						finding = ['COVID-19' if i=='COVID 19' else i for i in labels]

						self._dataset.images.append(hdf5_path / str(h5_image_index))
						self._dataset.metadata.append(Labels(
							patientid=patientid,
							sex=sex,
							age=age,
							modality=modality,
							finding=finding,
							view=view
						))

		# except Exception as e:
		# 	logger.warning(e)
	
	def _sanity_check(self, index, images):
		logger = self.logger
		# Check imagine checksum existed in database
		checksum = hashlib.md5(images).hexdigest()
		if (not checksum) or (checksum in self._dataset.imgsum_set):
			logger.info(f"Dataset BIMCV, images#{index} has duplicate checksum in dataset.")
			return None

		# Update set status
		self._dataset.imgsum_set.add(checksum)
		return True

	# def __load_participant(self):
	# 	try:
	# 		participants_dict = {}
	# 		participants_path = self.filepath / 'bimcv_covid19_posi_head_iter1' / 'participants.tsv'
	# 		# try:
	# 		with open(participants_path, encoding="utf8", newline='') as csvfile:
	# 			spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
	# 			self.header_p = next(spamreader)
	# 			self.__load_index_p(self.header_p)
	# 			for row in spamreader:
	# 				modality = re.findall(r"\'(\w+)\'", row[self.modality_index])
	# 				age = re.search(r"(\d+)", row[self.age_index])
	# 				age = int(age[0]) if age else None
	# 				participants_dict[row[self.participant_index]] = Part_label(modality, age, row[self.gender_index])
	# 	except Exception as e:
	# 		logging.warning(e)
		
	# 	return participants_dict
	
	def __load_index(self, header):
		self.patientid_index = self.header.index('Patient ID')
		self.gender_index = self.header.index("Patient's Sex")
		self.age_index = self.header.index("Patient's Age")
		self.modality_index = self.header.index('Modality')
		self.labels_index = self.header.index('Labels')
		self.view_index = self.header.index('Position_DL')
		self.h5_index = self.header.index("h5_idx")
		

if __name__ == '__main__':
	bimcv_path = Path.cwd() / 'bimcv_repo'
	bimcv_builder = BIMCV_builder('labels_covid19_posi.tsv', bimcv_path)
	bimcv_builder._load_dataset()
	bimcv_dataset = bimcv_builder._dataset
	bimcv_dataset.print_summary()
