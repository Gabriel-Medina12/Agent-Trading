import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

class TelegramNotifier:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID

    def send_message(self, message):
        """Envía un mensaje de texto a Telegram."""
        if not self.token or not self.chat_id:
            print("⚠️ Error: Telegram no configurado (Token o Chat ID faltante).")
            return
            
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("✅ Mensaje enviado a Telegram correctamente.")
            else:
                print(f"❌ Error al enviar a Telegram: {response.text}")
        except Exception as e:
            print(f"❌ Error de conexión con Telegram: {e}")

if __name__ == "__main__":
    # Prueba rápida
    notifier = TelegramNotifier()
    notifier.send_message("🚀 *¡Agente de Trading activado!* Estoy listo para vigilar el mercado por ti.")
