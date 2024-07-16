from openai import OpenAI
from time import sleep
import json

client = OpenAI()
starting_assistant = ""
starting_thread = ""

# Read more about function calling: https://platform.openai.com/docs/assistants/tools/function-calling
starting_tools = [
    {
        "type": "function",
        "function": {
            "name": "getCurrentWeather",
            "description": "Get the weather in location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state e.g. San Francisco, CA",
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "getNickname",
            "description": "Get the nickname of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state e.g. San Francisco, CA",
                    },
                },
                "required": ["location"],
            },
        },
    },
    # Add your next tool here
]


# Example function which would check the weather but is hardcoded in this example
def get_current_weather(location):
    return f"The weather in {location} is 64 degrees."


# Example function which would check the city nickname but is hardcoded in this example
def get_nickname(location):
    nickname = "TheCity"
    if location == "Chicago":
        nickname = "The Windy City"
    return f"The nickname for {location} is {nickname}."


def create_assistant():
    print("Creating assistant...")  # Debug
    if starting_assistant == "":
        my_assistant = client.beta.assistants.create(
            instructions="You are a helpful assistant.",
            name="MyQuickstartAssistant",
            model="gpt-3.5-turbo-0125",
            tools=starting_tools,
        )
    else:
        my_assistant = client.beta.assistants.retrieve(starting_assistant)
    print("Assistant created or retrieved.")  # Debug
    return my_assistant


def create_thread():
    print("Creating thread...")  # Debug
    empty_thread = client.beta.threads.create()
    print("Thread created.")  # Debug
    return empty_thread


def send_message(thread_id, message):
    print(f"Sending message to thread {thread_id}...")  # Debug
    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message,
    )
    print("Message sent.")  # Debug
    return thread_message


def run_assistant(thread_id, assistant_id):
    print(f"Running assistant {assistant_id} on thread {thread_id}...")  # Debug
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    print("Assistant run started.")  # Debug
    return run


def get_newest_message(thread_id):
    print(f"Getting newest message from thread {thread_id}...")  # Debug
    thread_messages = client.beta.threads.messages.list(thread_id)
    print("Newest message retrieved.")  # Debug
    return thread_messages.data[0]


def get_run_status(thread_id, run_id):
    print(f"Getting run status for run {run_id} in thread {thread_id}...")  # Debug
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    print(f"Run status: {run.status}")  # Debug
    return run.status


def run_action(thread_id, run_id):
    print(f"Running action for run {run_id} in thread {thread_id}...")  # Debug
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    for tool in run.required_action.submit_tool_outputs.tool_calls:
        print(f"Processing tool call: {tool.function.name}")  # Debug

        if tool.function.name == "getCurrentWeather":
            arguments = json.loads(tool.function.arguments)
            location = arguments["location"]

            weather_info = get_current_weather(location)

            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool.id,
                        "output": weather_info,
                    },
                ],
            )
        elif tool.function.name == "getNickname":
            arguments = json.loads(tool.function.arguments)
            location = arguments["location"]

            name_info = get_nickname(location)

            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool.id,
                        "output": name_info,
                    },
                ],
            )
        else:
            raise Exception(
                f"Unsupported function call: {tool.function.name} provided."
            )
    print("Action run completed.")  # Debug


def main():
    my_assistant = create_assistant()
    my_thread = create_thread()

    while True:
        user_message = input("Enter your message: ")
        if user_message.lower() == "exit":
            break

        send_message(my_thread.id, user_message)
        run = run_assistant(my_thread.id, my_assistant.id)

        while run.status != "completed":
            run.status = get_run_status(my_thread.id, run.id)

            # If assistant needs to call a function, it will enter the "requires_action" state
            if run.status == "requires_action":
                run_action(my_thread.id, run.id)

            sleep(1)
            print("⏳", end="\r", flush=True)

        sleep(0.5)

        response = get_newest_message(my_thread.id)
        print("Response:", response.content[0].text.value)


if __name__ == "__main__":
    main()