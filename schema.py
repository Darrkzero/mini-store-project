from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id= fields.Str(dump_only=True)
    price = fields.Float(required=True)
    name = fields.Str(required=True)

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class UpdateItemSchema(Schema):
    price = fields.Float()
    name = fields.Str()
    store_id = fields.Int()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True)
    stores = fields.Nested(PlainStoreSchema(), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema), dump_only = True)

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
