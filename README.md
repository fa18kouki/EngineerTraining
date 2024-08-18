# 株式会社E.G.T研修用リポジトリ

このリポジトリには、さまざまなOpenAI APIエンドポイント（チャット、アシスタントなど）のクイックスタートアプリが複数ホストされています。`examples`フォルダをチェックして、さまざまな例を試し、OpenAI APIの使用を開始し、CursorやCopilotを使用して思い通りに編集してみましょう

## Cursor用OpenAI API リファレンスドキュメントURL
URL:https://platform.openai.com/docs/api-reference
## OpenAI APIキー

## 基本リクエスト

[OpenAI Python SDK](https://github.com/openai/openai-python)を使用して最初のAPIリクエストを送信するには、[依存関係をインストール](https://platform.openai.com/docs/quickstart?context=python)してから、次のコードを実行してください：

```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "あなたは役に立つアシスタントです。"},
    {"role": "user", "content": "こんにちは！"}
  ]
)

print(completion.choices[0].message)
```

## セットアップ

1. Pythonがインストールされていない場合は、[Python.org](https://www.python.org/downloads/)からインストールしてください。

2. このリポジトリを[クローン](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)してください。

3. プロジェクトディレクトリに移動してください：

   ```bash
   $ cd openai-quickstart-python
   ```

4. 新しい仮想環境を作成してください：

   - macOS：

     ```bash
     $ python -m venv venv
     $ . venv/bin/activate
     ```

   - Windows：
     ```cmd
     > python -m venv venv
     > .\venv\Scripts\activate
     ```

5. 要件をインストールしてください：

   ```bash
   $ pip install -r requirements.txt
   ```

6. 例の環境変数ファイルのコピーを作成してください：

   ```bash
   $ cp .env.example .env
   ```

7. 新しく作成された`.env`ファイルに[APIキー](https://platform.openai.com/api-keys)を追加してください。

8. アプリを実行してください：

このステップは、アプリ自体によって異なります。Flaskを使用している場合（チャットの基本的な例のように）、次のように実行できます：

```bash
$ flask run
```

ブラウザから[http://localhost:5000](http://localhost:5000)のURLでアプリにアクセスできるようになります！

単純なPythonスクリプトの場合は、次のように実行できます：

```bash
$ python my_file.py
```


## 各チュートリアルの動かし方

### Assistant Flask アプリケーション

1. `examples/assistant-flask`ディレクトリに移動します。
2. 必要な依存関係をインストールします。
3. Flaskアプリを実行します：

   ```bash
   $ flask run
   ```

4. ブラウザで[http://localhost:5000](http://localhost:5000)にアクセスします。

### Chat Basic アプリケーション

1. `examples/chat-basic`ディレクトリに移動します。
2. 必要な依存関係をインストールします。
3. アプリを実行します：

   ```bash
   $ python app.py
   ```

4. ブラウザで[http://localhost:5000](http://localhost:5000)にアクセスします。

### Assistant Basic アプリケーション

1. `examples/assistant-basic`ディレクトリに移動します。
2. 必要な依存関係をインストールします。
3. アプリを実行します：

   ```bash
   $ python assistant.py
   ```

### Assistant Functions アプリケーション

1. `examples/assistant-functions`ディレクトリに移動します。
2. 必要な依存関係をインストールします。
3. アプリを実行します：

   ```bash
   $ python functions.py
   ```

### Assistant Code Interpreter アプリケーション

1. `examples/assistant-codeinterpreter`ディレクトリに移動します。
2. 必要な依存関係をインストールします。
3. アプリを実行します：

   ```bash
   $ python codeinterpreter.py
   ```

これで、各チュートリアルを実行する準備が整いました。各アプリケーションの指示に従って、OpenAI APIを活用してください。