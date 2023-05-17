import lstm
import json
import api_fetch
import os

cryptoList = api_fetch.cryptoCoins

# Create the model outside the loop
model = lstm.create_model((None, 1))

if os.path.exists('./../crypto_data/data.json'):
    with open('./../crypto_data/data.json','w') as file:
        pass
    
    
for i in cryptoList:
    if os.path.getsize('./../crypto_data/data.json') > 0:
        with open('./../crypto_data/data.json', 'r') as file:
            data = json.load(file)
    else:
        data = []

    print(f'{i} Starting')
    x = lstm.prediction(f'{i}-USD', model)
    prediction = float(x) if x != "NA" else "NA"
    inner_dict = {
        "name": str(i),
        "prediction": str(prediction)
    }
    data.append(inner_dict)

    with open('./../crypto_data/data.json', 'w') as file:
        json.dump(data, file)
