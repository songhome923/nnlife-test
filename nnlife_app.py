from flask import Flask,jsonify,request,render_template

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
  return render_template('index.html'),200


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
  return jsonify ({'message': "No Recipe found"}),200
  #pass

@app.route('/recipes', methods=['POST'])
def create_recipt():
  errmsg={'message':"Recipe creation failed!","required": "title, making_time, serves, ingredients, cost"}
  request_data = request.get_json()
  request_keys=list(request_data.keys())

  if 'title' not in request_keys or 'making_time' not in request_keys or 'serves' not in request_keys or 'ingredients'  not in request_keys or 'cost'  not in request_keys:
    return jsonify(errmsg),200
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
  return jsonify({'message': 'Recipe successfully created!','recipe':[new_recipe]}),200


@app.route('/recipes/<int:id>', methods=['PATCH'])
@app.route('/recipes/', methods=['PATCH'])
def update_recipe(id=1):
  request_data = request.get_json()
  IsExist=0
  for recipe in recipes:
    if recipe['id'] == id:
      IsExist=1
      break
  if IsExist==1:
    recipe.update({'title': request_data.get('title',recipe['title']) })
    recipe.update({'making_time': request_data.get('making_time',recipe['making_time']) })
    recipe.update({'serves': request_data.get('serves',recipe['serves']) })
    recipe.update({'ingredients': request_data.get('ingredients',recipe['ingredients']) })
    recipe.update({'cost': request_data.get('cost',recipe['cost']) })
    recipe.update({'updated_at':cts})
    return jsonify({'message': 'Recipe successfully updated!','recipe':[queryrecipe(recipe)]}),200
  else:
    return jsonify ({'message': 'recipe not found'}),200

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
  IsExist=0
  for recipe in recipes:
    if recipe['id'] == id:
      IsExist=1
      break
  if IsExist==1:
    recipes.remove(recipe)
    return jsonify({"message": "Recipe successfully removed!"}),200
  else:
    return jsonify({"message": "No Recipe found"}),200
  
if __name__ == 'main':
  app.run()

app.run()  