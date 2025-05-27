from flask import Flask, jsonify, request, render_template, redirect, url_for
import json
import pymongo
from pymongo.errors import PyMongoError
import os

app = Flask(__name__)

# Mango Atlas configuration
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client['yd']
collection = db['submissions']

@app.route('/submittodoitem', methods=['POST'])
def submit_item():
    data = request.get_json()
    item_name = data.get('itemName')
    item_desc = data.get('itemDescription')
    db.todos.insert_one({"name":item_name,"description":item_desc})
    return jsonify({"message":"Item Added"}),201