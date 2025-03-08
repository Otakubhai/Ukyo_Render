"""
This is an optional helper file for Render.com to set up the web service
with health checks. This is not essential for the bot's functionality.
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def health_check():
    """Simple health check endpoint for Render.com"""
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
