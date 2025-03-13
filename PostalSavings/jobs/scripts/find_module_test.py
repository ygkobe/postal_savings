import os


class TaskImplementor(object):

    def __init__(self):
        self.data = "test "

    def trigger(self):
        print(self.data, 1)

    def sync(self):
        print(self.data, 2)
