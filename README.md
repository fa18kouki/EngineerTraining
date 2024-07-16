# OpenAI API クイックスタート - Python

このリポジトリには、さまざまなOpenAI APIエンドポイント（チャット、アシスタントなど）のクイックスタートアプリが複数ホストされています。`examples`フォルダをチェックして、さまざまな例を試し、OpenAI APIの使用を開始してください。

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