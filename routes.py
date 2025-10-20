from views import *
from app import api, app

api.add_resource(Home, '/')
api.add_resource(SyncEmbeddings, '/sync-embeddings')
api.add_resource(ExplainFeatures, '/explain-features')
api.add_resource(CompareProducts, '/compare-products')
api.add_resource(GetQuotation, '/get-quotation')
api.add_resource(GetSpecs, '/get-specs')
api.add_resource(SummariseReviews, '/summarise-reviews')