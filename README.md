# covid19_collector

Empty folders including farjan_repo, ahmad_repo, ieee8032_repo, sirm_repo and bimcv_repo
are repositories of COVID_19 dataset
Please change to each repository: `cd {repository name}`
And do
1. Farjan_repo: `git clone https://github.com/Farjanasumona/covid_chestXray_dataset.git`
2. ieee8032_repo: `git clone https://github.com/ieee8023/covid-chestxray-dataset`
3. bimcv_repo: TBD
4. sirm_repo: `python3 sirm_repo_downloader.py`
5. ahmad_repo: `git clone https://github.com/ahmadhassan7/Covid-19-Datasets`
6. bimcv_repo: `git clone https://github.com/BIMCV-CSUSP/BIMCV-COVID-19`
   -> Please download entire BIMCV v1.0 dataset from https://osf.io/nh7g8/ , including
   1. bimcv_covid19_posi_head_iter1.tgz
   2. bimcv_covid19_posi_subjects_1.tgz
   3. bimcv_covid19_posi_subjects_2.tgz
   ...
   33. bimcv_covid19_posi_subjects_33.tgz
   34. bimcv_covid19_posi_subjects_34.tgz
   * bimcv.py does not require the entire data set to run