import os

from pathlib import Path
# from readme_module import add_key, get_readme_dict
import xray_dataset
import ieee8032, farjan, sirm
import ourlogger

kIEEE8032=True
kFarjan=False
kSirm=True

# class Director:
#     def __init__(self):
#         self._builder = None

#     def construct(self, builder):
#         self._builder = builder
#         self._builder._load_dataset()
		# self._builder._sanity_check(index, row)


def main():
	if kIEEE8032:
		ieee0832_path = Path.cwd() / 'ieee8032_repo'
		ieee_builder = ieee8032.IEEE8023_builder('metadata.csv', ieee0832_path)

		ieee_builder._load_dataset()
		ieee_dataset = ieee_builder._dataset
		print(f"ieee dataset images quantity: {len(ieee_dataset)}")

	if kFarjan:
		farjan_path = Path.cwd() / 'farjan_repo' 

		farjan_builder = farjan.Farjan_builder(farjan_path)
		farjan_builder._load_dataset()
		farjan_dataset = farjan_builder._dataset
		print(f"farjan dataset images quantity: {len(farjan_dataset)}")

	if kSirm:
		sirm_path = Path.cwd() / 'sirm_repo' 

		sirm_builder = sirm.Sirm_builder(sirm_path)
		sirm_builder._load_dataset()
		sirm_dataset = sirm_builder._dataset
		print(f"sirm_path dataset images quantity: {len(sirm_dataset)}")

if __name__ == '__main__':
	main()

