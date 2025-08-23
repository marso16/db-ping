from flask import Flask
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from datetime import datetime, timezone

# Vercel will automatically use this 'app' object as the serverless function.
app = Flask(__name__)

@app.route("/")
def ping():
    # Retrieve the MongoDB URI from environment variables
    uri = os.getenv("MONGODB_URI")
    client = None
    
    # Handle cases where the URI is not set
    if not uri:
        return "❌ MONGODB_URI environment variable not set.", 500

    try:
        # Connect to MongoDB
        client = MongoClient(uri, serverSelectionTimeoutMS=5000, server_api=ServerApi('1'))
        db = client.test

        # Ping the MongoDB database
        client.admin.command('ping')
        
        ping_history_collection = db.ping_history
        
        ping_result = {
            "timestamp": datetime.now(timezone.utc),
            "status": "success",
            "message": "MongoDB ping successful"
        }
        
        # Save the successful ping result to the database
        ping_history_collection.insert_one(ping_result)
        
        return "✅ MongoDB ping successful and history saved!", 200
        
    except Exception as e:
        # If the ping fails, log the failure to the database if possible
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
                # Handle case where logging the failure also fails
                return f"❌ Ping failed and could not save history: {e}, Logging failed: {log_e}", 500
        
        return f"❌ Ping failed: {e}", 500
        
    finally:
        # Close the MongoDB connection
        if client:
            client.close()

# The `if __name__ == "__main__":` block is not needed in a serverless environment
# because Vercel handles the running of the application.
