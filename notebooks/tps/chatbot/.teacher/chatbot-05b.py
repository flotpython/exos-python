"""
can deal with authentication so it can talk to the GPU server as well
"""

# the library to actually send stuff to the network
import requests
import flet as ft

SERVERS = {
    # this one is fast because it has GPUs,
    # but it requires a login / password
    'GPU': {
        "name": "GPU fast",
        "url": "https://ollama-sam.inria.fr",
        "username": "Bob",
        "password": "hiccup",
    },
    # this one is slow because it has no GPUs,
    # but it does not require a login / password
    'CPU': {
        "name": "CPU slow",
        "url": "http://ollama.pl.sophia.inria.fr:8080",
    },
}


# a hardwired list of models
MODELS = [
    "gemma2:2b",
    "mistral:7b",
    "deepseek-r1:7b",
]


TITLE = "My first Chatbot 0b5"


class History(ft.Column):
    """
    the history is a column of text messages
    where prompts and answers alternate
    """

    # constructor
    def __init__(self, app):
        super().__init__(
            [ft.TextField(
                label="Type a message...",
                on_submit=lambda event: app.send_request(event),
            )]
        )

    def add_message(self, message):
        self.controls.insert(-1, ft.Text(value=message))
    def current_prompt(self):
        return self.controls[-1].value


class ChatbotApp(ft.Column):

    def __init__(self):
        header = ft.Text(value="My Chatbot", size=40)

        self.streaming = ft.Checkbox(label="streaming", value=False)
        self.model = ft.Dropdown(
            options=[ft.dropdown.Option(model) for model in MODELS],
            value=MODELS[0],
            width=300,
        )
        self.server = ft.Dropdown(
            options=[ft.dropdown.Option(server) for server in ("CPU", "GPU")],
            value="GPU",
            width=100,
        )

        submit = ft.ElevatedButton("Send", on_click=self.send_request)

        self.history = History(self)

        row = ft.Row(
            [self.streaming, self.model, self.server, submit],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        super().__init__(
            [header, row, self.history],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def send_request(self, _event):
        print("Your current settings :")
        print(f"{self.streaming.value=}")
        print(f"{self.model.value=}")
        print(f"{self.server.value=}")

        model = self.model.value
        prompt = self.history.current_prompt()
        # ignore the streaming checkbox, as this first version is non-streaming

        server_record = SERVERS[self.server.value]
        server_name = server_record['name']
        # the endpoint is always at /api/generate
        url = f"{server_record['url']}/api/generate"

        print(f"Sending message to {server_name}, {model=}, {prompt=}")

        # authenticate if needed
        auth_args = {}
        if 'username' in server_record:
            auth_args = {
                'auth': (server_record['username'], server_record['password'])
            }

        # prepare data
        payload = {'model': model, 'prompt': prompt}
        answer = requests.post(url, json=payload, **auth_args)
        print("HTTP status code:", answer.status_code)
        print(f"==== Received answer:")
        print(answer.text)


def main(page: ft.Page):
    page.title = TITLE

    chatbot = ChatbotApp()
    page.add(chatbot)


ft.app(target=main)
