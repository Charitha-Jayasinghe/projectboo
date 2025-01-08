from typing import List
from typing import Dict, Any 



class user:
    def __init__(self):
        self._name = None
        self._reference_id = None
        self._description = None
        self._start_date = None
        self._end_date = None
        self.language = None
        

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def reference_id(self):
        return self._reference_id

    @reference_id.setter
    def reference_id(self, value):
        self._reference_id = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def end_date(self):
        return self._end_date
    
    @property
    def language(self):
        return self._language
    
    @language.setter
    def language(self, value):
        self._language = value

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    @property
    def channels(self):
        return self._channels

    


    def to_dict(self):
        return {
            "name": self.name,
            "reference_id": self.reference_id,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "language": self.language,
            "channels": [],
            "users": []
        }