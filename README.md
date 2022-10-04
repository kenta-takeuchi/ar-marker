# 使い方
## 仮想環境の作成
python -m venv env

## 仮想環境の有効化
### windows
.env\Scripts\activate.bat

### mac
source env/bin/activate

## ライブラリのインストール
pip install -r requirements.txt

## 実行
### カメラを起動してARマーカーの認識
python src/main.py

### ログの
read_ar_marker_logs.txtにログが吐き出される

### カメラの停止
キーボードの「q」を押す

