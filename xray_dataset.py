import os
import abc
from pathlib import Path
from collections import defaultdict

class Xray_dataset():
	imgname_set = set()
	imgsum_set = set()

	def __init__(self):
		self.images = []
		self.labels = []

	def __getitem__(self, index):
		if index >= len(self.images):
			return None
		return (self.images[index], self.labels[index])

	def __len__(self):
		return len(self.images)

	def __next__(self):
		index = self.index
		self.index += 1
		if index >= len(self.images): 
			raise StopIteration 
		return (self.images[index], self.labels[index])

	def __iter__(self):
		self.index = 0
		return self

	def summary_dict(self):
		finding_dic = defaultdict(lambda: defaultdict(int))
		for label in self.labels:
			finding_dic[label.finding][label.view] += 1
		return finding_dic

	def print_summary(self):
		print(f"Total number of data: {len(self)}")
		finding_dic = self.summary_dict()
		for cat, views in finding_dic.items():
			count = 0
			print(f"{cat}: ")
			for view, qty in views.items():
				count += qty
				print(f"\t{view}, {qty}")
			print('\t---------------')
			print(f"\tSub-total: {count}")
		
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