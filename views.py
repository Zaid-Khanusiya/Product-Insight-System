from flask import request
from flask_restful import Resource
import json
from utils import *
from models import *

class Home(Resource):
    def get(self):
        return "This is home page!"


class SyncEmbeddings(Resource):
    def get(self):
        items = Products.query.all()

        db_items_list = []
        for item in items:
            db_items_list.append({'id':item.id})

        with open('products.json','r') as f:
            json_products = json.load(f)

        json_items_list = []
        for product in json_products:
            json_items_list.append({'id':product['id']})

        if db_items_list != json_items_list:
            print("UPDATE/SYNC NEEDED!")
            products = []
            for item in items:
                products.append({
                    'id': item.id,
                    'product_name': item.product_name,
                    'category': item.category,
                    'brand': item.brand,
                    'description': item.description,
                    'specifications': item.specifications,
                    'features': item.features,
                    'price': item.price,
                    'stock': item.stock,
                    'warranty': item.warranty,
                })
            sync_embeddings(products=products)
            return {'msg': 'Found new products in DB, Sync done with embeddings!'}

        return {'msg': 'No new products found in DB, Embeddings are same!'}