# from flask import Flask

# app = Flask(__name__)


# @app.route("/")
# def home():
#     return "Hòa tệ như con chó :)"


# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template

web = Flask(
    __name__, template_folder='./management/templates')


@web.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    web.run(debug=True)
