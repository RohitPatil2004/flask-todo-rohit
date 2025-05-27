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

@app.route('/api',methods=['GET'])
def get_data():
    try:
        with open('data.json') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error":"Data file not found"}),404

@app.route('/',methods=['GET','POST'])
def form():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        try:
            collection.insert_one({"name":name,"email":email})
            return redirect(url_for('success'))
        except PyMongoError as e:
            error = f"An error occurred: {str(e)}"
        return render_template('form.html',error=error)

@app.route('/success')
def success():
    return render_template('success.html')
