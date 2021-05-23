import os
from enum import Enum


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Importance(Enum):
    very_important = 1
    important = 2
    not_important = 3


class BattleLog(metaclass=Singleton):

    def __init__(self):
        self.output = 'output'
        if self.output not in os.listdir():
            os.mkdir(self.output)

        self.full_log_path = self.output + '/full_log.md'
        self.important_log_path = self.output + '/important_log.md'
        self.very_important_log_path = self.output + '/very_important_log.md'

        self.full_log = self.open_log(self.full_log_path)
        self.important_log = self.open_log(self.important_log_path)
        self.very_important_log = self.open_log(self.very_important_log_path)

    @staticmethod
    def open_log(path):
        return open(path, 'w')

    def log(self, importance: Importance, message):
        self.full_log.write(message + '\n\n')
        if importance == Importance.important or \
                importance == Importance.very_important:
            self.important_log.write(message + '\n\n')
        if importance == Importance.very_important:
            self.very_important_log.write(message + '\n\n')
            print(message)

    def close_files(self):
        self.full_log.close()
        self.important_log.close()
