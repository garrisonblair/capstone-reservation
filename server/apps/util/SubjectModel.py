import abc

from django.db import models


class SubjectModel:

    # define static list in model class and return it in implementation
    def get_observers(self):
        pass

    def register(self, model_observer):
        self.get_observers().append(model_observer)

    def unregister(self, model_observer):
        self.get_observers().remove(model_observer)

    def object_created(self):
        for observer in self.get_observers():
            print("save")
            print(observer)
            observer.subject_created(self)

    def object_updated(self):
        for observer in self.get_observers():

            observer.subject_updated(self)

    def object_deleted(self):
        for observer in self.get_observers():
            observer.subject_deleted(self)
