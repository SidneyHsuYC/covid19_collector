import logging
import csv
import os
import hashlib
import abc

from pathlib import Path
# from readme_module import add_key, get_readme_dict

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('imageloader.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class Xray_dataset():
    imgname_set = set()
    imgsum_set = set()

    def __init__(self):
        self.images = []
        self.labels = []
        self.views = []

    def __getitem__(self, index):
        if index >= len(self.images):
            return None
        return (self.images[index], self.labels[index])

    def get_view(self, index):
        if index >= len(self.images):
            return None
        return (self.views[index])

    def __len__(self):
        return len(self.images)

    def __next__(self):
        index = self.index
        self.index += 1
        if index >= len(self.images): 
            raise StopIteration 
        return (self.images[index], self.labels[index], self.views[index])

    def __iter__(self):
        self.index = 0
        return self

# class Director:
#     def __init__(self):
#         self._builder = None

#     def construct(self, builder):
#         self._builder = builder
#         self._builder._load_dataset()
        # self._builder._sanity_check(index, row)

class COVID_builder(metaclass=abc.ABCMeta):

    def __init__(self):
        self._dataset = Xray_dataset()

    @abc.abstractmethod
    def _load_dataset():
        pass

    @abc.abstractmethod
    def _sanity_check():
        pass

class IEEE8023_builder(COVID_builder):
    def __init__(self, metadata):
        super().__init__()
        self.metadata = metadata

    def _load_dataset(self):
        try:
            with open(self.metadata, newline='') as csvfile:
                # print('loading')
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                self.header = next(spamreader)
                self.__load_index(self.header)

                for index, row in enumerate(spamreader):
                    label = ''
                    # Check if multiple values have COVID-19, otherwise skip
                    if ',' in row[self.finding_index]:  # Check multiple value in finding colum
                        cat_list = [cat.strip() for cat in row[self.finding_index].split(',')]
                        if 'COVID-19' in cat_list:
                            label = 'COVID-19'
                        else:
                            continue
                    else:       # Check single value
                        if row[self.finding_index] == 'todo':
                            continue
                        if row[self.finding_index] == 'No Finding':
                            label = 'normal'
                        elif row[self.finding_index] == 'COVID-19':
                            label = 'COVID-19'
                        else:
                            label = 'others' 

                    if self._sanity_check(index, row):
                        self._dataset.images.append(os.path.join(row[self.folder_index], row[self.filename_index]))
                        self._dataset.labels.append(label)
                        self._dataset.views.append(row[self.view_index])
                # print(len(self._dataset.images))
                # print(len(self._dataset.labels))
                # for i in range(20):
                #     print(self._dataset.images[i], self._dataset.labels[i])
        except Exception as e:
            logger.warning(e)

    def _sanity_check(self, index, row):
        # Check file name existed in dataset
        if row[self.filename_index] in self._dataset.imgname_set:
            logger.info(f"Dataset IEEE8023, image of row #{index} has duplicate name in dataset.")
            return None
        
        # Check imagine checksum existed in database
        checksum = 0
        try:
            with open(f"{row[self.folder_index ]}/{row[self.filename_index]}", 'rb') as f:
                image_file = f.read()
                checksum = hashlib.md5(image_file).hexdigest()
        except FileNotFoundError:
            logger.info(f"Dataset IEEE8023, image of row #{index} does not existed.")
            return None
        except Exception as e:
            logger.warning(f"{e}")

        if (not checksum) or (checksum in self._dataset.imgsum_set):
            logger.info(f"Dataset IEEE8023, image of row #{index} has duplicate checksum in dataset.")
            return None

        # Update set status
        self._dataset.imgname_set.add(row[self.filename_index])
        self._dataset.imgsum_set.add(checksum)
        return True

    def __load_index(self, header):
        self.view_index = self.header.index('view')
        self.finding_index = self.header.index('finding')
        self.folder_index = self.header.index('folder')
        self.filename_index = self.header.index('filename')


class Farjan_builder(COVID_builder):
    def __init__(self):
        super().__init__()
    
    def _load_dataset(self):
        try:
            dirs = os.listdir(Path.cwd() / 'covid_19 dataset')
            label_from_folder = ['COVID-19' if i == 'covid19' else i for i in dirs]

            for index, sub_dir in enumerate(dirs):
                # for file in os.listdir(Path.cwd() / 'covid_19 dataset' / sub_dir):
                #     print(file)
                sub_path = Path.cwd() / 'covid_19 dataset' / sub_dir
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

class Sirm_builder(COVID_builder):
    def __init__(self):
        super().__init__()

    def _load_dataset(self):
        try:
            files = [i for i in os.listdir(Path.cwd()) if i.startswith('COVID')]
            for file in files:
                if self._sanity_check(Path.cwd() / file):
                    self._dataset.images.append(str(Path.cwd() / file))
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

def main():

    ieee0832_path = Path.cwd() / 'ieee8032_repo'
    os.chdir(ieee0832_path)
    # ieee_builder = IEEE8023_builder('metadata.csv')

    # ieee_builder._load_dataset()
    # ieee_dataset = ieee_builder._dataset
    # print(f"ieee dataset images quantity: {len(ieee_dataset)}")

    farjan_path = Path.cwd().parent / 'farjan_repo' 
    os.chdir(farjan_path)
    # farjan_builder = Farjan_builder()
    # farjan_builder._load_dataset()
    # farjan_dataset = farjan_builder._dataset
    # print(f"farjan dataset images quantity: {len(farjan_dataset)}")

    sirm_path = Path.cwd().parent / 'sirm_repo' 
    os.chdir(sirm_path)
    sirm_builder = Sirm_builder()
    sirm_builder._load_dataset()
    sirm_dataset = sirm_builder._dataset
    print(f"sirm_path dataset images quantity: {len(sirm_dataset)}")
    print(len(sirm_dataset))
    for i in sirm_dataset:
        print(i)

if __name__ == '__main__':
    main()

