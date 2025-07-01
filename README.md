# Pyweather - 日本の天気予報システムトレイアプリ

日本気象庁のAPIを使用して天気予報を取得し、システムトレイに表示するPythonアプリケーションです。

## 機能

- 気象庁の公式データから天気予報を取得
- システムトレイに常駐して定期的に天気情報を更新
- 右クリックメニューから天気詳細の確認
- 地域の変更機能

## 必要な環境

- Python 3.7以上
- Windows OS（システムトレイ機能のため）

## 必要なライブラリ

```bash
pip install requests pillow pystray
```

## ファイル構成

- `hoge.py` - メインのアプリケーションファイル
- `debug_weather.py` - デバッグ用の簡易版
- `test_weather.py` - 天気API取得のテスト用
- `weather_config.json` - 地域設定ファイル（自動生成）

## 使い方

### 1. 初回セットアップ

```bash
python hoge.py
```

初回起動時は地域選択画面が表示されます：
1. 都道府県を選択
2. 市区町村を選択
3. 設定が`weather_config.json`に保存されます

### 2. 通常の使用

アプリケーションが起動すると：
- システムトレイに天気アイコンが表示されます
- 1時間ごとに天気情報が自動更新されます
- トレイアイコンを右クリックでメニューが表示されます

### 3. メニュー機能

- **天気を見る**: 詳細な天気予報をポップアップで表示
- **地域を変更**: 別の地域に変更
- **終了**: アプリケーションを終了

## トラブルシューティング

### 起動しても何も表示されない場合

1. **設定ファイルの確認**
   ```bash
   python test_weather.py
   ```
   このコマンドで天気情報が正常に取得できるか確認

2. **デバッグモードで実行**
   ```bash
   python debug_weather.py
   ```
   詳細なログを確認して問題を特定

3. **必要なライブラリの確認**
   ```bash
   python -c "import pystray; print('pystray OK')"
   python -c "from PIL import Image; print('PIL OK')"
   ```

### よくある問題と解決方法

#### 1. ライブラリが見つからないエラー
```bash
pip install requests pillow pystray
```

#### 2. システムトレイにアイコンが表示されない
- Windowsの通知領域設定を確認
- 管理者権限で実行してみる
- ウイルス対策ソフトによるブロックを確認

#### 3. 天気情報が取得できない
- インターネット接続を確認
- ファイアウォール設定を確認
- `test_weather.py`で単体テスト実行

#### 4. 地域設定が正しくない
設定ファイルを削除して再設定：
```bash
del weather_config.json
python hoge.py
```

## 設定ファイル例

`weather_config.json`:
```json
{
  "pref": "大阪府",
  "name": "大阪府 大阪府", 
  "code": "270000"
}
```

## API仕様

このアプリケーションは以下の気象庁APIを使用しています：

- 地域情報: `https://www.jma.go.jp/bosai/common/const/area.json`
- 天気予報: `https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{地域コード}.json`

## 注意事項

- このアプリケーションは非公式です
- 気象庁のAPIに過度な負荷をかけないよう、更新間隔は1時間に設定されています
- 商用利用前には気象庁の利用規約を確認してください

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 更新履歴

- v1.0: 基本機能実装
- v1.1: デバッグ機能追加、エラーハンドリング改善
