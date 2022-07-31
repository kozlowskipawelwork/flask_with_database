from flask import Flask, jsonify, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)#database
ma = Marshmallow(app)

class Myapp(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(500))
    toppings = db.Column(db.String(500))
    crust = db.Column(db.String(500))


class MyAppSchema(ma.Schema):
    class Meta:
        fields = ('order_id','size','toppings','crust')

my_app_schema = MyAppSchema(many=True)

@app.route('/')
def hello_database():
    return 'hello database!'
#reads our table
@app.route('/order')
def get_order():
    entries = Myapp.query.all()
    result = my_app_schema.dump(entries)
    return jsonify(result)

#adds a new table(creates)
@app.route('/order',methods=["POST"])
def insert_order():
    req = request.get_json()
    order_id = req['order_id']
    size = req['size']
    toppings = req['toppings']
    crust = req['crust']
    new_entry = Myapp(order_id=order_id, size=size, toppings=toppings, crust=crust)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('get_order'))

#updates a table
@app.route('/order/<order_id>',methods=["PUT"])
def update_order(order_id):
    req = request.get_json()
    entry = Myapp.query.get(order_id)
    entry.size = req['size']
    entry.toppings = req['toppings']
    entry.crust = req['crust']
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('get_order'))

#deletes a table
@app.route('/order/<order_id>',methods=["DELETE"])
def remove_order(order_id):
    entry = Myapp.query.get_or_404(order_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('get_order'))

if __name__ == '__main__':
    db.create_all()
    app.run()