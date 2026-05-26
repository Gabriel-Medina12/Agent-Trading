import ccxt
import pandas as pd
import pandas_ta as ta
import time

class CryptoObserver:
    def __init__(self, symbols=['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT']):
        self.exchange = ccxt.binance()
        self.symbols = symbols

    def fetch_data(self, symbol, timeframe='1h', limit=100):
        """Obtiene datos históricos (OHLCV) de un símbolo."""
        print(f"📡 Obteniendo datos para {symbol}...")
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"❌ Error al obtener datos de {symbol}: {e}")
            return None

    def analyze_indicators(self, df):
        """Calcula indicadores técnicos básicos."""
        if df is None or df.empty:
            return None
        # RSI (Índice de Fuerza Relativa)
        df['RSI'] = ta.rsi(df['close'], length=14)
        
        # Medias Móviles (Tendencia)
        df['EMA_20'] = ta.ema(df['close'], length=20)
        df['EMA_50'] = ta.ema(df['close'], length=50)
        
        return df

    def get_market_summary(self):
        """Genera un resumen del estado actual de las monedas seleccionadas."""
        summary = []
        for symbol in self.symbols:
            df = self.fetch_data(symbol)
            df = self.analyze_indicators(df)
            
            if df is not None:
                last_row = df.iloc[-1]
                
                # Lógica simple de tendencia
                trend = "ALCISTA 🟢" if last_row['EMA_20'] > last_row['EMA_50'] else "BAJISTA 🔴"
                
                info = {
                    'symbol': symbol,
                    'price': last_row['close'],
                    'rsi': round(last_row['RSI'], 2) if not pd.isna(last_row['RSI']) else 0,
                    'trend': trend,
                    'change_24h': round(((last_row['close'] - df.iloc[0]['close']) / df.iloc[0]['close']) * 100, 2)
                }
                summary.append(info)
        
        return summary

if __name__ == "__main__":
    observer = CryptoObserver()
    print("\n--- REPORTE DEL OBSERVADOR ---")
    results = observer.get_market_summary()
    
    for res in results:
        print(f"\n🪙 {res['symbol']}")
        print(f"   Precio: ${res['price']}")
        print(f"   RSI: {res['rsi']} ({'Sobreventa' if res['rsi'] < 30 else 'Sobrecompra' if res['rsi'] > 70 else 'Neutral'})")
        print(f"   Tendencia (EMA 20/50): {res['trend']}")
        print(f"   Cambio (periodo): {res['change_24h']}%")
