from datetime import datetime
from app import get_db
from flask_bcrypt import generate_password_hash, check_password_hash

class User:
    def __init__(self, uid=None, email=None, password_hash=None, google_id=None, 
                 name=None, created_at=None, has_password=False):
        self.uid = uid
        self.email = email
        self.password_hash = password_hash
        self.google_id = google_id
        self.name = name
        self.created_at = created_at or datetime.utcnow()
        self.has_password = has_password

    def to_dict(self):
        return {
            'uid': self.uid,
            'email': self.email,
            'password_hash': self.password_hash,
            'google_id': self.google_id,
            'name': self.name,
            'created_at': self.created_at,
            'has_password': self.has_password
        }

    @staticmethod
    def from_dict(data):
        return User(
            uid=data.get('uid'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            google_id=data.get('google_id'),
            name=data.get('name'),
            created_at=data.get('created_at'),
            has_password=data.get('has_password', False)
        )

    def save(self):
        """Salvar usuário no Firestore"""
        db = get_db()
        if db is None:
            return False
        
        try:
            user_ref = db.collection('users').document(self.uid)
            user_ref.set(self.to_dict())
            return True
        except Exception as e:
            print(f"Erro ao salvar usuário: {e}")
            return False

    @staticmethod
    def find_by_email(email):
        """Buscar usuário por email"""
        db = get_db()
        if db is None:
            return None
        
        try:
            users_ref = db.collection('users')
            query = users_ref.where('email', '==', email).limit(1)
            docs = query.stream()
            
            for doc in docs:
                data = doc.to_dict()
                data['uid'] = doc.id
                return User.from_dict(data)
            
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário por email: {e}")
            return None

    @staticmethod
    def find_by_uid(uid):
        """Buscar usuário por UID"""
        db = get_db()
        if db is None:
            return None
        
        try:
            user_ref = db.collection('users').document(uid)
            doc = user_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data['uid'] = doc.id
                return User.from_dict(data)
            
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário por UID: {e}")
            return None

    @staticmethod
    def find_by_google_id(google_id):
        """Buscar usuário por Google ID"""
        db = get_db()
        if db is None:
            return None
        
        try:
            users_ref = db.collection('users')
            query = users_ref.where('google_id', '==', google_id).limit(1)
            docs = query.stream()
            
            for doc in docs:
                data = doc.to_dict()
                data['uid'] = doc.id
                return User.from_dict(data)
            
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário por Google ID: {e}")
            return None

    def set_password(self, password):
        """Definir senha com hash"""
        self.password_hash = generate_password_hash(password).decode('utf-8')
        self.has_password = True

    def check_password(self, password):
        """Verificar senha"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def update_password(self, new_password):
        """Atualizar senha do usuário"""
        self.set_password(new_password)
        return self.save()
