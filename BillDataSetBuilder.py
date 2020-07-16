from Sirm_builder import Sirm_builder
from Farjan_builder import Farjan_builder
from IEEE8032_builder import IEEE8023_builder
from pathlib import Path
def main():

    ieee0832_path = Path.cwd() / 'ieee8032_repo/covid-chestxray-dataset'
    #os.chdir(ieee0832_path)
    ieee_builder = IEEE8023_builder(ieee0832_path / 'metadata.csv')

    ieee_builder._load_dataset()
    ieee_dataset = ieee_builder._dataset
    print(f"ieee dataset images quantity: {len(ieee_dataset)}")

    farjan_path = Path.cwd() / 'farjan_repo/covid_chestXray_dataset' 
    #os.chdir(farjan_path)
    farjan_builder = Farjan_builder(farjan_path)
    farjan_builder._load_dataset()
    farjan_dataset = farjan_builder._dataset
    print(f"farjan dataset images quantity: {len(farjan_dataset)}")

    sirm_path = Path.cwd() / 'sirm_repo' 
    #os.chdir(sirm_path)
    sirm_builder = Sirm_builder(sirm_path)
    sirm_builder._load_dataset()
    sirm_dataset = sirm_builder._dataset
    print(f"sirm_path dataset images quantity: {len(sirm_dataset)}")
    print(len(sirm_dataset))
    for i in sirm_dataset:
        print(i)

if __name__ == '__main__':
    main()