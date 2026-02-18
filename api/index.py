from flask import Flask, jsonify, send_from_directory
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone
import certifi
import os

app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )

@app.route("/")
def ping():
    uri = (
        "mongodb+srv://marcelino:311976Lh*C@cluster0.zt9d44u.mongodb.net/"
        "?appName=Cluster0"
        "&tls=true"
        "&tlsAllowInvalidCertificates=false"
        f"&tlsCAFile={certifi.where()}"
    )

    if not uri:
        return jsonify({
            "status": "failure",
            "message": "MONGO_URI environment variable not set"
        }), 500

    try:
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            server_api=ServerApi("1"),
            tls=True,
            tlsCAFile=certifi.where()
        )
        client.admin.command("ping")
        db = client["test"]
        collection = db["ping_history"]

        ping_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success"
        }

        collection.insert_one(ping_result)

        return jsonify({
            "timestamp": ping_result["timestamp"],
            "status": "success",
            "message": "MongoDB ping successful and logged"
        }), 200

    except Exception as e:
        print("MongoDB error:", e)

        return jsonify({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "failure",
            "message": str(e)
        }), 500

    finally:
        if "client" in locals():
            client.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
