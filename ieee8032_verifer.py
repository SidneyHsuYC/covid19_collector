import os
import pandas as pd

from pathlib import Path
from collections import defaultdict

finding_dic = defaultdict(lambda: defaultdict(int))
current_path = Path(os.getcwd())
repo_path = current_path / 'ieee8032_repo' / 'covid-chestxray-dataset'

def ieee8032_pdreader(filepath=repo_path):
	df = pd.read_csv(repo_path / 'metadata.csv')
	finding_dic = defaultdict(lambda: defaultdict(int))
	for row in df.itertuples(index=False):
	    if 'COVID-19' not in row.finding:
	    	continue
	    if row.filename not in os.listdir(repo_path / row.folder):
	    	continue

	    if ',' in row.finding:
	        cat_list = [cat.strip() for cat in row.finding.split(',')]
	        for cat in cat_list: 
	            finding_dic[cat][row.view] += 1
	    else:
	    	finding_dic[row.finding][row.view] += 1

	return finding_dic.get('COVID-19')

if __name__ == '__main__':
	pd_finding = ieee8032_pdreader()
	print(pd_finding)