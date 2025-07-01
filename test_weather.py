import json
import requests

# コンフィグファイルから設定を読み込み
def load_config():
    with open("weather_config.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 天気予報を取得
def fetch_forecast(area_code):
    try:
        url = f"https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{area_code}.json"
        print(f"リクエストURL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"ステータスコード: {response.status_code}")
        
        response.raise_for_status()
        data = response.json()
        
        print("レスポンスデータの構造:")
        print(f"keys: {list(data.keys())}")
        
        if "headlineText" in data and "text" in data:
            return data["headlineText"] + "\n\n" + data["text"]
        else:
            return f"データ構造が予期したものと異なります: {data}"
            
    except requests.exceptions.RequestException as e:
        return f"リクエストエラー: {e}"
    except json.JSONDecodeError as e:
        return f"JSONデコードエラー: {e}"
    except Exception as e:
        return f"その他のエラー: {e}"

def main():
    # 設定を読み込み
    config = load_config()
    print(f"設定: {config}")
    
    # 天気予報を取得
    forecast = fetch_forecast(config["code"])
    print(f"\n{config['name']}の天気概況:")
    print("-" * 50)
    print(forecast)

if __name__ == "__main__":
    main()
