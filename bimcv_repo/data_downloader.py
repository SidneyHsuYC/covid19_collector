import argparse
import requests
from url_dict import *
from tqdm import tqdm

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
	if (not args.header) and (not args.dataset):
		parser.print_help()
		exit(0)
		# Downloading header folder
	index_list = None
	if args.dataset:
		dataset_index = args.dataset
		if ':' in dataset_index:
			index_list = dataset_index.split(':')
		else:
			index_list = [dataset_index]
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

	# index_list = list(set(sorted(index_list)))

# def downlaod(file, url):

# print(f"d = {args.d}")

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
# parser.add_argument('-f', '--foo')
# args = parser.parse_args()
# print(args.accumulate(args.integers))

def download(file_name):
	url = url_dict.get(file_name)
	response = requests.get(url, stream=True)
	total_size_in_bytes= int(response.headers.get('content-length', 0))
	block_size = 1024 #1 Kibibyte

	if response.status_code == 200:
		print(f"Downloading {file_name}")
		progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
		with open(file_name, 'wb') as file:
			for data in response.iter_content(block_size):
				progress_bar.update(len(data))
				file.write(data)
	# progress_bar.close()

	if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
		print("ERROR, something went wrong")
		exit(1)

if __name__ == '__main__':
	args = parser.parse_args()
	header, index_list = arg_check(args)

	if header:
		download('bimcv_covid19_posi_head_iter1.tgz')
	for index in index_list:
		download(f"bimcv_covid19_posi_subjects_{index}.tgz")
'''
homepage = requests.get('https://osf.io/nh7g8/')
# data-level = 5 class="tb-row tb-odd"
soup = BeautifulSoup(homepage.text, 'html.parser')
# print(soup)
# print(soup.find_all('a', class_="tb-row tb-odd"))
for link in soup.find_all('a', href=True):
	print(link['href'])
'''