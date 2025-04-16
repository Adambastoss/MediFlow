from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '1072e926d71a094f491476e564a2443f'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:201611@localhost:3306/MEDIFLOW'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Opcional: desabilita avisos

db = SQLAlchemy(app)


from MediFlow import routes
