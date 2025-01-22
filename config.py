# Description: Configuration file for the CoinGecko API
API_KEY_HEADER = 'x-cg-pro-api-key'
API_KEY = 'CG-3fbgb2MmtN3mXh8iQc8myWFh'

#
REFRESH_INTERVAL = 100  # in seconds
PRICE_CHANGE_THRESHOLD = 0.01
MINIMUM_PRICE_CHANGE_THRESHOLD = 0.001

# Default currency
CURRENCY = 'usd'

# Number of coins to display
COIN_COUNTER = 5

# List of cryptocurrencies to track due to limits of demo API
CRYPTOS = [
    {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
    {"id": "ethereum", "symbol": "eth", "name": "Ethereum"},
    {"id": "ripple", "symbol": "xrp", "name": "XRP"},
    {"id": "tether", "symbol": "usdt", "name": "Tether"},
    {"id": "solana", "symbol": "sol", "name": "Solana"}
]

# Set to True to avoid fetching ALL cryptocurrencies from the API
IN_TEST = True
