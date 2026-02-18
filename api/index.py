from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone
import certifi
import ssl
import os

app = Flask(__name__)

@app.route("/")
def ping():
    uri = "mongodb+srv://marcelino:311976Lh*C@cluster0.zt9d44u.mongodb.net/?appName=Cluster0"

    try:
        # Force TLS 1.2 and use certifi CA bundle
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            server_api=ServerApi("1"),
            tls=True,
            tlsCAFile=certifi.where(),
            tlsVersion=ssl.TLSVersion.TLSv1_2
        )

        # Ping the database
        client.admin.command("ping")

        # Record result (optional: insert into DB if you want)
        ping_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success",
            "message": "MongoDB ping successful"
        }

        return jsonify(ping_result), 200

    except Exception as e:
        # Log failure locally (safer than logging to MongoDB if connection failed)
        print(f"MongoDB ping failed: {e}")
        ping_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "failure",
            "message": f"Ping failed: {e}"
        }
        return jsonify(ping_result), 500

    finally:
        if "client" in locals():
            client.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
