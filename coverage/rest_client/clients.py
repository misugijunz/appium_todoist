import requests
import uuid
import json
from .models import Projects, Dues, Tasks
from abc import ABCMeta, abstractmethod

class AbstractClient():
    
    """It is an abstract client to define basic behaviour of the API client objects.
    
    The class defines default behaviour of API with/without implementation and it should
    be instantiated with extending classes.
    """
    
    __metaclass__ = ABCMeta
    
    def __init__(self, token):
        """Constructor of AbstractClient
        
        It defines basic properties of extending classes. Instance should be made with extending
        classes.
        
        :param token: The auth token provided by Todoist app
        :type token: string
        """
        self.base_url = "https://api.todoist.com/rest/v1/"
        self.token = token
        self.headers = {
            "Authorization": "Bearer %s" % token
        }
    
    @abstractmethod
    def get_all(self, params=None):
        """Get a collection of objects.
        
        It is an abstract method. Override this to define behaviour of
        getting extending classes' collection of objects with/without
        supplied parameters
        
        :param params: To retrieve specific collection of objects based on params
        :type params: Dict
        """
        pass
    
    @abstractmethod
    def get(self, id):
        """Get an object.
        
        It is an abstract method. Override this to define behaviour of
        getting extending classes' an object with specfic id
        
        :param id: To retrieve an object based on supplied id
        :type id: int
        """
        pass
    
    @abstractmethod
    def create(self, params):
        """Create an object.
        
        It is an abstract method. Override this to define behaviour of
        creating extending classes' an object with specific params
        
        :param params: To create an object based on supplied params
        :type params: int
        """
        pass
    
    @abstractmethod
    def update(self, id, params):
        """Update an object.
        
        It is an abstract method. Override this to define behaviour of
        updating extending classes' an object with specific id & params
        
        :param id: To create an object based on supplied id
        :type id: int
        :param params: To create an object based on supplied params
        :type params: int
        """
        pass
    
    @abstractmethod
    def delete(self, id):
        """Delete an object.
        
        It is an abstract method. Override this to define behaviour of
        deleting extending classes' an object with specific id
        
        :param id: To create an object based on supplied id
        :type id: int
        """
        pass
    
 
class ProjectsClient(AbstractClient):
    
    """It is a class to define API client for task.
    
    The class defines default behaviour of task's client API.
    """

    def get_all(self, params=None):
        """Get a collection of projects.
        
        It is getting collection of projects from REST API.
        
        :param params: params isn't required and should not be provided for this api
        :type params: Dict
        :return: projects object model list
        :rtype: List
        """
        api_url = self.base_url + "projects"
        projects_arr = requests.get(api_url,
                                    headers=self.headers).json()
        projects = []
        for project_dict in projects_arr:
            project = self._create_project_instance(project_dict)
            projects.append(project)
        return projects
        
    
    def get(self, id):
        """Get a project.
        
        It is getting a project from REST API with supplied project's ID
        
        :param id: To retrieve a project based on supplied id
        :type id: int
        :return: project object model
        :rtype: Projects
        """
        api_url = self.base_url + "projects"
        api_url = api_url + "/{}".format(id)
        project_dict = requests.get(api_url,
                                    headers=self.headers).json()
        project = self._create_project_instance(project_dict)
        return project
    
    def create(self, params):
        """Create a project.
        
        It is creating project via REST API with supplied params.
        
        :param params: To create a project based on supplied params
        :type params: int
        :return: project object model
        :rtype: Projects
        """
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
        """Update a project.
        
        It is updating a project via REST API
        
        :param id: To update a project based on supplied id
        :type id: int
        :param params: To update a project based on supplied params
        :type params: int
        :return: resp of requests lib's http request
        :rtype: Response
        """
        api_url = self.base_url + "projects"
        api_url = api_url + "/{}".format(id)
        _header = self.headers
        _header["Content-Type"] = "application/json"
        _header["X-Request-Id"] = str(uuid.uuid4())
        resp = requests.post(api_url,
                             data=json.dumps(params),
                             headers=_header)
        return resp

    def delete(self, id):
        """Delete a project.
        
        Delete a project with supplied project's ID via REST API
        
        :param id: To delete a project based on supplied id
        :type id: int
        :return: resp of requests lib's http request
        :rtype: Response
        """
        api_url = self.base_url + "projects"
        api_url = api_url + "/{}".format(id)
        resp = projects_arr = requests.delete(api_url,
                                              headers=self.headers)
        return resp
        
    def _create_project_instance(self, dict):
        """Create instance of project model.
        
        Internal method for creating project model object
        
        :param dict: Dict object of retrieved project
        :type dict: Dict
        :return: project object model
        :rtype: Projects
        """
        id = dict.get('id')
        name = dict.get('name')
        parent = dict.get('parent')
        order = dict.get('order')
        comment_count = dict.get('comment_count')
        project = Projects(id, name, parent, order, comment_count)
        return project


