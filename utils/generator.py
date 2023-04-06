

class IDGenerator():
    def __init__(self):
        self.id = 0

    def next(self):
        self.id +=1
        return self.id


