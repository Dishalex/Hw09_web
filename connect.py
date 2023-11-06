from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read('./config.ini')
DB = 'DB_Hw09'

mongo_user = config.get(DB, 'user')
mongodb_pass = config.get(DB, 'pass')
db_name = config.get(DB, 'db_name')
domain = config.get(DB, 'domain')

# connect to cluster on AtlasDB with connection string
connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)


# NEXT CODE FOR TESTING CONNECTION


# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# uri = f'mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority'

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
