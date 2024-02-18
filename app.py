# app.py


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
# Configure MySQL database URI
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://username:password@hostname/database_name"
)
app.config["SECRET_KEY"] = "your_secret_key"
# Set this to True if you want to track modifications to objects and emit signals
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
api = Api(app)
CORS(app)


# Define models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship("Comment", backref="post", lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)


# Flask-Login configuration
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Routes
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return jsonify({"message": "Login successful"})
        return jsonify({"message": "Invalid credentials"}), 401


class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return jsonify({"message": "Logout successful"})


class PostResource(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        content = data.get("content")
        if content:
            post = Post(user_id=current_user.id, content=content)
            db.session.add(post)
            db.session.commit()
            return jsonify({"message": "Post created successfully"})
        return jsonify({"message": "Content is required"}), 400


class LikePost(Resource):
    @login_required
    def post(self, post_id):
        post = Post.query.get(post_id)
        if post:
            post.likes += 1
            db.session.commit()
            return jsonify({"message": "Post liked successfully"})
        return jsonify({"message": "Post not found"}), 404


class CommentResource(Resource):
    @login_required
    def post(self, post_id):
        data = request.get_json()
        content = data.get("content")
        post = Post.query.get(post_id)
        if post and content:
            comment = Comment(post_id=post_id, content=content)
            db.session.add(comment)
            db.session.commit()
            return jsonify({"message": "Comment added successfully"})
        return jsonify({"message": "Post not found or content is required"}), 404


class Posts(Resource):
    def get(self):
        posts = Post.query.all()
        return jsonify(
            [
                {"id": post.id, "content": post.content, "likes": post.likes}
                for post in posts
            ]
        )


# API routes
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(PostResource, "/posts")
api.add_resource(LikePost, "/posts/<int:post_id>/like")
api.add_resource(CommentResource, "/posts/<int:post_id>/comment")
api.add_resource(Posts, "/posts")

if __name__ == "__main__":
    app.run(debug=True)
