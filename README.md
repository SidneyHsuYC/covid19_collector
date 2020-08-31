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
6. bimcv_repo: `git clone https://github.com/BIMCV-CSUSP/BIMCV-COVID-19` <br>
   PLease follow these steps to build up bimcv dataset.
   1. Download dataset by running `python data_downloader.py`, select number of dataset folder wants to download, then script will automatically download, extract and delete .tgz file. (Source from: https://osf.io/nh7g8/) <br>
   Folder information: <br>
   * (Metadata folder) bimcv_covid19_posi_head_iter1.tgz<br>
   * (Data folder) bimcv_covid19_posi_subjects_1.tgz ... bimcv_covid19_posi_subjects_34.tgz<br>
   * bimcv.py does not require the an entire dataset to run
   2. Download `Frontal_Lateral_Model.h5` from https://www.dropbox.com/s/nn1me22ie5iye1e/Frontal_Lateral_Model.h5?dl=0 and put it under /covid19_collector/bimcv_repo folder. <br>
   3. Run `python generate_hdf5_csv.py`. This will process all source images under bimcv folder and store them into `bimcv_metadata.hdf5`, meanwhile process their corresponding json file, combining with metadata with Metadata folder and store them into `bimcv_metadata.csv`.
