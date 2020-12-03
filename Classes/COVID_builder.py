import abc
from Classes.xray_dataset import Xray_dataset

class COVID_builder(metaclass=abc.ABCMeta):

    def __init__(self):
        self._dataset = Xray_dataset()

    @abc.abstractmethod
    def _load_dataset(self):
        pass

    @abc.abstractmethod
    def _sanity_check(self):
        pass
