from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone

app = Flask(__name__)

@app.route("/")
def ping():
    uri = "mongodb+srv://marcelino:311976Lh*C@cluster0.zt9d44u.mongodb.net/?tls=true&appName=Cluster0"
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000, server_api=ServerApi('1'))
        client.admin.command('ping')
        ping_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success",
            "message": "MongoDB ping successful"
        }
        return jsonify(ping_result), 200
    except Exception as e:
        return jsonify({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "failure",
            "message": f"Ping failed: {e}"
        }), 500
    finally:
        if 'client' in locals():
            client.close()
