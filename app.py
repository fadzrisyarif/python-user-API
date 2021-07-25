from flask import Flask, request, render_template
from flask_restful import Api, Resource
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

api = Api(app)
connection = sqlite3.connect("user.db")
cursor = connection.cursor()

query1 = '''CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, email TEXT)'''
cursor.execute(query1)
# query2 = '''INSERT INTO user (id, firstname, lastname, email) VALUES(NULL, ?,?,?)'''
# cursor.execute(query2, ("John", "Doe", "johndoe@mail.com"))

connection.commit()

cursor.execute("select * from user")
res = cursor.fetchall()
# print(len(res))
users = []
for i in range(len(res)):
    users.append({'id' : res[i][0], 'firstname' : res[i][1], 'lastname' : res[i][2], 'email' : res[i][3]})

connection.close()

class User(Resource):
    def get(self, id):
        user = next(filter(lambda x:x['id'] == id, users), None)
        return {'user':user}
    def delete(self, id):
        global users
        users = list(filter(lambda x:x['id']!=id, users))
        return users
    def put(self, name):
        data = request.get_json()
        user = next(filter(lambda x:x['name'] == name,users),None)
        if user is None:
            user = {'name':name,'price':data['price']}
            users.append(user)
        else:
            user.update(data)

class AddUser(Resource):
    def post(self):
        data = request.get_json()
        global users
        email = data['email']
        if email == next(filter(lambda x:x['email'] == email, users), None):
            return {'message':'user'+email+'exist'}
        
        con = sqlite3.connect("user.db")
        cur = con.cursor()
        q = '''INSERT INTO user (id, firstname, lastname, email) VALUES(NULL, ?,?,?)'''
        cur.execute(q, (data['firstname'], data['lastname'], data['email']))
        cur.execute("select * from user")

        global res    
        res = cur.fetchall()
        con.commit()

        users = []
        for i in range(len(res)):
            users.append({'id' : res[i][0], 'firstname' : res[i][1], 'lastname' : res[i][2], 'email' : res[i][3]})

        user = next(filter(lambda x:x['email'] == email, users), None)
        return {'user': user}

class DeleteUser(Resource):
    def post(self):
        data = request.get_json()
        global users
        
        con = sqlite3.connect("user.db")
        cur = con.cursor()
        q = '''DELETE FROM user WHERE id = ?'''
        print(data['id'])
        cur.execute(q, (data['id'],))
        cur.execute("select * from user")

        global res    
        res = cur.fetchall()
        con.commit()

        users = []
        for i in range(len(res)):
            users.append({'id' : res[i][0], 'firstname' : res[i][1], 'lastname' : res[i][2], 'email' : res[i][3]})

        return {'Delete status': 'Success'}

class UpdateUser(Resource):
    def post(self):
        data = request.get_json()
        global users
        
        con = sqlite3.connect("user.db")
        cur = con.cursor()
        q = '''UPDATE user
        SET firstname = ?,
            lastname = ?,
            email = ?
        WHERE
            id = ?;'''
        print(data['id'])
        cur.execute(q, (data['firstname'], data['lastname'], data['email'], data['id']))
        cur.execute("select * from user")

        global res    
        res = cur.fetchall()
        con.commit()

        users = []
        for i in range(len(res)):
            users.append({'id' : res[i][0], 'firstname' : res[i][1], 'lastname' : res[i][2], 'email' : res[i][3]})

        return {'Update status': 'Success'}
        

class UserList(Resource):
    def get(self):
        return{'users': users}

api.add_resource(User, "/api/v1/users/<int:id>")
api.add_resource(AddUser, "/api/v1/users/add")
api.add_resource(DeleteUser, "/api/v1/users/delete")
api.add_resource(UpdateUser, "/api/v1/users/update")
api.add_resource(UserList, "/api/v1/users")


if __name__ == '__main__':
    app.run(port=4000, debug=True)


