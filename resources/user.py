from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import UserModel
from passlib.hash import pbkdf2_sha256
from schema import UserSchema
from flask_jwt_extended import create_access_token


UserBluePrint = Blueprint("user", __name__, description= "operations on users")

@UserBluePrint.route("/register")
class UserRegister(MethodView):
    @UserBluePrint.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(401, "Username already exist")
        
        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()
        
        return {"message": "User Created Successfully!"}, 201
@UserBluePrint.route("/login")    
class Login(MethodView):
    @UserBluePrint.arguments(UserSchema)
    def post(self, user_data):
        user =  UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity= user.id)
            return {"access_token":access_token}
        
        abort(401, message="invalid password")


@UserBluePrint.route("/user/<int:user_id>")
class UserDetail(MethodView):
    @UserBluePrint.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()
        return {"message":"user successfully deleted"}

# @UserBluePrint.route("/user/<int:user_id>")
# class User(MethodView):
#     # Get user by id
#     @UserBluePrint.response(200, UserSchema)
#     def get(self, user_id):
#         user = UserModel.query.get_or_404(user_id)
#         return user


