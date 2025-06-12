from flask import Flask
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from flask_login import LoginManager
=======
from flask_login import LoginManager # Importa o gerenciador de login
from werkzeug.security import generate_password_hash # Para hashing de senhas

>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8

# Inicializa a aplicação Flask
app = Flask(__name__, template_folder='templates')
<<<<<<< HEAD

# Configurações básicas da aplicação
app.config['SECRET_KEY'] = '1072e926d71a094f491476e564a2443f'
=======
app.config['SECRET_KEY'] = '1072e926d71a094f491476e564a2443f' # **Mantenha esta chave secreta e forte!**

>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:201611@localhost:3306/MEDIFLOW'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)

<<<<<<< HEAD
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
=======
# --- Configuração do Flask-Login ---
login_manager = LoginManager() # Cria uma instância do LoginManager
login_manager.init_app(app)    # Inicializa o Flask-Login com seu aplicativo Flask
login_manager.login_view = 'login' # Rota para onde o usuário será redirecionado se não estiver logado
login_manager.login_message_category = 'alert-info' # Categoria da mensagem flash exibida ao ser redirecionado para o login
login_manager.login_message = 'Por favor, faça login para acessar esta página.' # Mensagem padrão do Flask-Login

# Importa o modelo Funcionarios (necessário para o user_loader)
# A importação deve vir após a inicialização de 'db' para evitar erros de importação circular
from MediFlow.models import Funcionarios, Perfis 

@login_manager.user_loader
def load_user(user_id):
    """
    Função obrigatória para o Flask-Login.
    Ela carrega um objeto usuário da ID de usuário armazenada na sessão.
    """
    return Funcionarios.query.get(int(user_id))

# A importação das rotas deve vir por último para garantir que 'app' e 'db' estejam inicializados
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
from MediFlow import routes

