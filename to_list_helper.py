from datetime import date
import time

class TodoListTTemp(object):
    def __init__(self,mysql):
        self.counter = 0
        self.todos = []
        self.mysql= mysql

    def create_Update_Task(self, data):
        self.counter += 1
        data['id'] = self.counter
        self.todos.append(data)
        return data


    def get_all_tasks(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM todos")
        retrivedData,result = cur.fetchall(),[]
        for task in retrivedData:
            todo = {"id": task[0], "task": task[1],"due_date": task[2], "status": task[3]}
            result.append(todo)
        return result

    def get_all_finished_tasks(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM todos")
        retrivedData,result = cur.fetchall(),[]
        for task in retrivedData:
            if task[3] == "Finished":
                todo={"id": task[0], "task": task[1],"due_date": task[2], "status": task[3]}
                result.append(todo)
        return result

    def get_all_overdue_tasks(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM todos")
        retrivedData,result = cur.fetchall(),[]
        for task in retrivedData:
            dueDate = task[2]
            formattedDueDate = time.strptime(dueDate, "%Y-%m-%d")
            formattedCurrentDate = time.strptime(str(date.today()), "%Y-%m-%d")
            todo={"id": task[0], "task": task[1],"due_date": task[2], "status": task[3]}
            if formattedDueDate < formattedCurrentDate and task[3] != "Finished":
                result.append(todo)
        return result
    
    def get_all_due_tasks(self, due_date):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM todos")
        retrivedData,result = cur.fetchall(),[]
        for task in retrivedData:
            todo= {"id": task[0], "task": task[1],"due_date": task[2], "status": task[3]}
            if task[2] == due_date and task[3] != "Finished":
                result.append(todo)
        return result

    def get_task(self, id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM todos")
        retrivedData,result = cur.fetchall(),[]
        for task in retrivedData:
            if task[0] == id:
                todo= {"id": task[0], "task": task[1],"due_date": task[2], "status": task[3]}
                result.append(todo)
        return result
