from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This field cannot be left blank!')

    @jwt_required()
    def get(self, name):
        if item := ItemModel.find_by_name(name):
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists.'.format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An exception occured inserting the item.'}, 500

        return item.json(), 201

    def delete(self, name):
        if item := ItemModel.find_by_name(name):
            item.delete_from_db()

        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if not item:
             item = ItemModel(name, **data)
        else:
             item.price = data['price']

        item.save_to_db()
        return item.json()
    

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
