import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel
from schema import StoreSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

StoreBluePrint = Blueprint("store", __name__, description= "operations on Stores")


@StoreBluePrint.route('/store/<string:store_id>')
class Store(MethodView):
    @jwt_required()
    @StoreBluePrint.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "store deleted"}

@StoreBluePrint.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @StoreBluePrint.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @StoreBluePrint.arguments(StoreSchema)
    @StoreBluePrint.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="an error occured while creating a store.")
        return store, 201


        # try:
        #     del stores[store_id]
        #     return {"message":"store deleted"}
        # except KeyError:
        #     return abort(404, message="store not found")


