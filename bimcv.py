import logging
import csv
import os, re
import hashlib
import glob
from pathlib import Path
from collections import namedtuple

import xray_dataset

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
		metadata_path = self.filepath / 'bimcv_covid19_posi_head_iter1' / 'derivatives' / 'labels'
		partition_dict = self.__load_participant()
		try:
			metafilepath = metadata_path / self.metadata

			with open(metafilepath, encoding="utf8", newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
				self.header = next(spamreader)
				self.__load_index(self.header)
				count = 0
				for row in spamreader:
					patientid = row[self.patientid_index]
					reportid = row[self.reportid_index]
					image_path = glob.glob(str(Path(self.filepath) / '*' / patientid / reportid / 'mod-rx' / '*.png'))

					# Only select one piciture and do sanity check
					if image_path and self._sanity_check(Path(image_path[0])):
						self._dataset.images.append(image_path[0])
						# Transform finding string to list object
						finding = [label.strip("'").strip() for label in row[self.labels_index][1:-1].split('\t ') if label.strip("'")]
						# Replace "COVID 19" to COVID-19 
						finding = ['COVID-19' if i=='COVID 19' else i for i in finding]
						metadata = partition_dict.get(patientid)
						if metadata:
							self._dataset.images.append(image_path)
							self._dataset.metadata.append(Labels(
								patientid=patientid,
								sex=metadata.gender,
								age=partition_dict.get('age'),
								modality=metadata.modality_dicom,
								finding=finding
							))

		except Exception as e:
			logger.warning(e)
	
	def _sanity_check(self, file_path):
		logger = self.logger
		if file_path.name in self._dataset.imgname_set:
			logger.info(f"Dataset BIMCV, {file_path.name} has duplicate name in dataset.")
			return None
		# Check imagine checksum existed in database
		checksum = 0
		try:
			with open(file_path, 'rb') as f:
				image_file = f.read()
				checksum = hashlib.md5(image_file).hexdigest()
		except FileNotFoundError:
			logger.info(f"Dataset BIMCV, {file_path} does not existed.")
			return None
		except Exception as e:
			logger.exception(f"{e}")
		
		if (not checksum) or (checksum in self._dataset.imgsum_set):
			logger.info(f"Dataset BIMCV, {file_path} has duplicate checksum in dataset.")
			return None

		# Update set status
		self._dataset.imgname_set.add(file_path.name)
		self._dataset.imgsum_set.add(checksum)
		return True

	def __load_participant(self):
		try:
			participants_dict = {}
			participants_path = self.filepath / 'bimcv_covid19_posi_head_iter1' / 'participants.tsv'
			# try:
			with open(participants_path, encoding="utf8", newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
				self.header_p = next(spamreader)
				self.__load_index_p(self.header_p)
				for row in spamreader:
					modality = re.findall(r"\'(\w+)\'", row[self.modality_index])
					age = re.search(r"(\d+)", row[self.age_index])
					age = int(age[0]) if age else None
					participants_dict[row[self.participant_index]] = Part_label(modality, age, row[self.gender_index])
		except Exception as e:
			logging.warning(e)
		
		return participants_dict

	def __load_index(self, header):
		self.patientid_index = self.header.index('PatientID')
		self.reportid_index = self.header.index('ReportID')
		self.labels_index = self.header.index('Labels')
	
	def __load_index_p(self, header_p):
		self.participant_index = self.header_p.index('participant')
		self.modality_index = self.header_p.index('modality_dicom')
		self.age_index = self.header_p.index('age')
		self.gender_index = self.header_p.index('gender')	

if __name__ == '__main__':
	bimcv_path = Path.cwd() / 'bimcv_repo'
	bimcv_builder = BIMCV_builder('labels_covid19_posi.tsv', bimcv_path)
	bimcv_builder._load_dataset()
	bimcv_dataset = bimcv_builder._dataset
	bimcv_dataset.print_summary()