class TasksClient(AbstractClient):
    
    """It is a class to define API client for Task.
    
    The class defines default behaviour of Task's client API.
    """
    
    def get_all(self, params):
        """Get a collection of Tasks.
        
        It is getting collection of Tasks from REST API.
        
        :param params: params is to provide task's id which Tasks are part of
        :type params: Dict
        :return: tasks object model list
        :rtype: List
        """
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
        """Get an active Task.
        
        It is getting an active Task from REST API with supplied Task's ID
        
        :param id: To retrieve an active Task based on supplied id
        :type id: int
        :return: task object model
        :rtype: Tasks
        """
        api_url = self.base_url + "tasks"
        api_url = api_url + "/{}".format(id)
        task_dict = requests.get(api_url,
                                    headers=self.headers).json()
        task = self._create_task_instance(task_dict)
        return task
    
    def create(self, params):
        """Create a Task.
        
        It is creating Task via REST API with supplied params.
        
        :param params: To create a Task based on supplied params
        :type params: int
        :return: task object model
        :rtype: Tasks
        """
        api_url = self.base_url + "tasks"
        # append additional headers for post request
        _header = self.headers
        _header["Content-Type"] = "application/json"
        _header["X-Request-Id"] = str(uuid.uuid4())
        task_dict = requests.post(api_url,
                                  data=json.dumps(params),
                                  headers=_header).json()
        task = self._create_task_instance(task_dict)
        return task

    def update(self, id, params):
        """Update a Task.
        
        It is updating a Task via REST API
        
        :param id: To update a Task based on supplied id
        :type id: int
        :param params: To update a Task based on supplied params
        :type params: int
        :return: resp of requests lib's http request
        :rtype: Response
        """
        api_url = self.base_url + "tasks"
        api_url = api_url + "/{}".format(id)
        # add additional headers for post request
        _header = self.headers
        _header["Content-Type"] = "application/json"
        _header["X-Request-Id"] = str(uuid.uuid4())
        resp = requests.post(api_url,
                             data=json.dumps(params),
                             headers=_header)
        return resp

    def delete(self, id):
        """Delete a task.
        
        Delete a task with supplied task's ID via REST API
        
        :param id: To delete a task based on supplied id
        :type id: int
        :return: resp of requests lib's http request
        :rtype: Response
        """
        api_url = self.base_url + "tasks"
        api_url = api_url + "/{}".format(id)
        resp = requests.delete(api_url,
                               headers=self.headers)
        return resp
    
    def close(self, id):
        """Close a task.
        
        Close a task with supplied task's ID via REST API
        
        :param id: To close a task based on supplied id
        :type id: int
        :return: resp of requests lib's http request
        :rtype: Response
        """
        api_url = self.base_url + "tasks"
        api_url = api_url + "/{}/close".format(id)
        resp = requests.post(api_url,
                             headers=self.headers)
        return resp
    
    def reopen(self, id):
        """Reopen a task.
        
        Reopen a closed task with supplied task's ID via REST API
        
        :param id: To reopen a task based on supplied id
        :type id: int
        :return: resp of requests lib's http request
        :rtype: Response
        """
        api_url = self.base_url + "tasks"
        api_url = api_url + "/{}/reopen".format(id)
        resp = requests.post(api_url,
                             headers=self.headers)
        return resp
        
    def _create_task_instance(self, dict):
        """Create instance of Task model.
        
        Internal method for creating Task model object
        
        :param dict: Dict object of retrieved Tasks
        :type dict: Dict
        :return: Tasks object model
        :rtype: Tasks
        """
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
        
        task = Tasks(id, project_id, content,
                     completed, label_ids,
                     parent, order, priority,
                     _due, url, comment_count)
        return task
    
    def _create_due_instance(self, dict):
        """Create instance of Dues model.
        
        Internal method for creating Dues model object
        
        :param dict: Dict object of retrieved Dues
        :type dict: Dict
        :return: Dues object model
        :rtype: Dues
        """
        strin = dict.get('string')
        date = dict.get('date')
        datetime = dict.get('datetime')
        timezone = dict.get('timezone')
        due = Dues(strin, date, datetime, timezone)
        return due;
