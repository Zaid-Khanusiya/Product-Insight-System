from flask import request
from flask_restful import Resource
import json
from utils import *
from models import *
from prompts import *
import uuid

GOOGLE_LLM_MODEL = "gemini-2.5-flash"

sentence_transformer_model, faiss_index = load_model_and_fiass_index()

class Home(Resource):
    def get(self):
        return "This is home page!"


class SyncEmbeddings(Resource):
    def get(self):
        all_products = Products.query.all()

        db_items_list = []
        for item in all_products:
            db_items_list.append({'id':item.id})

        with open('products.json','r') as f:
            json_products = json.load(f)

        json_items_list = []
        for product in json_products:
            json_items_list.append({'id':product['id']})

        if db_items_list != json_items_list:
            print("UPDATE/SYNC NEEDED!")
            products = []
            for item in all_products:
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



class ExplainFeatures(Resource):
    def post(self):
        json_data = request.get_json()
        user_prompt = json_data.get("user_prompt")
        user_id = json_data.get("user_id")

        model_prompt, chat_id = create_chat_prompt_with_context(user_id=user_id,chat_type='explain-features',user_prompt=user_prompt)

        response = gc_client.models.generate_content(
            model=GOOGLE_LLM_MODEL,
            contents=model_prompt
        )

        # chat_id = uuid.uuid4().hex[:12]
        add_chat_history_list = []
        add_chat_history_list.append({
            'chat_id': chat_id,
            'user_id': user_id,
            'chat_type': 'explain-features',
            'message': user_prompt,
            'entity_type': 'user'
        })
        add_chat_history_list.append({
            'chat_id': chat_id,
            'user_id': user_id,
            'chat_type': 'explain-features',
            'message': response.text,
            'entity_type': 'system'
        })
        # print("cid "+chat_id,"uid ",user_id)
        add_chat_to_db(add_chat_history_list)

        return response.text


class CompareProducts(Resource):
    def post(self):
        json_data = request.get_json()
        user_prompt = json_data.get("user_prompt")
        user_id = json_data.get("user_id")

        model_prompt, chat_id = create_chat_prompt_with_context(user_id=user_id,user_prompt=user_prompt,chat_type='compare-products')
        
        # print(model_prompt)
        
        response = gc_client.models.generate_content(
            model=GOOGLE_LLM_MODEL,
            contents=model_prompt
        )

        add_chat_history_list = []
        add_chat_history_list.append({
            'chat_id': chat_id,
            'user_id': user_id,
            'chat_type': 'compare-products',
            'message': user_prompt,
            'entity_type': 'user'
        })
        add_chat_history_list.append({
            'chat_id': chat_id,
            'user_id': user_id,
            'chat_type': 'compare-products',
            'message': response.text,
            'entity_type': 'system'
        })
        add_chat_to_db(add_chat_history_list)

        return response.text

class GetQuotation(Resource):
    def post(self):
        json_data = request.get_json()
        user_prompt = json_data.get("user_prompt")
        user_id = json_data.get("user_id")

        model_prompt, chat_id = create_chat_prompt_with_context(user_id=user_id,user_prompt=user_prompt,chat_type='get-quotation')

        # print(model_prompt)
        
        response = gc_client.models.generate_content(
            model=GOOGLE_LLM_MODEL,
            contents=model_prompt
        )

        add_chat_history_list = []
        add_chat_history_list.append({
            'chat_id': chat_id,
            'user_id': user_id,
            'chat_type': 'get-quotation',
            'message': user_prompt,
            'entity_type': 'user'
        })
        add_chat_history_list.append({
            'chat_id': chat_id,
            'user_id': user_id,
            'chat_type': 'get-quotation',
            'message': response.text,
            'entity_type': 'system'
        })
        add_chat_to_db(add_chat_history_list)

        return response.text

class GetSpecs(Resource):
    def post(self):
        json_data = request.get_json()
        user_prompt = json_data.get("user_prompt")
        user_id = json_data.get("user_id")

        model_prompt, chat_id = create_chat_prompt_with_context(user_id=user_id,user_prompt=user_prompt,chat_type='get-specs')

        # print(model_prompt)
        
        response = gc_client.models.generate_content(
            model=GOOGLE_LLM_MODEL,
            contents=model_prompt
        )

        add_chat_history_list = []
        add_chat_history_list.append({
            'chat_id': chat_id,
            'user_id': user_id,
            'chat_type': 'get-specs',
            'message': user_prompt,
            'entity_type': 'user'
        })
        add_chat_history_list.append({
            'chat_id': chat_id,
            'user_id': user_id,
            'chat_type': 'get-specs',
            'message': response.text,
            'entity_type': 'system'
        })
        add_chat_to_db(add_chat_history_list)
        # print(response)
        return response.text

