from flask import Flask,jsonify,request,render_template

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


import sqlite3
conn = sqlite3.connect('db.recipes', check_same_thread=False)
db_cursor=conn.cursor()

query_sql='select id,title,making_time,serves,ingredients,cost from recipes'
insert_sql="INSERT INTO recipes VALUES (NULL,'{0}','{1}','{2}','{3}',{4},'{5}','{6}')"
update_sql="update recipes set title='{0}',making_time='{1}',serves='{2}',ingredients='{3}',cost='{4}',updated_at='{5}' where id={6}"
delete_sql="delete from recipes where id={0}"

#conn.close()



import datetime;
ct = datetime.datetime.now()
cts=ct.strftime("%Y-%m-%d %H:%M:%S")



def query2dict(header,result):
  query_output={}
  for i in range(len(header)):
      query_output[header[i][0]]=result[i]
  return(query_output)

##################################################################

@app.route('/')
def home():
  return "no resource",404

@app.route('/recipes',methods=['PURGE'])
def inidb():
  db_cursor.execute("DROP TABLE IF EXISTS recipes")
  db_cursor.execute("""CREATE TABLE IF NOT EXISTS recipes (
    id integer PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    making_time TEXT NOT NULL,
    serves TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    cost integer NOT NULL,
    created_at datetime ,
    updated_at datetime
  );""")

  db_cursor.execute("""INSERT INTO recipes (
    id,
    title,
    making_time,
    serves,
    ingredients,
    cost,
    created_at,
    updated_at
  )
  VALUES (
    1,
    'チキンカレー',
    '45分',
    '4人',
    '玉ねぎ,肉,スパイス',
    1000,
    '2016-01-10 12:10:12',
    '2016-01-10 12:10:12'
  );""")

  db_cursor.execute("""INSERT INTO recipes (
    id,
    title,
    making_time,
    serves,
    ingredients,
    cost,
    created_at,
    updated_at
  )
  VALUES (
    2,
    'オムライス',
    '30分',
    '2人',
    '玉ねぎ,卵,スパイス,醤油',
    700,
    '2016-01-11 13:10:12',
    '2016-01-11 13:10:12'
  );""")
  conn.commit()  
  return "reset",200

@app.route('/recipes',methods=['GET'])
def get_recipes():
  result=[]
  db_cursor.execute(query_sql)
  for recipe in db_cursor.fetchall():
    result.append(query2dict(db_cursor.description,recipe))
  return jsonify({'recipes':result}),200


@app.route('/recipes/<int:id>',methods=['GET'])
@app.route('/recipes/',methods=['GET'])
def get_recipe(id=1):
  db_cursor.execute(query_sql+' where id={0}'.format(id))
  queryresult=db_cursor.fetchone()
  if queryresult==None:
    return jsonify ({'message': "No Recipe found"}),200
  else:
    return jsonify({'message': 'Recipe details by id','recipe':[query2dict(db_cursor.description,queryresult)]})


@app.route('/recipes', methods=['POST'])
def create_recipt():
  errmsg={'message':"Recipe creation failed!","required": "title, making_time, serves, ingredients, cost"}
  request_data = request.get_json()
  request_keys=list(request_data.keys())

  if 'title' not in request_keys or 'making_time' not in request_keys or 'serves' not in request_keys or 'ingredients'  not in request_keys or 'cost'  not in request_keys:
    return jsonify(errmsg),200
  else:
    db_cursor.execute(insert_sql.format(request_data['title'],request_data['making_time'],request_data['serves'],request_data['ingredients'],request_data['cost'],cts,cts))
    db_cursor.execute(query_sql+' where id =(select max(id) from recipes)')
    queryresult=db_cursor.fetchone()
  return jsonify({'message': 'Recipe successfully created!','recipe':[query2dict(db_cursor.description,queryresult)]}),200


@app.route('/recipes/<int:id>', methods=['PATCH'])
@app.route('/recipes/', methods=['PATCH'])
def update_recipe(id=1):
  request_data = request.get_json()
  db_cursor.execute(query_sql+' where id={0}'.format(id))
  queryresult=db_cursor.fetchone()
  if queryresult==None:
    return jsonify ({'message': 'recipe not found'}),200
  else:
    db_cursor.execute(update_sql.format(request_data['title'],request_data['making_time'],request_data['serves'],request_data['ingredients'],request_data['cost'],cts,id))
    db_cursor.execute(query_sql+' where id={0}'.format(id))
    queryresult=db_cursor.fetchone()
    return jsonify({'message': 'Recipe successfully updated!','recipe':[query2dict(db_cursor.description,queryresult)]}),200    

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
  db_cursor.execute(query_sql+' where id={0}'.format(id))
  queryresult=db_cursor.fetchone()
  if queryresult==None:
    return jsonify ({'message': 'recipe not found'}),200
  else:
    db_cursor.execute(delete_sql.format(id))
    return jsonify({"message": "Recipe successfully removed!"}),200  

if __name__ == 'main':
  app.run()
# app.run()  

