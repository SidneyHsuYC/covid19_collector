import os
import abc
from pathlib import Path
from collections import defaultdict

class Xray_dataset():
	imgname_set = set()
	imgsum_set = set()

	def __init__(self):
		self.images = []
		self.metadata = []

	def __getitem__(self, index):
		if index >= len(self.images):
			return None
		return (self.images[index], self.metadata[index])

	def __len__(self):
		return len(self.images)

	def __next__(self):
		index = self.index
		self.index += 1
		if index >= len(self.images): 
			raise StopIteration 
		return (self.images[index], self.metadata[index])

	def __iter__(self):
		self.index = 0
		return self

	def summary_dict(self):
		finding_dic = defaultdict(int)
		for data in self.metadata:
			for find in data.finding:
				finding_dic[find] += 1
		return finding_dic

	def print_summary(self):
		print(f"Number of data in dataset: {len(self)}")
		finding_dic = self.summary_dict()
		for cat, qty in finding_dic.items():
			print(f"{cat}: {qty}")
		print('---------------')
		
class COVID_builder(metaclass=abc.ABCMeta):

	def __init__(self, filepath):
		self._dataset = Xray_dataset()
		assert(isinstance(filepath, Path))
		self.filepath = filepath

	@abc.abstractmethod
	def _load_dataset():
		pass

	@abc.abstractmethod
	def _sanity_check():
		pass