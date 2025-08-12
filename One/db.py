from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Pavan891:Pavans@cluster0.pdzpbto.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"❌ Connection error: {e}")

# ✅ Correct Database: QA
db = client["QA"]

# ✅ Correct Collection: RegDetails
reg_collection = db["RegDetails"]


# ✅ Correct Collection: storedata
saved_collection = db["PDFDATA"]

# answer saved data 
saved_useranswer = db["Answers"]

report_collection = db["Reports"]



