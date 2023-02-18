import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import ItemModel
from schema import ItemSchema, UpdateItemSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

ItemBluePrint = Blueprint("item", __name__, description= "operations on items")

@ItemBluePrint.route('/item/<string:item_id>')
class Item(MethodView):
    @ItemBluePrint.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "item deleted"}


    @ItemBluePrint.arguments(UpdateItemSchema)
    @ItemBluePrint.response(200, ItemSchema)
    def put(self, item_id, item_data):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["price"]
            item.price = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
    
        db.session.add(item)
        db.session.commit()
        return item

@ItemBluePrint.route("/item")
class StoreList(MethodView):
    @ItemBluePrint.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @ItemBluePrint.arguments(ItemSchema)
    @ItemBluePrint.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An item with that name already exists.")

        except SQLAlchemyError:
            abort(500, message="an error occured while creating a store.")
        return item, 201