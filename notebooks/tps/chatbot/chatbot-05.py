"""
this version is now able to send requests to a server
it just prints the response for now
"""

import requests
import flet as ft


SERVERS = [
    # this one is fast because it has GPUs,
    # but it requires a login / password
    {
        "name": "GPU fast",
        "url": "https://ollama-sam.inria.fr",
        "username": "Bob",
        "password": "hiccup",
        "default": True,
    },
    # this one is slow because it has no GPUs,
    # but it does not require a login / password
    {
        "name": "CPU slow",
        "url": "http://ollama.pl.sophia.inria.fr:8080",
    },
]


# a hardwired list of models
MODELS = [
    "gemma2:2b",
    "mistral:7b",
]


TITLE = "My first Chatbot 05"


# find the server details from the UI label
def spot_server(servername):
    return next(server for server in SERVERS if servername in server["name"])


def send_request(servername, model, streaming, prompt):
    server = spot_server(servername)
    print(f"Sending message to {server=}, {model=}, {streaming=}, {prompt=}")
    # first version is non-streaming
    url = f"{server['url']}/api/generate"
    data = {'model': model, 'prompt': prompt}
    answer = requests.post(url, json=data)
    print("HTTP status code:", answer.status_code)
    print(f"Received answer: {answer.text}")


class History(ft.Column):
    """
    the history is a column of text messages
    where prompts and answers alternate
    """

    def __init__(self):
        super().__init__([ft.TextField(label="Type a message...")])

    # leave the prompt as the last entry
    # so insert at the penultimate position;
    def add_message(self, message):
        self.controls.insert(-1, ft.Text(value=message))
    def current_prompt(self):
        return self.controls[-1].value


class ChatbotApp(ft.Column):

    def __init__(self):
        header = ft.Text(value=TITLE, size=40)

        self.streaming = ft.Checkbox(label="streaming", value=False)
        self.model = ft.Dropdown(
            options=[ft.dropdown.Option(model) for model in MODELS],
            value=MODELS[0],
            width=300,
        )
        self.server = ft.Dropdown(
            options=[ft.dropdown.Option(server) for server in ("CPU", "GPU")],
            value="CPU",
            width=100,
        )

        self.submit = ft.ElevatedButton("Send", on_click=self.show_current_settings)

        self.history = History()

        row = ft.Row(
            [self.streaming, self.model, self.server, self.submit],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        super().__init__(
            [header, row, self.history],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)


    # in this version we access the application status through
    # attributes in the 'ChatbotApp' instance
    def show_current_settings(self, _event):
        print("Your current settings :")
        print(f"{self.streaming.value=}")
        print(f"{self.model.value=}")
        print(f"{self.server.value=}")
        print(f"{self.history.current_prompt()=}")
        send_request(self.server.value, self.model.value,
                     self.streaming.value, self.history.current_prompt())


def main(page: ft.Page):
    page.title = TITLE

    chatbot = ChatbotApp()
    page.add(chatbot)


ft.app(target=main)
