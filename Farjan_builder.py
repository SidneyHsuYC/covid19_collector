from ICOVID_builder import *
class Farjan_builder(COVID_builder):
    def __init__(self, path = 'farjan_repo/covid_chestXray_dataset'):
        super().__init__()
        self.folder_path = path
    
    def _load_dataset(self):
        try:
            dirs = os.listdir(self.folder_path / 'covid_19 dataset')
            label_from_folder = ['COVID-19' if i == 'covid19' else i for i in dirs]

            for index, sub_dir in enumerate(dirs):
                # for file in os.listdir(Path.cwd() / 'covid_19 dataset' / sub_dir):
                #     print(file)
                sub_path = self.folder_path / 'covid_19 dataset' / sub_dir
                for file in os.listdir(sub_path):
                    if self._sanity_check(sub_path / file):
                        self._dataset.images.append(str(sub_path / file))
                        self._dataset.labels.append(label_from_folder[index])
                        self._dataset.views.append('')
        except Exception as e:
            raise e

    def _sanity_check(self, file_path):
        if file_path.name in self._dataset.imgname_set:
            logger.info(f"Dataset Farjan, {file_path.name} has duplicate name in dataset.")
            return None
        # Check imagine checksum existed in database
        checksum = 0
        try:
            with open(file_path, 'rb') as f:
                image_file = f.read()
                checksum = hashlib.md5(image_file).hexdigest()
        except FileNotFoundError:
            logger.info(f"Dataset Farjan, {file_path} does not existed.")
            return None
        except Exception as e:
            logger.exception(f"{e}")
        
        if (not checksum) or (checksum in self._dataset.imgsum_set):
            logger.info(f"Dataset Farjan, {file_path} has duplicate checksum in dataset.")
            return None

        # Update set status
        self._dataset.imgname_set.add(file_path.name)
        self._dataset.imgsum_set.add(checksum)
        return True
