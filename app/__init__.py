from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from app.config import Config
import firebase_admin
from firebase_admin import credentials, firestore
import os

bcrypt = Bcrypt()
db = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensões
    CORS(app)
    bcrypt.init_app(app)
    
    # Inicializar Firebase
    init_firebase()
    
    # Registrar blueprints
    from app.auth.routes import auth_bp
    from app.api.routes import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Rota principal
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    
    return app

def init_firebase():
    global db
    try:
        # Verificar se o Firebase já foi inicializado
        if not firebase_admin._apps:
            # Para desenvolvimento, usar credenciais de exemplo
            # Em produção, usar arquivo de credenciais real
            if os.path.exists('firebase-credentials.json'):
                cred = credentials.Certificate('firebase-credentials.json')
                firebase_admin.initialize_app(cred)
                db = firestore.client()
            else:
                print("Arquivo de credenciais do Firebase não encontrado.")
                print("Usando simulador local do Firestore para desenvolvimento.")
                # Usar simulador local para desenvolvimento
                from app.firestore_simulator import get_mock_firestore_client
                db = get_mock_firestore_client()
        else:
            db = firestore.client()
    except Exception as e:
        print(f"Erro ao inicializar Firebase: {e}")
        print("Usando simulador local do Firestore para desenvolvimento.")
        # Para desenvolvimento, usar simulador local
        from app.firestore_simulator import get_mock_firestore_client
        db = get_mock_firestore_client()

def get_db():
    return db
