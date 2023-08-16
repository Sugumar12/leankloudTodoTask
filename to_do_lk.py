from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

# own class and methods for code readability
from db_connection import setDBConnection
from to_list_helper import TodoListTTemp


app = Flask(__name__)

# MySQL database configurations
mysql =  setDBConnection(app)

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
          description='A simple TodoMVC API',)


ns = api.namespace('todos', description='TODO operations')


todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='Task details'),
    # Adding two new fields to each task (due_date and status)
    'due_date': fields.String(required=True, description='Task due date'),
    'status': fields.String(required=True, description='Status of the task'),
})


# Object declaration
DAO = TodoListTTemp(mysql)


@ns.route("/")
class TodoList(Resource):
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        allTasks = DAO.get_all_tasks()
        return allTasks

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        sourceDictionary = DAO.create_Update_Task(api.payload)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO todos(task,due_date,status,id) VALUES(%s,%s,%s,%s)", (
            sourceDictionary["task"], sourceDictionary["due_date"], sourceDictionary["status"], sourceDictionary["id"]))
        mysql.connection.commit()
        cur.close()
        return sourceDictionary, 201


@ns.route("/finished")
class getFinished(Resource):
    '''Shows a list of all todos that are finished'''
    @ns.doc('list_finished_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all the finished tasks'''
        finishedTasks = DAO.get_all_finished_tasks()
        return finishedTasks

@ns.route("/overdue")
class getOverdue(Resource):
    '''Shows a list of all todos that are overdue'''
    @ns.doc('list_overdue_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all the overdue tasks'''
        overdueTasks = DAO.get_all_overdue_tasks()
        return overdueTasks



@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete and edit them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a task given its id'''
        aTask = DAO.get_task(id)
        return aTask

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM todos WHERE id = {}".format(id))
        mysql.connection.commit()
        return "DELETED"


    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        sourceDictionary = DAO.create_Update_Task(api.payload)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE todos SET task = %s, due_date = %s,status=%s WHERE id ={}".format(
            id), (sourceDictionary["task"], sourceDictionary["due_date"], sourceDictionary["status"]))
        mysql.connection.commit()
        return "UPDATED"



@ns.route('/<string:due_date>')
@ns.response(404, 'No Dues')
@ns.param('due_date', 'Due date for the task')
class getTodosForGivenDate(Resource):
    '''Shows due with given date'''
    @ns.doc('get_dues_with_given_date')
    @ns.marshal_with(todo)
    def get(self, due_date):
        '''Fetch dues of the day'''
        dueTasks = DAO.get_all_due_tasks(due_date)
        return dueTasks


if __name__ == '__main__':
    app.run(debug=True)