import json
import os

PORTFOLIO_FILE = "portfolio.json"

class PortfolioManager:
    def __init__(self, initial_cash=1000.0):
        self.initial_cash = initial_cash
        self.load_portfolio()

    def load_portfolio(self):
        """Carga el portafolio desde el archivo JSON o crea uno nuevo."""
        if os.path.exists(PORTFOLIO_FILE):
            with open(PORTFOLIO_FILE, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "cash": self.initial_cash,
                "positions": {}, # Ejemplo: {"BTC/USDT": 0.001}
                "history": []
            }
            self.save_portfolio()

    def save_portfolio(self):
        """Guarda el estado actual en el archivo JSON."""
        with open(PORTFOLIO_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def execute_trade(self, symbol, action, price, amount_usd=100.0):
        """
        Ejecuta una compra o venta virtual.
        amount_usd: Cantidad de dólares a invertir en la compra.
        """
        if action == "COMPRAR":
            if self.data["cash"] >= amount_usd:
                quantity = amount_usd / price
                self.data["cash"] -= amount_usd
                self.data["positions"][symbol] = self.data["positions"].get(symbol, 0) + quantity
                self.data["history"].append({
                    "date": str(os.times()), # Simplificado
                    "symbol": symbol,
                    "action": "BUY",
                    "price": price,
                    "quantity": quantity
                })
                self.save_portfolio()
                return f"✅ Compra virtual: {quantity:.6f} {symbol} a ${price}"
            else:
                return "❌ Fondos insuficientes para comprar."

        elif action == "VENDER":
            if symbol in self.data["positions"] and self.data["positions"][symbol] > 0:
                quantity = self.data["positions"][symbol]
                total_value = quantity * price
                self.data["cash"] += total_value
                del self.data["positions"][symbol]
                self.data["history"].append({
                    "date": str(os.times()),
                    "symbol": symbol,
                    "action": "SELL",
                    "price": price,
                    "quantity": quantity
                })
                self.save_portfolio()
                return f"💰 Venta virtual: {quantity:.6f} {symbol} a ${price} (Total: ${total_value:.2f})"
            else:
                return f"⚠️ No tienes posición en {symbol} para vender."
        
        return None

    def get_total_value(self, current_prices):
        """Calcula el valor total del portafolio (Efectivo + Monedas)."""
        total_value = self.data["cash"]
        for symbol, qty in self.data["positions"].items():
            price = current_prices.get(symbol, 0)
            total_value += qty * price
        return total_value

if __name__ == "__main__":
    # Prueba rápida
    pm = PortfolioManager()
    print(f"Saldo inicial: ${pm.data['cash']}")
