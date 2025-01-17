from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://tutran:M00nd0g-@cluster0.kkp4z.mongodb.net/"

client = MongoClient(CONNECTION_STRING)
db_realestate = client['RealEstate']