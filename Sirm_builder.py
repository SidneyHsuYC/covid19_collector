from ICOVID_builder import *
class Sirm_builder(COVID_builder):
    def __init__(self, path):
        super().__init__()
        self.folder_path = path
    def _load_dataset(self):
        try:
            files = [i for i in os.listdir(self.folder_path) if i.startswith('COVID')]
            for file in files:
                if self._sanity_check(self.folder_path / file):
                    self._dataset.images.append(str(self.folder_path / file))
                    self._dataset.labels.append('COVID-19')
                    self._dataset.views.append('')
        except Exception as e:
            logger.exception(f"e")

    def _sanity_check(self, file_path):
        if file_path.name in self._dataset.imgname_set:
            logger.info(f"Dataset Sirm, {file_path.name} has duplicate name in dataset.")
            return None
        # Check imagine checksum existed in database
        checksum = 0
        try:
            with open(file_path, 'rb') as f:
                image_file = f.read()
                checksum = hashlib.md5(image_file).hexdigest()
        except FileNotFoundError:
            logger.info(f"Dataset Sirm, {file_path} does not existed.")
            return None
        except Exception as e:
            logger.exception(f"{e}")
        
        if (not checksum) or (checksum in self._dataset.imgsum_set):
            logger.info(f"Dataset Sirm, {file_path} has duplicate checksum in dataset.")
            return None

        # Update set status
        self._dataset.imgname_set.add(file_path.name)
        self._dataset.imgsum_set.add(checksum)
        return True