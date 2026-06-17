from flask import Flask  # type: ignore[import]

app = Flask(__name__)

from routes import *

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )