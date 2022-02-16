from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return shane_c_demo()

def shane_c_demo():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run()
