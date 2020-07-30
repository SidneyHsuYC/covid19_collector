import argparse
import requests
import tarfile
import os
from url_dict import *
from tqdm import tqdm
from pathlib import Path

parser = argparse.ArgumentParser(usage="python data_downloader.py [-h] -d start:end",
	description='Pass in which data package whats to download for BIMCV+ dataset.')
parser.add_argument('-m', '--meta', dest="header", action='store_true', help='Download Metadata.')
parser.add_argument("-d", "--data", 
					dest="dataset",
					help='''Download data folder(s) (index from 1 to 34):     
							-d [index] (for single folder), or
							-d [start]:[end] (for multiple folders)" 
							''')

def arg_check(args):

	index_list = None
	# Set default value if no input
	if (not args.header) and (not args.dataset):
		print(f"Using default value: Download header folder and Dataset 1.")
		args.header = True
		index_list = [1]

		if os.path.exists('./bimcv_covid19_posi_head_iter1'):
			print(f"--> Header folder already exists.")
			args.header = False
		if os.path.exists('./bimcv_covid19_posi_subjects_1'):
			print(f"--> Dataset bimcv_covid19_posi_subjects_1 already exists.")
			index_list = None
		
	if args.dataset:
		dataset_index = args.dataset
		# Check multiple folders
		if ':' in dataset_index:
			index_list = dataset_index.split(':')
		# Only one folder	
		else:
			index_list = [dataset_index]
		# Sanity check on input	
		for i, num in enumerate(index_list):
			try:
				num = int(num)
				if num > 34:
					print("Folder number cannot be greater than 34.")
					exit(1)
				index_list[i] = int(num)
			except:
				print("Invalid number format.")
				exit(1)
		if len(index_list) > 2:
			print("Invalid format: more than two numbers.")
			exit(1)
		elif len(index_list) == 2:
			if index_list[0] >= index_list[1]:
				print("Start index must be smaller than end index.")
				exit(1)

	return args.header, index_list

def download(filename):
	url = url_dict.get(filename)
	response = requests.get(url, stream=True)
	total_size_in_bytes= int(response.headers.get('content-length', 0))
	block_size = 1024 #1 Kibibyte

	if response.status_code == 200:
		print(f"Downloading {filename}")
		progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
		with open(filename, 'wb') as file:
			for data in response.iter_content(block_size):
				progress_bar.update(len(data))
				file.write(data)
	progress_bar.close()

	if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
		print("ERROR, something went wrong")
		exit(1)

def extract(filename):
	print(f"Extrating {filename}... ", end='', flush=True)
	tar = tarfile.open(f"{filename}")
	tar.extractall(f"{Path(filename).stem}")
	tar.close()
	print("Done")

def remove(filename):
	print(f"Removing {filename}... ", end='', flush=True)
	os.remove(filename)
	print("Done")

if __name__ == '__main__':
	args = parser.parse_args()
	header, index_list = arg_check(args)

	if header:
		download('bimcv_covid19_posi_head_iter1.tgz')
		extract('bimcv_covid19_posi_head_iter1.tgz')
		remove('bimcv_covid19_posi_head_iter1.tgz')
	
	if index_list:
		for index in index_list:
			download(f"bimcv_covid19_posi_subjects_{index}.tgz")
			extract(f"bimcv_covid19_posi_subjects_{index}.tgz")
			remove(f"bimcv_covid19_posi_subjects_{index}.tgz")