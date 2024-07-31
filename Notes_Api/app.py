from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import load_config


config = load_config()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/{3}'.format(config['user'], config['password'], config['host'], config['database'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    '''Maps a Python object to the User table in Postgres database'''
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    profession = db.Column(db.String(50), nullable=False)

    def json(self):
        '''Constructs a json object of a user instance
        Return:
            user (dict) - Python dict representation of a user object
        '''
        return {"id": self.id, "username": self.username, "profession": self.profession}


@app.route("/api/v1/test", methods=["GET"])
def test_route():
    return make_response(jsonify({"message": "test route is working"}), 200)


@app.route("/api/v1/users", methods=["GET"])
def get_all_users():
    try:
        users = User.query.all()
        return make_response(jsonify({
            "total": len(users),
            "users": [user.json() for user in users]
            }), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        user = User(username=data["username"], profession=data["profession"])
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"message": "user created successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"message": str(e.message)}), 500)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
