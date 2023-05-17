import config
import requests

headers = {
  'x-access-token': config.apiKey
}

response = requests.get("https://api.coinranking.com/v2/coins", headers=headers)
cryptoCoins = []

if response.status_code == 200:
    data = response.json()['data']['coins']
    cryptoCoins.extend(coin['symbol'] for coin in data)
    #print(cryptoCoins)
else:
    print(f"Error: {response.status_code}")
