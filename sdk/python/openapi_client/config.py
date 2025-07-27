#!/usr/bin/env python3
"""
Configurazione semplificata per Maybind SDK
"""

import os
from pathlib import Path
from . import Configuration, ApiClient
from .api.default_api import DefaultApi


class MaybindConfig:
    """Classe per gestire la configurazione dell'SDK Maybind"""
    
    def __init__(self, api_key=None, host=None, config_file=None):
        """
        Inizializza la configurazione
        
        Args:
            api_key: API key diretta (opzionale)
            host: Host API (opzionale)
            config_file: File di configurazione (opzionale)
        """
        self.api_key = api_key
        self.host = host or "https://sdk.maybind.com"
        self.config_file = config_file
        
        # Carica configurazione da diverse fonti
        self._load_config()
        
    def _load_config(self):
        """Carica la configurazione da diverse fonti in ordine di priorità"""
        
        # 1. Parametri passati al costruttore (massima priorità)
        if self.api_key:
            return
            
        # 2. Variabili d'ambiente
        env_key = os.getenv("MAYBIND_API_KEY")
        if env_key:
            self.api_key = env_key
            self.host = os.getenv("MAYBIND_API_HOST", self.host)
            return
            
        # 3. File .env nella directory corrente
        env_file = Path(".env")
        if env_file.exists():
            self._load_from_env_file(env_file)
            return
            
        # 4. File .env nella directory del progetto
        project_env = Path(__file__).parent.parent.parent / ".env"
        if project_env.exists():
            self._load_from_env_file(project_env)
            return
            
        # 5. File di config personalizzato
        if self.config_file and Path(self.config_file).exists():
            self._load_from_config_file(self.config_file)
            return
            
    def _load_from_env_file(self, env_file):
        """Carica configurazione da file .env"""
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        if key == "MAYBIND_API_KEY":
                            self.api_key = value.strip('"\'')
                        elif key == "MAYBIND_API_HOST":
                            self.host = value.strip('"\'')
        except Exception as e:
            print(f"Errore nel caricamento del file .env: {e}")
            
    def _load_from_config_file(self, config_file):
        """Carica configurazione da file JSON"""
        try:
            import json
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.api_key = config.get('api_key')
                self.host = config.get('host', self.host)
        except Exception as e:
            print(f"Errore nel caricamento del file di configurazione: {e}")
            
    def is_configured(self):
        """Verifica se la configurazione è completa"""
        return bool(self.api_key)
        
    def get_openapi_configuration(self):
        """Restituisce la configurazione OpenAPI"""
        if not self.is_configured():
            raise ValueError("API key non configurata! Vedi setup_config() per i dettagli.")
            
        configuration = Configuration()
        configuration.host = self.host
        configuration.api_key['ApiKeyAuth'] = self.api_key
        configuration.timeout = 30
        configuration.verify_ssl = True
        
        return configuration
        
    def get_api_client(self):
        """Restituisce un client API configurato"""
        config = self.get_openapi_configuration()
        return ApiClient(config)
        
    def get_default_api(self):
        """Restituisce l'istanza DefaultApi configurata"""
        client = self.get_api_client()
        return DefaultApi(client)
        
    def setup_config(self):
        """Aiuta l'utente a configurare l'API key"""
        print("🔐 Configurazione Maybind SDK")
        print("=" * 40)
        
        if self.is_configured():
            print(f"✅ API key già configurata")
            print(f"   Host: {self.host}")
            print(f"   API Key: {'*' * 20}...{self.api_key[-4:]}")
            return True
            
        print("❌ API key non configurata!")
        print("\nModi per configurare l'API key:")
        print("\n1. Variabile d'ambiente (raccomandato):")
        print("   Windows: set MAYBIND_API_KEY=your_api_key_here")
        print("   Unix/Linux/macOS: export MAYBIND_API_KEY='your_api_key_here'")
        
        print("\n2. File .env:")
        print("   Crea un file .env nella directory del progetto:")
        print("   MAYBIND_API_KEY=your_api_key_here")
        print("   MAYBIND_API_HOST=https://sdk.maybind.com")
        
        print("\n3. Nel codice Python:")
        print("   config = MaybindConfig(api_key='your_api_key_here')")
        
        print("\n4. Configurazione interattiva:")
        try:
            api_key = input("Inserisci la tua API key: ").strip()
            if api_key:
                self.api_key = api_key
                print("✅ API key configurata temporaneamente!")
                
                # Chiedi se salvare in .env
                save = input("Salvare in .env? (s/n): ").strip().lower()
                if save == 's':
                    self._save_to_env_file()
                    
                return True
        except KeyboardInterrupt:
            print("\n❌ Configurazione annullata")
            
        return False
        
    def _save_to_env_file(self):
        """Salva la configurazione in .env"""
        try:
            env_content = f"""# Maybind SDK Configuration
MAYBIND_API_KEY={self.api_key}
MAYBIND_API_HOST={self.host}
"""
            with open(".env", "w") as f:
                f.write(env_content)
            print("✅ Configurazione salvata in .env")
        except Exception as e:
            print(f"❌ Errore nel salvataggio: {e}")
            
    def test_connection(self):
        """Testa la connessione API"""
        if not self.is_configured():
            print("❌ API key non configurata!")
            return False
            
        try:
            api = self.get_default_api()
            
            print("🧪 Testando connessione...")
            print(f"   Host: {self.host}")
            print(f"   API Key: {'*' * 20}...{self.api_key[-4:]}")
            
            # Test health check
            try:
                response = api.health_check_health_get()
                print("✅ Health check: OK")
                print(f"   Response: {response}")
            except Exception as e:
                print(f"⚠️  Health check: {e}")
                
            return True
            
        except Exception as e:
            print(f"❌ Errore di connessione: {e}")
            return False


# Funzioni di utilità per semplificare l'uso
def quick_setup():
    """Setup rapido dell'SDK"""
    config = MaybindConfig()
    
    if not config.setup_config():
        return None
        
    return config

def get_configured_api():
    """Ottiene un'istanza API configurata"""
    config = MaybindConfig()
    
    if not config.is_configured():
        print("❌ API key non configurata!")
        print("Esegui: python -c \"from config import quick_setup; quick_setup()\"")
        return None
        
    return config.get_default_api()

def test_sdk():
    """Test rapido dell'SDK"""
    config = MaybindConfig()
    
    if not config.is_configured():
        print("Configurazione necessaria...")
        if not config.setup_config():
            return False
            
    return config.test_connection()


if __name__ == "__main__":
    # Esegui setup interattivo
    config = quick_setup()
    if config:
        config.test_connection()
