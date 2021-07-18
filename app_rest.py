from flask import Flask,jsonify,request,render_template
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@auth.verify_password
def verify_password(username, password):
    if username=="test" and password=="Orion123":
      return True
    return False

@app.route('/')
def home():
  return "Hello, World!"

# #post /store data: {name :}
# @app.route('/task' , methods=['POST'])
# def create_store():
#   request_data = request.get_json()
#   new_store = {
#     'name':request_data['name'],
#     'items':[]
#   }
#   stores.append(new_store)
#   return jsonify(new_store)
  #pass

#get /store
@app.route('/task')
def get_tasks():
  return jsonify(tasks)
  #pass

#get /store/<name> data: {name :}
@app.route('/task/<int:task_id>')
def get_task(task_id):
  for task in tasks:
      if task['id'] == task_id:
          return jsonify(task)
  return jsonify ({'message': 'task not found'})
  #pass

@app.route('/task', methods=['POST'])
def create_task():
  request_data = request.get_json()
  if not request_data.get('title'):
    return jsonify("Error"),400
  else:
    new_task={
      'id':tasks[-1]['id'] + 1,
      'title':request_data['title'],
      'description':request_data.get('description','none'),
      'done':False
    }
  tasks.append(new_task)
  return jsonify(new_task),201


@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
  request_data = request.get_json()
  for task in tasks:
    if task['id'] == task_id:
      break

  task.update({'title': request_data.get('title',task['title']) })
  task.update({'description': request_data.get('description',task['description']) })
  task.update({'done': request_data.get('done',task['done']) })
  
  return jsonify(task)


@app.route('/task/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
  for task in tasks:
    if task['id'] == task_id:
      break
  tasks.remove(task)
  return jsonify({'result': True})

app.run(host = '0.0.0.0' ,port = 5000, debug = 'True')