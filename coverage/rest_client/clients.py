import requests
import uuid
import json
from abc import ABC, abstractmethod

class AbstractClient(ABC):
    def __init__(self, token):
        self.base_url = "https://api.todoist.com/rest/v1/"
        self.token = token
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def get(self, params):
        pass
    
    @abstractmethod
    def create(self, params):
        pass
    
    @abstractmethod
    def update(self, params):
        pass
    
    @abstractmethod
    def delete(self, params):
        pass
    
    
class ProjectsClients(AbstractClient):

    def get_all(self):
        pass
    
    def get(self, params):
        pass
    
    def create(self, params):
        pass
    
    def update(self, params):
        pass
    
    def delete(self, params):
        pass