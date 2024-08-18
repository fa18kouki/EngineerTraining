from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import time

from openai import OpenAI

client = OpenAI()

app = Flask(__name__)
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "csv"}

# Initialize the Assistant and Thread globally
assistant_id = ""
thread_id = ""

chat_history = [
    {"role": "system", "content": "あなたは役に立つアシスタントです。数学やコンピュータの問題について尋ねられた場合、質問に答えるためにコードを書いて実行してください。"},
]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify(success=False, message="No file part")

    file = request.files["file"]

    global assistant_id

    if file.filename == "":
        return jsonify(success=False, message="No selected file")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uploaded_file = client.files.create(file=file.stream, purpose="assistants")
        assistant_files = client.beta.assistants.files.list(assistant_id=assistant_id)

        file_ids = [file.id for file in assistant_files.data]
        file_ids.append(uploaded_file.id)

        client.beta.assistants.update(
            assistant_id,
            file_ids=file_ids,
        )

        return jsonify(
            success=True,
            message="File uploaded successfully and added to the Assistant",
            filename=filename,
        )
    return jsonify(success=False, message="File type not allowed")


@app.route("/get_ids", methods=["GET"])
def get_ids():
    return jsonify(assistant_id=assistant_id, thread_id=thread_id)


@app.route("/get_messages", methods=["GET"])
def get_messages():
    if thread_id != "":
        thread_messages = client.beta.threads.messages.list(thread_id, order="asc")
        messages = [
            {
                "role": msg.role,
                "content": msg.content[0].text.value,
            }
            for msg in thread_messages.data
        ]
        return jsonify(success=True, messages=messages)
    else:
        return jsonify(success=False, message="No thread ID")


@app.route("/delete_files", methods=["POST"])
def delete_files():
    file_id = request.json.get("fileId")
    deleted_assistant_file = client.beta.assistants.files.delete(
        assistant_id=assistant_id, file_id=file_id
    )
    print("Deleted: ", deleted_assistant_file.deleted)
    if deleted_assistant_file.deleted == True:
        return jsonify(success=True, messages="File deleted!")
    else:
        return jsonify(success=False, messages="File failed to be deleted.")


@app.route("/get_files", methods=["GET"])
def get_files():
    global assistant_id
    assistant_files = client.beta.assistants.files.list(assistant_id=assistant_id)
    print(assistant_files)

    files_list = []
    for file in assistant_files.data:
        files_list.append(
            {
                "id": file.id,
                "object": file.object,
                "created_at": file.created_at,
            }
        )
    return jsonify(assistant_files=files_list)


# アシスタントの初期化とスレッドの作成
def create_assistant():
    global assistant_id
    if assistant_id == "":
        my_assistant = client.beta.assistants.create(
            instructions="あなたは役に立つアシスタントです。数学やコンピュータの問題について尋ねられた場合、質問に答えるためにコードを書いて実行してください。",
            name="MyQuickstartAssistant",
            model="gpt-3.5-turbo",
            tools=[{"type": "code_interpreter"}],
        )
        assistant_id = my_assistant.id
    else:
        my_assistant = client.beta.assistants.retrieve(assistant_id)
        assistant_id = my_assistant.id

    return my_assistant


def create_thread():
    global thread_id
    if thread_id == "":
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(thread_id)
        thread_id = thread.id

    return thread


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", chat_history=chat_history)  # インデックスページを表示


@app.route("/chat", methods=["POST"])
def chat():
    content = request.json["message"]
    chat_history.append({"role": "user", "content": content})

    # アシスタントにメッセージを送信
    message_params = {"thread_id": thread_id, "role": "user", "content": content}

    thread_message = client.beta.threads.messages.create(**message_params)

    # アシスタントを実行
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    # 実行が完了するまで待機
    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    response = client.beta.threads.messages.list(thread_id).data[0]

    text_content = None

    for content in response.content:
        if content.type == "text":
            text_content = content.text.value
            break  # 最初のテキストコンテンツが見つかったらループを終了

    if text_content:
        chat_history.append({"role": "assistant", "content": text_content})
        return jsonify(success=True, message=text_content)
    else:
        # テキストコンテンツが見つからなかった場合の処理
        return jsonify(success=False, message="テキストコンテンツが見つかりませんでした")


@app.route("/reset", methods=["POST"])
def reset_chat():
    global chat_history
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

    global thread_id
    thread_id = ""
    create_thread()
    return jsonify(success=True)

@app.before_request
def initialize():
    app.before_request_funcs[None].remove(initialize)
    create_assistant()
    create_thread()


if __name__ == "__main__":
    app.run()