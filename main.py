import json
import requests

endpoint_url = 'https://prices.runescape.wiki/api/v1/osrs/5m'
headers = {
    'User-Agent': 'GP Predict v1.0',
    'From': 'tysonthetyrant@gmail.com'  # This is another valid field
}

response = requests.get(endpoint_url, headers=headers)
if response.status_code == 200:
    data = response.json()
    with open("gp_data.json", "r") as file:
        existing_data = json.load(file)
    
    timestamp = data['timestamp']
    for key, value in data['data'].items():
        avgHighPrice = value['avgHighPrice']
        highPriceVolume = value['highPriceVolume']
        avgLowPrice = value['avgLowPrice']
        lowPriceVolume = value['lowPriceVolume']
        item = key

        # Check if item already exists in existing data
        item_exists = False
        for existing_item in existing_data:

            # Calculating price/volume changes
            if existing_item['item'] == item:
                last_avg_high_price = existing_item['avg_high_price'][-1]
                if last_avg_high_price is None:
                    high_price_change = None
                else:
                    high_price_change = avgHighPrice - last_avg_high_price
                last_avg_low_price = existing_item['avg_low_price'][-1]
                if last_avg_low_price is None:
                    low_price_change = None
                else:
                    low_price_change = avgLowPrice - last_avg_low_price
                
                last_high_price_volume = existing_item['high_price_volume'][-1]
                if last_high_price_volume is None:
                    high_price_volume_change = None
                else:
                    high_price_volume_change = highPriceVolume - last_high_price_volume
                
                last_low_price_volume = existing_item['low_price_volume'][-1]
                if last_low_price_volume is None:
                    low_price_volume_change = None
                else:
                    low_price_volume_change = lowPriceVolume - last_low_price_volume
                existing_item['avg_high_price'].append(avgHighPrice)
                existing_item['high_price_volume'].append(highPriceVolume)
                existing_item['avg_low_price'].append(avgLowPrice)
                existing_item['low_price_volume'].append(lowPriceVolume)
                existing_item['timestamp'].append(timestamp)
                existing_item['high_price_change'].append(high_price_change)
                existing_item['low_price_change'].append(low_price_change)
                existing_item['high_price_volume_change'].append(high_price_volume_change)
                existing_item['low_price_volume_change'].append(low_price_volume_change)
                item_exists = True
                break

        # If item doesn't exist, add a new entry
        if not item_exists:
            existing_data.append({
                'item': item,
                'avg_high_price': [avgHighPrice],
                'high_price_volume': [highPriceVolume],
                'avg_low_price': [avgLowPrice],
                'low_price_volume': [lowPriceVolume],
                'timestamp': [timestamp],
                'high_price_change': [None],
                'low_price_change': [None],
                'high_price_volume_change': [None],
                'low_price_volume_change': [None]
            })

    with open("gp_data.json", "w") as file:
        json.dump(existing_data, file, indent=4)
else:
    print("Error:", response.status_code)

# [
#     {
#         "item": "test",
#         "avg_high_price": [
#             0
#         ],
#         "avg_low_price": [
#             0
#         ],
#         "low_price_volume": [
#             0
#         ],
#         "timestamp": [
#             0
#         ],
#         "avg_high_price_change": [
#             0
#         ],
#         "low_price_change": [
#             0
#         ],
#         "high_price_volume_change": [
#             0
#         ],
#         "low_price_volume_change": [
#             0
#         ]
#     }
# ]