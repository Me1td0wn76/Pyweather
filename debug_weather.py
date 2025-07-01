import os
import json
import requests
import tkinter as tk
from tkinter import messagebox
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import time

CONFIG_PATH = "weather_config.json"
AREA_LIST_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{}.json"
INTERVAL = 3600  # 1時間更新

CONFIG = {}

# 設定読み込み
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 天気取得
def fetch_forecast(area_code):
    try:
        url = FORECAST_URL_TEMPLATE.format(area_code)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["headlineText"] + "\n\n" + data["text"]
    except Exception as e:
        return f"取得エラー: {e}"

def show_weather():
    print(f"天気を表示中: {CONFIG}")
    weather = fetch_forecast(CONFIG["code"])
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(f"{CONFIG['name']}の天気概況", weather)
    root.destroy()

def weather_loop(icon):
    print("天気ループ開始")
    while icon.visible:
        try:
            forecast = fetch_forecast(CONFIG["code"])
            latest = forecast.split("\n")[0][:30]
            icon.title = f"{CONFIG['name']}：{latest}"
            print(f"天気情報更新: {latest}")
            time.sleep(INTERVAL)
        except Exception as e:
            print(f"天気ループエラー: {e}")
            time.sleep(60)  # エラー時は1分後にリトライ

def create_icon_image():
    try:
        img = Image.new("RGB", (64, 64), "skyblue")
        draw = ImageDraw.Draw(img)
        draw.text((10, 20), "☀", fill="white")
        print("アイコン画像作成完了")
        return img
    except Exception as e:
        print(f"アイコン作成エラー: {e}")
        raise

def exit_app(icon, item):
    print("アプリケーション終了")
    icon.stop()

def main():
    print("アプリケーション開始")
    
    global CONFIG
    CONFIG = load_config()
    print(f"設定読み込み: {CONFIG}")
    
    if "code" not in CONFIG:
        print("設定が不完全です")
        return
    
    try:
        print("システムトレイアイコン作成中...")
        icon = Icon("WeatherTray")
        icon.icon = create_icon_image()
        icon.menu = Menu(
            MenuItem("天気を見る", lambda: show_weather()),
            MenuItem("終了", lambda icon, item: exit_app(icon, item))
        )
        
        print("天気ループスレッド開始...")
        threading.Thread(target=weather_loop, args=(icon,), daemon=True).start()
        
        print("システムトレイアイコン表示...")
        icon.run()
        
    except Exception as e:
        print(f"メイン処理エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
