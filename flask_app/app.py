from flask import Flask, request, jsonify, abort
from models import Item
from database import db, DATABASE_URL, engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 20,
    'max_overflow': 30,
    'pool_pre_ping': True,
    'pool_recycle': 3600,
    'pool_timeout': 60
}

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/items/", methods=["POST"])
def create_item():
    data = request.get_json()
    item = Item(**data)
    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.id, **data})

@app.route("/items/", methods=["GET"])
def list_items():
    items = Item.query.all()
    return jsonify([{ "id": i.id, "name": i.name, "description": i.description, "price": i.price, "in_stock": i.in_stock } for i in items])

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404)
    return jsonify({ "id": item.id, "name": item.name, "description": item.description, "price": item.price, "in_stock": item.in_stock })

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404)
    data = request.get_json()
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return jsonify({ "id": item.id, **data })

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"ok": True})
