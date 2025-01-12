from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Configure the JWT secret key
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key in production
jwt = JWTManager(app)

# Connect to MongoDB
client = MongoClient("mongodb+srv://noumana:Turing!!@cluster0.xydhc.mongodb.net/")  # Replace with your MongoDB URI
db = client['watchlist_service']
watchlist_collection = db['watchlists']

# Add a new item to the watchlist
@app.route('/watchlist', methods=['POST'])
@jwt_required()
def add_to_watchlist():
    current_user = get_jwt_identity()
    data = request.json

    video_id = data.get('video_id')
    title = data.get('title')

    if not video_id or not title:
        return jsonify({'error': 'Video ID and title are required'}), 400

    watchlist_item = {
        'user': current_user,
        'video_id': video_id,
        'title': title
    }
    watchlist_collection.insert_one(watchlist_item)
    return jsonify({'message': 'Video added to watchlist'}), 201

# Get all watchlist items for the current user
@app.route('/watchlist', methods=['GET'])
@jwt_required()
def get_watchlist():
    current_user = get_jwt_identity()
    items = watchlist_collection.find({'user': current_user})
    watchlist = [{'id': str(item['_id']), 'video_id': item['video_id'], 'title': item['title']} for item in items]
    return jsonify(watchlist), 200

# Remove an item from the watchlist
@app.route('/watchlist/<item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_watchlist(item_id):
    current_user = get_jwt_identity()
    result = watchlist_collection.delete_one({'_id': ObjectId(item_id), 'user': current_user})

    if result.deleted_count == 0:
        return jsonify({'error': 'Item not found'}), 404

    return jsonify({'message': 'Item removed from watchlist'}), 200

# Test endpoint
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'Watchlist Service is running'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
