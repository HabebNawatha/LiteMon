from flask import Flask
from litemon import monitor, configure_client


app = Flask(__name__)

configure_client(server_url="http://127.0.0.1:8000", push_interval=2)

@monitor
def greet():
    print("Hello! Welcome to the server.")
    return "Hello! Welcome to the server."

@monitor
def bye():
    print("Goodbye! See you soon.")
    return "Goodbye! See you soon."

@monitor
def divide():
    print("dividing by 0")
    return 3/0

@app.route('/greet', methods=['GET'])
def greet_route():
    return greet()

@app.route('/bye', methods=['GET'])
def bye_route():
    return bye()

@app.route('/divide', methods=["GET"])
def divide_route():
    return divide()

if __name__ == '__main__':
    # Start LiteMon client (push metrics every 3s)
    app.run(debug=True, port=5050)