class SummariseReviews(Resource):
    def post(self):
        json_data = request.get_json()
        user_prompt = json_data.get("user_prompt")
        user_id = json_data.get("user_id")
        # product_id = json_data.get("product_id")

        user_query_vector = sentence_transformer_model.encode([user_prompt]).astype("float32")
        distances, indices = faiss_index.search(user_query_vector, 20)
        
        with open("products.json", "r") as f:
            products = json.load(f)

        top_products = [products[i] for i in indices[0]]

        product_id = gc_client.models.generate_content(
            model=GOOGLE_LLM_MODEL,
            contents=f"Products:{top_products}\n\nYou are provided with various products and you have to strictly **only output the product_id** of 1 product that matches user prompt and nothing else. Ex: 10\n\nUser prompt:{user_prompt}"
        ).text
        print(product_id)

        reviews = ProductReviews.query.filter_by(product_id=product_id).all()
        review_list = []
        for review in reviews:
            review_list.append({
                'reviewer_name': review.reviewer_name,
                'rating': review.rating,
                'review_text': review.review_text,
                'review_date': review.review_date,
            })
        
        if len(review_list) == 0:
            review_list = ["No reviews are available for this product, Become first reviewer of this product!"]

        chat_context = ChatHistory.query.filter_by(user_id=user_id,chat_type='summarise-reviews').all()
        if chat_context:
            context_list = []
            for context in chat_context:
                context_list.append({
                    'entity_type': context.entity_type,
                    'message': context.message
                })
            chat_id = context.chat_id
            print("OLD_CHAT_ID::::::::",chat_id)
            model_prompt = summarise_review_model_prompt(context=context_list,reviews=review_list,user_prompt=user_prompt)
        else:
            context_list = []
            chat_id = uuid.uuid4().hex[:12]
            model_prompt = summarise_review_model_prompt(context=context_list,reviews=review_list,user_prompt=user_prompt)
            print("NEW_CHAT_ID::::::::",chat_id)
        
        print(model_prompt)

        response = gc_client.models.generate_content(
            model=GOOGLE_LLM_MODEL,
            contents=model_prompt
        )

        add_chat_history_list = []
        add_chat_history_list.append({
            'chat_id': chat_id,
            'user_id': user_id,
            'chat_type': 'summarise-reviews',
            'message': user_prompt,
            'entity_type': 'user'
        })
        add_chat_history_list.append({
            'chat_id': chat_id,
            'user_id': user_id,
            'chat_type': 'summarise-reviews',
            'message': response.text,
            'entity_type': 'system'
        })
        add_chat_to_db(add_chat_history_list)

        return response.text


def create_chat_prompt_with_context(user_prompt,user_id,chat_type):
    user_query_vector = sentence_transformer_model.encode([user_prompt]).astype("float32")
    distances, indices = faiss_index.search(user_query_vector, 20)
    
    with open("products.json", "r") as f:
        products = json.load(f)
    top_products = [products[i] for i in indices[0]]
    # print(top_products)
    chat_context = ChatHistory.query.filter_by(user_id=user_id,chat_type=chat_type).all()
    if chat_context:
        context_list = []
        for context in chat_context:
            context_list.append({
                'entity_type': context.entity_type,
                'message': context.message
            })
        chat_id = context.chat_id
        print("OLD_CHAT_ID::::::::",chat_id)

        if chat_type == 'explain-features':
            model_prompt = explain_features_model_prompt(context=context_list,products=top_products,user_prompt=user_prompt)
        elif chat_type == 'get-specs':
            model_prompt = get_specs_model_prompt(context=context_list,products=top_products,user_prompt=user_prompt)
        elif chat_type == 'get-quotation':
            model_prompt = get_quotation_model_prompt(context=context_list,products=top_products,user_prompt=user_prompt)
        elif chat_type == 'compare-products':
            model_prompt = compare_products_model_prompt(context=context_list,products=top_products,user_prompt=user_prompt)
        else:
            model_prompt = ''

    else:
        context_list = ['There is no previous chat context available, this is a new chat!']
        chat_id = uuid.uuid4().hex[:12]

        if chat_type == 'explain-features':
            model_prompt = explain_features_model_prompt(context=context_list,products=top_products,user_prompt=user_prompt)
        elif chat_type == 'get-specs':
            model_prompt = get_specs_model_prompt(context=context_list,products=top_products,user_prompt=user_prompt)
        elif chat_type == 'get-quotation':
            model_prompt = get_quotation_model_prompt(context=context_list,products=top_products,user_prompt=user_prompt)
        elif chat_type == 'compare-products':
            model_prompt = compare_products_model_prompt(context=context_list,products=top_products,user_prompt=user_prompt)
        else:
            model_prompt = ''

        print("NEW_CHAT_ID::::::::",chat_id)
        
        return model_prompt, chat_id