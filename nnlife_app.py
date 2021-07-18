from flask import Flask,jsonify,request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

import datetime;
ct = datetime.datetime.now()
cts=ct.strftime("%Y-%m-%d %H:%M:%S")

def queryrecipe(recipe):
  output={'id':recipe['id']
  ,'title':recipe['title']
  ,'making_time':recipe['making_time']
  ,'serves':recipe['serves']
  ,'ingredients':recipe['ingredients']
  ,'cost':recipe['cost']
  }
  return(output)

recipes = [
    {
        'id':1,
        'title':u'チキンカレー',
        'making_time':u'45分',
        'serves':u'4人',
        'ingredients': u'玉ねぎ,肉,スパイス',
        'cost':1000,
        'created_at':'2016-01-10 12:10:12',
        'updated_at':'2016-01-10 12:10:12'
    },
    {
        'id':2,
        'title':u'オムライス',
        'making_time':u'30分',
        'serves':u'2人',
        'ingredients': u'玉ねぎ,卵,スパイス,醤油',
        'cost':700,
        'created_at':'2016-01-11 13:10:12',
        'updated_at':'2016-01-11 13:10:12'
    }
]


@app.route('/')
def home():
  return f"Hello, World!"


@app.route('/recipes',methods=['GET'])
def get_recipes():
  result=[]
  for recipe in recipes:
    result.append(queryrecipe(recipe))
  return jsonify({'recipes':result}),200
  #pass


@app.route('/recipes/<int:id>',methods=['GET'])
@app.route('/recipes/',methods=['GET'])
def get_recipe(id=1):
  for recipe in recipes:
      if recipe['id'] == id:
          return jsonify({'message': 'Recipe details by id','recipe':[queryrecipe(recipe)]})
  return jsonify ({'message': 'recipe not found'}),200
  #pass

@app.route('/recipes', methods=['POST'])
def create_recipt():
  errmsg={'message':"Recipe creation failed!","required": "title, making_time, serves, ingredients, cost"}
  request_data = request.get_json()
  request_keys=list(request_data.keys())

  if 'title' not in request_keys or 'making_time' not in request_keys or 'serves' not in request_keys or 'ingredients'  not in request_keys or 'cost'  not in request_keys:
    return jsonify(errmsg),400
  else:
    new_recipe={
      'id':recipes[-1]['id'] + 1,
      'title':request_data['title'],
      "making_time": request_data['making_time'],
      "serves": request_data['serves'],
      "ingredients": request_data['ingredients'],
      "cost": request_data['cost'],
      "created_at":cts,
      "updated_at":cts
    }
  recipes.append(new_recipe)  
  return jsonify({'message': 'Recipe successfully created!','recipe':[new_recipe]}),201


# @app.route('/task/<int:task_id>', methods=['PUT'])
# def update_task(task_id):
#   request_data = request.get_json()
#   for task in tasks:
#     if task['id'] == task_id:
#       break

#   task.update({'title': request_data.get('title',task['title']) })
#   task.update({'description': request_data.get('description',task['description']) })
#   task.update({'done': request_data.get('done',task['done']) })
  
#   return jsonify(task)


# @app.route('/task/<int:task_id>', methods=['DELETE'])
# def delete_task(task_id):
#   for task in tasks:
#     if task['id'] == task_id:
#       break
#   tasks.remove(task)
#   return jsonify({'result': True})

if __name__ == 'main':
    app.run() #啟動伺服器