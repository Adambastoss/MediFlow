from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicializa a aplicação Flask
app = Flask(__name__, template_folder='templates')

# Configurações básicas da aplicação
app.config['SECRET_KEY'] = '1072e926d71a094f491476e564a2443f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:201611@localhost:3306/MEDIFLOW'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Configura o Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Nome da função que renderiza a tela de login
login_manager.login_message_category = 'alert-info'

# Importa modelos após inicializar o app e o db
from MediFlow.models import Funcionarios  # Certifique-se de que a estrutura está correta

# Callback para carregar o usuário logado
@login_manager.user_loader
def load_user(user_id):
    return Funcionarios.query.get(int(user_id))

# Importa as rotas após tudo estar configurado
from MediFlow import routes

