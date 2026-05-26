import time
import os
from datetime import datetime
from dotenv import load_dotenv
from observer import CryptoObserver
from agent_brain import TradingBrain
from telegram_notifier import TelegramNotifier
from portfolio_manager import PortfolioManager

load_dotenv()
INTERVALO = 3600  # 1 hora

def run_agent():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n🚀 [{now}] Iniciando ciclo del Agente con Paper Trading...")
    
    try:
        # 1. Inicializar módulos
        observer = CryptoObserver()
        brain = TradingBrain()
        notifier = TelegramNotifier()
        portfolio = PortfolioManager()
        
        # 2. Obtener datos del mercado
        market_data = observer.get_market_summary()
        current_prices = {item['symbol']: item['price'] for item in market_data}
        
        # 3. Obtener recomendación de la IA (JSON)
        print("🤖 La IA está analizando y tomando decisiones...")
        decision_json = brain.get_recommendation(market_data)
        
        if not decision_json:
            print("⚠️ No se pudo obtener una decisión válida.")
            return

        # 4. Ejecutar operaciones y construir mensaje
        report_lines = []
        trade_results = []
        
        for rec in decision_json.get("recomendaciones", []):
            symbol = rec["simbolo"]
            action = rec["accion"]
            reason = rec["razon"]
            price = current_prices.get(symbol)
            
            # Intentar ejecutar operación si es COMPRAR o VENDER
            if action in ["COMPRAR", "VENDER"]:
                res = portfolio.execute_trade(symbol, action, price)
                if res:
                    trade_results.append(res)
            
            report_lines.append(f"🪙 *{symbol}*: {action}\n└ _{reason}_")

        # 5. Calcular valor total del portafolio
        total_val = portfolio.get_total_value(current_prices)
        cash = portfolio.data["cash"]
        
        # 6. Enviar a Telegram
        header = f"📊 *REPORTE DE OPERACIONES* 🕒 _{now}_"
        body = "\n\n".join(report_lines)
        trades = "\n".join(trade_results) if trade_results else "No se realizaron operaciones."
        footer = f"\n\n💰 *PORTAFOLIO VIRTUAL*\n💵 Efectivo: ${cash:.2f}\n📈 Valor Total: ${total_val:.2f}"
        
        final_message = f"{header}\n\n{body}\n\n⚡ *EJECUCIÓN:*\n{trades}{footer}"
        notifier.send_message(final_message)
        
        print("✅ Ciclo completado y notificado.")

    except Exception as e:
        print(f"❌ Error crítico en el ciclo: {e}")

if __name__ == "__main__":
    print("🚀 Agente de Trading con Paper Trading ACTIVO.")
    run_agent()
    
    while True:
        time.sleep(INTERVALO)
        run_agent()
