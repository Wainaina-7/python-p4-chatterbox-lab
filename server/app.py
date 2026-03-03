from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

with app.app_context():
    db.create_all()
 # Seed one message if database is empty
    if not Message.query.first():
        seed_message = Message(
            body="Initial message",
            username="System"
        )
        db.session.add(seed_message)
        db.session.commit()
# GET all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([message.to_dict() for message in messages]), 200


# POST create message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    new_message = Message(
        body=data['body'],
        username=data['username']
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201


# PATCH update message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)

    data = request.get_json()

    if "body" in data:
        message.body = data["body"]

    db.session.commit()

    return jsonify(message.to_dict()), 200


# DELETE message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)

    if message:
        db.session.delete(message)
        db.session.commit()

    # Ensure at least one message always exists
    if not Message.query.first():
        seed = Message(
            body="Seed message",
            username="System"
        )
        db.session.add(seed)
        db.session.commit()

    return {}, 204


if __name__ == '__main__':
    app.run(port=5555)