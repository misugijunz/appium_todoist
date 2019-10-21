class Projects():
    def __init__(self, id, name, parent,
                 order, comment_count):
        self.id = id
        self.name = name
        self.parent = parent
        self.order = order
        self.comment_count = comment_count
    
    def __str__(self):
        return self.name
        
class Dues():
    def __init__(self, string, date, 
                 datetime, timezone):
        self.string = string
        self.date = date
        self.datetime = datetime
        self.timezone = timezone
    
    def __str__(self):
        return self.name

class Tasks():
    def __init__(self, id, project_id,
                 content, completed,
                 label_ids, parent, order,
                 priority, due, url,
                 comment_count):
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
        return self.name