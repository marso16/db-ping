from flask import Flask, send_from_directory, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone
import os

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route("/")
def ping():
    uri = "mongodb+srv://marcelino:311976Lh*C@cluster0.zt9d44u.mongodb.net/?appName=Cluster0"
    client = None

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000, server_api=ServerApi('1'))
        db = client.test

        client.admin.command('ping')
        
        ping_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success",
            "message": "MongoDB ping successful"
        }

        ping_history_collection = db.ping_history
        ping_history_collection.insert_one(ping_result) 
        ping_result.pop('_id', None)
        
        return jsonify(ping_result), 200

    except Exception as e:
        if client:
            try:
                db = client.test
                ping_history_collection = db.ping_history
                ping_result = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "failure",
                    "message": f"Ping failed: {e}"
                }
                ping_history_collection.insert_one(ping_result)
                
                ping_result.pop('_id', None)

            except Exception as log_e:
                return jsonify({
                    "status": "failure",
                    "message": f"Ping failed and could not save history: {e}",
                    "logging_error": str(log_e)
                }), 500

        return jsonify({
            "status": "failure",
            "message": f"Ping failed: {e}"
        }), 500

    finally:
        if client:
            client.close()
