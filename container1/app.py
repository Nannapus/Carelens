from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/relax", methods=["GET"])
def relax():
    response = requests.get("http://container2:5001/activity")
    activity = response.json().get("activity", "พักผ่อนตามใจคุณ")
    return jsonify({
        "message": "ถึงเวลาคลายเครียดแล้ว!",
        "suggested_activity": activity
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
