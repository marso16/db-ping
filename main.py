from flask import Flask
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from datetime import datetime, timezone

app = Flask(__name__)

@app.route("/ping")
def ping():
    uri = os.getenv("MONGO_URI")
    client = None
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000, server_api=ServerApi('1'))
        db = client.test

        client.admin.command('ping')
        
        ping_history_collection = db.ping_history
        
        ping_result = {
            "timestamp": datetime.now(timezone.utc),
            "status": "success",
            "message": "MongoDB ping successful"
        }
        
        ping_history_collection.insert_one(ping_result)
        
        return "✅ MongoDB ping successful and history saved!", 200
        
    except Exception as e:
        if client:
            try:
                db = client.test
                ping_history_collection = db.ping_history
                ping_result = {
                    "timestamp": datetime.now(timezone.utc),
                    "status": "failure",
                    "message": f"Ping failed: {e}"
                }
                ping_history_collection.insert_one(ping_result)
            except Exception as log_e:
                return f"❌ Ping failed and could not save history: {e}, Logging failed: {log_e}", 500
        
        return f"❌ Ping failed: {e}", 500
        
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)