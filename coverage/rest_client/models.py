class Projects():
    
    """It is an encasulaption class of Projects object
    
    Create a model object for Projects data.
    """
    
    def __init__(self, id, name, parent,
                 order, comment_count):
        """Creating instance of Projects
        
        It is defining properties for Projects client model.
        
        :param id: id of the project
        :param name: name of the project
        :param parent: parent project of this project (if any)
        :param order: order of project location under a parent one (if any)
        :param comment_count: total of comments made for this project
        :type id: int
        :type name: string
        :type parent: int
        :type order: int
        :type comment_count: int
        :return: instance of Projects
        :rtype: Projects 
        """
        self.id = id
        self.name = name
        self.parent = parent
        self.order = order
        self.comment_count = comment_count
    
    def __str__(self):
        return self.name
        
class Dues():

    """It is an encasulaption class of Dues object
    
    Create a model object for Dues data.
    """

    def __init__(self, string, date, 
                 datetime, timezone):
        """Creating instance of Dues (Due of a task)
        
        It is defining properties for Dues client model.
        
        :param string: string representation of due time
        :param date: date string representation of due
        :param datetime: datetime string representation of due
        :param timezone: order of project location under a parent one (if any)
        :type string: string
        :type date: string
        :type datetime: string
        :type timezone: string
        :return: instance of Dues
        :rtype: Dues
        """
        self.string = string
        self.date = date
        self.datetime = datetime
        self.timezone = timezone
    
    def __str__(self):
        return self.string

class Tasks():

    """It is an encasulaption class of Tasks object
    
    Create a model object for Tasks data.
    """

    def __init__(self, id, project_id,
                 content, completed,
                 label_ids, parent, order,
                 priority, due, url,
                 comment_count):
        """Creating instance of Tasks
        
        It is defining properties for Tasks client model.
        
        :param id: id of the task
        :param project_id: id of the project where this task is located
        :param content: content of the task
        :param completed: status of task completion
        :param label_ids: array id of labes used on this task
        :param parent: refer to parent taks id of this task
        :param order: position of task under same parent (task)
        :param priority: Task priority from 1 (normal/default) to urgent (4)
        :param due: object representing Dues (due time/date)
        :param url: URL to access this task in Todoist web interface
        :param comment_count: total of comments made for this task
        :type id: int
        :type content: string
        :type completed: boolean
        :type label_ids: list
        :type poarent: int
        :type order: int
        :type priority: int
        :type due: Dues
        :type url: string
        :type comment_count: int
        :return: instance of Task
        :rtype: Tasks
        """
        self.id = id
        self.project_id = project_id
        self.content = content
        self.completed = completed
        self.label_ids = label_ids
        self.parent = parent
        self.order = order
        self.priority = priority
        self.due = due
        self.url = url
        self.comment_count = comment_count

    def __str__(self):
        str_ret = "{}_{}".format(self.id, self.content)
        return str_ret
