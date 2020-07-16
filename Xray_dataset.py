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