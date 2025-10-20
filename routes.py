from views import *
from app import api, app

api.add_resource(Home, '/')
api.add_resource(SyncEmbeddings, '/sync-embeddings')