import requests
import math
import time
import numpy as np
import os

os.system('cls')

API_KEY = ""
API_SECRET = ""

def get_coin_price(coin_id):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin_id}USDT"
    response = requests.get(url)
    data = response.json()

    if "price" in data:
        return float(data["price"])

    return None

def calculate_log_prices(price_data):
    return [math.log(price) for price in price_data]

def detect_navarro_200_formation(price_data):
    num_periods = 200
    formation_count = 0
    log_prices = calculate_log_prices(price_data)
    formation_points = []

    for i in range(num_periods, len(price_data)):
        if price_data[i] < 0.95 * price_data[i - num_periods]:
            formation_count += 1
            formation_points.append(i)

    formation_percentage = (formation_count / (len(price_data) - num_periods)) * 100

    return formation_percentage, log_prices, formation_points

class FormationPoints:
    def __init__(self, price_data):
        self.num_periods = 200
        self.formation_count = 0
        self.formation_points = []

        for i in range(self.num_periods, len(price_data)):
            if price_data[i] < 0.95 * price_data[i - self.num_periods]:
                self.formation_count += 1
                self.formation_points.append(price_data[i])

        self.formation_percentage = (self.formation_count / (len(price_data) - self.num_periods)) * 100


watchlist = ["BTC", "ETH", "XRP"]

while True:
    for coin in watchlist:
        coin_price = get_coin_price(coin)

        if coin_price is not None:
            price_data = [coin_price]

            formation_percentage, log_prices, formation_points = detect_navarro_200_formation(price_data)
            formation_points = FormationPoints(price_data)
            
            print("[COIN_LIVE_DATA]", price_data)

            print(f"{coin} için Navarro 200 formasyonunun oluşum yüzdesi: {formation_percentage:.2f}%")

            print("Fiyat Verileri:")
            for i, price in enumerate(price_data):
                print(f"{i + 1}. fiyat: {price:.3f}")

            print("Logaritmik Veriler:")
            for i, log_price in enumerate(log_prices):
                print(f"{i + 1}. logaritmik değer: {log_price:.3f}")

            print("Formasyon Noktaları:")
            if formation_points.formation_points:
                for point in formation_points.formation_points:
                    print(f"Formasyon noktası: {point:.2f} \n")
            else:
                print("Formasyon noktası bulunamadı. \n")

        else:
            print(f"{coin} için fiyat verisi alınamadı.")

    time.sleep(60)  # Her dakika yenile

