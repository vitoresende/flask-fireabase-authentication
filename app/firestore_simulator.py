"""
Simulador do Firestore para desenvolvimento local
Este módulo simula as operações básicas do Firestore quando não há conexão real
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List

class MockDocument:
    def __init__(self, doc_id: str, data: Dict[str, Any]):
        self.id = doc_id
        self._data = data
    
    def to_dict(self) -> Dict[str, Any]:
        return self._data.copy()
    
    @property
    def exists(self) -> bool:
        return bool(self._data)

class MockQuery:
    def __init__(self, collection_name: str, storage: Dict[str, Any]):
        self.collection_name = collection_name
        self.storage = storage
        self._filters = []
        self._limit = None
    
    def where(self, field: str, operator: str, value: Any):
        self._filters.append((field, operator, value))
        return self
    
    def limit(self, count: int):
        self._limit = count
        return self
    
    def stream(self):
        collection_data = self.storage.get(self.collection_name, {})
        results = []
        
        for doc_id, doc_data in collection_data.items():
            # Aplicar filtros
            match = True
            for field, operator, value in self._filters:
                if operator == '==':
                    if doc_data.get(field) != value:
                        match = False
                        break
                # Adicionar outros operadores conforme necessário
            
            if match:
                results.append(MockDocument(doc_id, doc_data))
                
                # Aplicar limite
                if self._limit and len(results) >= self._limit:
                    break
        
        return results

class MockDocumentReference:
    def __init__(self, collection_name: str, doc_id: str, storage: Dict[str, Any]):
        self.collection_name = collection_name
        self.doc_id = doc_id
        self.storage = storage
    
    def set(self, data: Dict[str, Any]):
        if self.collection_name not in self.storage:
            self.storage[self.collection_name] = {}
        
        # Converter datetime para string para serialização
        serializable_data = self._make_serializable(data)
        self.storage[self.collection_name][self.doc_id] = serializable_data
        self._save_to_file()
    
    def get(self):
        collection_data = self.storage.get(self.collection_name, {})
        doc_data = collection_data.get(self.doc_id, {})
        return MockDocument(self.doc_id, doc_data)
    
    def _make_serializable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Converter objetos não serializáveis para formatos JSON"""
        result = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                result[key] = self._make_serializable(value)
            else:
                result[key] = value
        return result
    
    def _save_to_file(self):
        """Salvar dados no arquivo local"""
        try:
            with open(self.storage['_file_path'], 'w') as f:
                # Criar uma cópia dos dados sem a chave especial '_file_path'
                data_to_save = {k: v for k, v in self.storage.items() if k != '_file_path'}
                json.dump(data_to_save, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados locais: {e}")

class MockCollection:
    def __init__(self, collection_name: str, storage: Dict[str, Any]):
        self.collection_name = collection_name
        self.storage = storage
    
    def document(self, doc_id: str):
        return MockDocumentReference(self.collection_name, doc_id, self.storage)
    
    def where(self, field: str, operator: str, value: Any):
        return MockQuery(self.collection_name, self.storage).where(field, operator, value)

class MockFirestoreClient:
    def __init__(self, data_file: str = 'firestore_local_data.json'):
        self.data_file = data_file
        self.storage = self._load_from_file()
        self.storage['_file_path'] = data_file
    
    def _load_from_file(self) -> Dict[str, Any]:
        """Carregar dados do arquivo local"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar dados locais: {e}")
        
        return {}
    
    def collection(self, collection_name: str):
        return MockCollection(collection_name, self.storage)

# Instância global do simulador
_mock_client = None

def get_mock_firestore_client():
    """Obter instância do cliente simulado do Firestore"""
    global _mock_client
    if _mock_client is None:
        _mock_client = MockFirestoreClient()
    return _mock_client
