# 使い方
## 仮想環境の設定
#### 仮想環境の作成
```
python -m venv env
```

### 仮想環境の有効化
#### windows
```
.\env\Scripts\activate.bat
```

#### mac
```
source env/bin/activate
```

## ライブラリのインストール
```
pip install -r requirements.txt
```

## 実行
### アプリを起動
```
python src/main.py
```
カメラにARマーカーを認識されるとログファイル（read_ar_marker_logs.txt）に吐き出される

### アプリの停止
キーボードの「q」を押す

## exeファイル化
```
pyinstaller -F -w src/main.py
```