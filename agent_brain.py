import os
import json
from google import genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

client = genai.Client(api_key=GOOGLE_API_KEY)

class TradingBrain:
    def __init__(self):
        self.model_id = MODEL_NAME

    def get_recommendation(self, market_data):
        """Envía los datos al modelo y recibe una recomendación en formato JSON."""
        
        prompt = f"""
        Eres un Agente de IA experto en Trading. Analiza los siguientes datos y decide si debemos COMPRAR, VENDER o ESPERAR.
        
        DATOS ACTUALES:
        {market_data}

        INSTRUCCIONES:
        1. Responde ÚNICAMENTE con un objeto JSON válido.
        2. Para cada moneda, decide una acción basándote en el RSI y la Tendencia.
        3. Si el RSI < 35 y tendencia ALCISTA, considera COMPRAR.
        4. Si el RSI > 65, considera VENDER.
        5. En cualquier otro caso, elige ESPERAR.

        FORMATO DE RESPUESTA REQUERIDO (JSON):
        {{
            "recomendaciones": [
                {{
                    "simbolo": "BTC/USDT",
                    "accion": "COMPRAR",
                    "razon": "Explicación breve"
                }},
                ...
            ]
        }}
        """

        try:
            response = client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            # Limpiamos la respuesta por si la IA pone texto extra o backticks
            clean_response = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_response)
        except Exception as e:
            print(f"❌ Error decodificando JSON de la IA: {e}")
            return None

if __name__ == "__main__":
    # Prueba rápida
    brain = TradingBrain()
    print("🧠 Probando respuesta JSON de la IA...")
    # Datos de prueba
    test_data = [{'symbol': 'BTC/USDT', 'price': 60000, 'rsi': 25, 'trend': 'ALCISTA 🟢'}]
    print(brain.get_recommendation(test_data))
