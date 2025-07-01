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

# 地域リスト取得
def get_area_dict():
    response = requests.get(AREA_LIST_URL)
    data = response.json()
    offices = data["offices"]
    
    # 都道府県リスト作成
    prefectures = {}
    for k, v in offices.items():
        if "children" in v and v["name"].endswith(("都", "道", "府", "県")):
            # 子要素（市区町村など）を格納
            children = {}
            for ck in v["children"]:
                if ck in offices:
                    children[offices[ck]["name"]] = ck
            prefectures[v["name"]] = children
    return prefectures

# 地域選択UI（ボタン式）
def select_area_by_button():
    area_dict = get_area_dict()
    prefecture_names = sorted(area_dict.keys())
    selected = {}

    def on_pref_select(name):
        selected["pref"] = name
        root.destroy()

    # 都道府県選択
    root = tk.Tk()
    root.title("都道府県を選択")
    row = 0
    col = 0
    for i, name in enumerate(prefecture_names):
        btn = tk.Button(root, text=name, width=15, command=lambda n=name: on_pref_select(n))
        btn.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col > 3:
            col = 0
            row += 1
    root.mainloop()

    if "pref" not in selected:
        messagebox.showerror("エラー", "都道府県が選択されませんでした")
        exit(1)

    # 市区町村選択
    city_dict = area_dict[selected["pref"]]
    city_names = sorted(city_dict.keys())

    def on_city_select(name):
        selected["name"] = f"{selected['pref']} {name}"
        selected["code"] = city_dict[name]
        root2.destroy()

    root2 = tk.Tk()
    root2.title("市区町村を選択")
    row = 0
    col = 0
    for i, name in enumerate(city_names):
        btn = tk.Button(root2, text=name, width=15, command=lambda n=name: on_city_select(n))
        btn.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col > 3:
            col = 0
            row += 1
    root2.mainloop()

    if "code" in selected:
        return selected
    else:
        messagebox.showerror("エラー", "市区町村が選択されませんでした")
        exit(1)

# 設定保存
def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False)

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
    weather = fetch_forecast(CONFIG["code"])
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(f"{CONFIG['name']}の天気概況", weather)
    root.destroy()

def weather_loop(icon):
    while icon.visible:
        forecast = fetch_forecast(CONFIG["code"])
        latest = forecast.split("\n")[0][:30]
        icon.title = f"{CONFIG['name']}：{latest}"
        time.sleep(INTERVAL)

def create_icon_image():
    img = Image.new("RGB", (64, 64), "skyblue")
    draw = ImageDraw.Draw(img)
    draw.text((10, 20), "☀", fill="white")
    return img

def exit_app(icon, item):
    icon.stop()

def change_area(icon, item):
    config = select_area_by_button()
    save_config(config)
    global CONFIG
    CONFIG = config
    show_weather()

def main():
    global CONFIG
    CONFIG = load_config()
    if "code" not in CONFIG:
        CONFIG = select_area_by_button()
        save_config(CONFIG)

    icon = Icon("WeatherTray")
    icon.icon = create_icon_image()
    icon.menu = Menu(
        MenuItem("天気を見る", lambda: show_weather()),
        MenuItem("地域を変更", lambda icon, item: change_area(icon, item)),
        MenuItem("終了", lambda icon, item: exit_app(icon, item))
    )

    threading.Thread(target=weather_loop, args=(icon,), daemon=True).start()
    icon.run()

if __name__ == "__main__":
    main()
