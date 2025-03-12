# server.py
from app import app

"""
To start server run the command: python server.py
"""

HOST = "0.0.0.0"
PORT = 5000

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)