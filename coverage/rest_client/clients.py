import requests
import uuid
import json
from .models import Projects, Dues, Tasks
from abc import ABCMeta, abstractmethod

class AbstractClient():
    __metaclass__ = ABCMeta
    
    def __init__(self, token):
        self.base_url = "https://api.todoist.com/rest/v1/"
        self.token = token
        self.headers = {
            "Authorization": "Bearer %s" % token
        }
    
    @abstractmethod
    def get_all(self, params=None):
        pass
    
    @abstractmethod
    def get(self, id):
        pass
    
    @abstractmethod
    def create(self, params):
        pass
    
    @abstractmethod
    def update(self, id, params):
        pass
    
    @abstractmethod
    def delete(self, id):
        pass
    
 
class ProjectsClient(AbstractClient):

    def get_all(self, params=None):
        api_url = self.base_url + "projects"
        projects_arr = requests.get(api_url,
                                    headers=self.headers).json()
        projects = []
        for project_dict in projects_arr:
            project = self._create_project_instance(project_dict)
            projects.append(project)
        return projects
        
    
    def get(self, id):
        api_url = self.base_url + "projects"
        api_url = api_url + "/" + id
        project_dict = requests.get(api_url,
                                    headers=self.headers).json()
        project = self._create_project_instance(project_dict)
        return project
    
    def create(self, params):
        api_url = self.base_url + "projects"
        _header = self.headers
        _header["Content-Type"] = "application/json"
        _header["X-Request-Id"] = str(uuid.uuid4())
        project_dict = requests.post(api_url,
                                     data=json.dumps(params),
                                     headers=_header).json()
        project = self._create_project_instance(project_dict)
        return project

    def update(self, id, params):
        api_url = self.base_url + "projects"
        api_url = api_url + "/" + id
        _header = self.headers
        _header["Content-Type"] = "application/json"
        _header["X-Request-Id"] = str(uuid.uuid4())
        resp = requests.post(api_url,
                             data=json.dumps(params),
                             headers=_header).json()
        return resp

    def delete(self, id):
        api_url = self.base_url + "projects"
        api_url = api_url + "/" + id
        resp = projects_arr = requests.delete(api_url,
                                              headers=self.headers).json()
        return resp
        
    def _create_project_instance(self, dict):
        id = dict.get('id')
        name = dict.get('name')
        parent = dict.get('parent')
        order = dict.get('order')
        comment_count = dict.get('comment_count')
        project = Projects(id, name, parent, order, comment_count)
        return project


class TasksClient(AbstractClient):
    
    def get_all(self, params):
        api_url = self.base_url + "tasks"
        tasks_arr = requests.get(api_url,
                                 params=params,
                                 headers=self.headers).json()
        tasks = []
        for task_dict in tasks_arr:
            task = self._create_task_instance(task_dict)
            tasks.append(task)
        return tasks
        
    def get(self, id):
        api_url = self.base_url + "tasks"
        api_url = api_url + "/" + id
        project_dict = requests.get(api_url,
                                    headers=self.headers).json()
        project = self._create_task_instance(project_dict)
        return project
    
    def create(self, params):
        api_url = self.base_url + "tasks"
        _header = self.headers
        _header["Content-Type"] = "application/json"
        _header["X-Request-Id"] = str(uuid.uuid4())
        project_dict = requests.post(api_url,
                                     data=json.dumps(params),
                                     headers=_header).json()
        project = self._create_task_instance(project_dict)
        return project

    def update(self, id, params):
        api_url = self.base_url + "tasks"
        api_url = api_url + "/" + id
        _header = self.headers
        _header["Content-Type"] = "application/json"
        _header["X-Request-Id"] = str(uuid.uuid4())
        resp = requests.post(api_url,
                             data=json.dumps(params),
                             headers=_header).json()
        return resp

    def delete(self, id):
        api_url = self.base_url + "tasks"
        api_url = api_url + "/{}".format(id)
        resp = requests.delete(api_url,
                               headers=self.headers).json()
        return resp
    
    def close(self, id):
        api_url = self.base_url + "tasks"
        api_url = api_url + "/{}/close".format(id)
        resp = requests.delete(api_url,
                               headers=self.headers).json()
        return resp
    
    def reopen(self, id):
        api_url = self.base_url + "tasks"
        api_url = api_url + "/{}/reopen".format(id)
        resp = requests.delete(api_url,
                               headers=self.headers).json()
        return resp
        
    def _create_task_instance(self, dict):
        due_dict = dict.get('due')
        _due = None
        if due_dict is not None:
            _due = self._create_due_instance(due_dict)
        id = dict.get('id')
        project_id = dict.get('project_id')
        content = dict.get('content')
        completed = dict.get('completed')
        label_ids = dict.get('label_ids')
        parent = dict.get('parent')
        order = dict.get('order')
        priority = dict.get('priority')
        url = dict.get('url')
        comment_count = dict.get('comment_count')
        
        project = Tasks(id, project_id, content,
                        completed, label_ids,
                        parent, order, priority,
                        _due, url, comment_count)
        return project
    
    def _create_due_instance(self, dict):
        strin = dict.get('string')
        date = dict.get('date')
        datetime = dict.get('datetime')
        timezone = dict.get('timezone')
        due = Dues(strin, date, datetime, timezone)
        return due;
