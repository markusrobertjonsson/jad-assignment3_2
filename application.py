# from os import environ
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from math import sqrt


application = Flask(__name__)
CORS(application)

# Get environment variables on server
# USERNAME = environ.get('RDS_USERNAME')
# PASSWORD = environ.get('RDS_PASSWORD')
# HOSTNAME = environ.get('RDS_HOSTNAME')
# PORT = environ.get('RDS_PORT')
# DBNAME = environ.get('RDS_DB_NAME')

# Syntax: dialect+driver://username:password@host:port/database
# application.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DBNAME}'

# In tests. Creates a file xydata_test.db in same dir as this file.
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///xydata_sqlite.db'

# To avoid warning. We do not use the Flask-SQLAlchemy event system, anyway.
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)


def _correlation_coefficient(x_list, y_list):
    n = len(x_list)
    x_mean = sum(x_list) / n
    y_mean = sum(y_list) / n
    xx_prod = 0
    yy_prod = 0
    xy_prod = 0
    for x, y in zip(x_list, y_list):
        xx_prod += (x - x_mean)**2
        yy_prod += (y - y_mean)**2
        xy_prod += (x - x_mean) * (y - y_mean)
    return xy_prod / sqrt(xx_prod * yy_prod)


class XYData3(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Since "id" is builtin
    description = db.Column(db.String(256), unique=False, nullable=True)
    owner = db.Column(db.String(80), unique=False, nullable=False)
    x = db.Column(db.String(500), unique=False)
    y = db.Column(db.String(500), unique=False)

    def correlation_coefficient(self, id):
        xydata = XYData3.query.get_or_404(id)
        x_str = xydata.x
        y_str = xydata.y
        x_list = x_str.split(',')
        y_list = y_str.split(',')
        return _correlation_coefficient(x_list, y_list)

    def __repr__(self):
        return f"<Data set {self.id}>"


db.create_all()


# @application.route('/info', methods=['GET'])
# def show_info():
#     return f"USERNAME={USERNAME}, PASSWORD={PASSWORD}, HOSTNAME={HOSTNAME}, PORT={PORT}, DBNAME={DBNAME}"


@application.route('/', methods=['GET'])
def index():
    xydatas = XYData3.query.order_by(XYData3.id).all()
    return render_template('index.html', xydatas=xydatas)


@application.route('/', methods=['POST'])
def add():
    description = request.form['description']
    owner = request.form['owner']
    x = request.form['x']
    y = request.form['y']
    new_data = XYData3(description=description, owner=owner, x=x, y=y)
    try:
        db.session.add(new_data)
        db.session.commit()
        return redirect('/')
    except Exception:
        return "There was an error adding your data set."


@application.route('/update/<int:id>', methods=['GET'])
def update_get(id):
    xydata = XYData3.query.get_or_404(id)
    return render_template('update.html', xydata=xydata)


@application.route('/update/<int:id>', methods=['POST'])
def update_post(id):
    # return "Here"
    xydata = XYData3.query.get_or_404(id)
    xydata.description = request.form['description']  # Keys are "name"s of input fields (not "id"s)
    xydata.owner = request.form['owner']
    xydata.x = request.form['x']
    xydata.y = request.form['y']
    try:
        db.session.commit()
        return redirect('/')
    except Exception:
        return "There was an error updating your task."


@application.route('/delete/<int:id>')
def delete(id):
    xydata_to_delete = XYData3.query.get_or_404(id)
    try:
        db.session.delete(xydata_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception:
        return "There was a problem deleting that data."


# Not needed if we start with "flask run" (or "python -m flask run")
if __name__ == '__main__':
    # application.debug = True

    # Start Flask app
    application.run()


# def create_app(test_config=None):
#     """
#     Application factory.
#     Flask will automatically detect the factory if it is called create_app or make_app.
#     To pass arguments to the factory, use
#     export FLASK_APP="markusapp:create_app('dev')"
#     """

#     app = Flask(__name__, instance_relative_config=True)
#     CORS(app)

#     # # Get environment variables on server
#     # USERNAME = environ.get('RDS_USERNAME')
#     # PASSWORD = environ.get('RDS_PASSWORD')
#     # HOSTNAME = environ.get('RDS_HOSTNAME')
#     # PORT = environ.get('RDS_PORT')
#     # DBNAME = environ.get('RDS_DB_NAME')

#     # Syntax: dialect+driver://username:password@host:port/database
#     # application.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DBNAME}'

#     # In tests. Creates a file xydata_test.db in same dir as this file.
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///xydata_sqlite.db'

#     # To avoid warning. We do not use the Flask-SQLAlchemy event system, anyway.
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db = SQLAlchemy(app)

#     # Create and configure the app
#     app.config.from_mapping(
#         SECRET_KEY='dev',  # os.urandom(16) will give a random string
#         DATABASE=os.path.join(app.instance_path, 'markusapp.sqlite'),
#     )

#     if test_config is None:
#         # Load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # Load the test config if passed in
#         app.config.from_mapping(test_config)

#     # Ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     # A simple page that says hello
#     @app.route('/hello')
#     def hello():
#         return 'Hello, World!'

#     return app
