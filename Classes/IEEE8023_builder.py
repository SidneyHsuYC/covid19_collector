import csv
import hashlib
import os

from Classes.COVID_builder import COVID_builder

class IEEE8023_builder(COVID_builder):
    def __init__(self, metadata, logger):
        super().__init__()
        self.metadata = metadata
        self.logger = logger

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
            self.logger.warning(e)

    def _sanity_check(self, index, row):
        # Check file name existed in dataset
        if row[self.filename_index] in self._dataset.imgname_set:
            self.logger.info(f"Dataset IEEE8023, image of row #{index} has duplicate name in dataset.")
            return None
        
        # Check imagine checksum existed in database
        checksum = 0
        try:
            with open(f"{row[self.folder_index ]}/{row[self.filename_index]}", 'rb') as f:
                image_file = f.read()
                checksum = hashlib.md5(image_file).hexdigest()
        except FileNotFoundError:
            self.logger.info(f"Dataset IEEE8023, image of row #{index} does not existed.")
            return None
        except Exception as e:
            self.logger.warning(f"{e}")

        if (not checksum) or (checksum in self._dataset.imgsum_set):
            self.logger.info(f"Dataset IEEE8023, image of row #{index} has duplicate checksum in dataset.")
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
