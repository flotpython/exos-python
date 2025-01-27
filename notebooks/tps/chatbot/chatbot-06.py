"""
this version now actually displays the answer from the server

to this end, the History class is a little more elaborate,
as it needs to add only pieces of the answer to the last message
"""

import json

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
]


TITLE = "My first Chatbot 06"


class History(ft.Column):
    """
    the history is a column of text messages
    where prompts and answers alternate
    """

    def __init__(self, app):
        super().__init__(
            [ft.TextField(
                label="Type a message...",
                on_submit=lambda event: app.send_request(event),
            )]
        )

    def add_message(self, message):
        self.controls.insert(-1, ft.Text(value=message))
    def add_chunk(self, chunk):
        self.controls[-2].value += chunk
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


    # need to split this in two for clarity
    # could use a better naming, but to minimize the diffs
    # we still use these names
    def send_request(self, _event):
        model = self.model.value
        prompt = self.history.current_prompt()
        server_record = SERVERS[self.server.value]
        server_name = server_record['name']
        # the endpoint is always at /api/generate
        url = f"{server_record['url']}/api/generate"

        # record the question asked
        self.history.add_message(prompt)
        # create placeholder for the answer
        self.history.add_message("")
        # update UI
        self.update()

        # send the request
        print(f"Sending message to {server_name}, {model=}, {prompt=}")

        # authenticate if needed
        auth_args = {}
        if 'username in server_record':
            auth_args = {
                'auth': (server_record['username'], server_record['password'])
            }

        # prepare data
        payload = {'model': model, 'prompt': prompt}
        answer = requests.post(url, json=payload, **auth_args)
        print("HTTP status code:", answer.status_code)
        # turns out we receive a stream of JSON objects
        # each one on its own line
        for line in answer.text.split("\n"):
            # splitting artefacts can be ignored
            if not line:
                continue
            # ther should be no exception, but just in case...
            try:
                # print("line:", line)
                data = json.loads(line)
                # the last JSON chunk contains statistics and is not a message
                if data['done']:
                    # ignore last summary chunk
                    pass
                # display that message; it's only a token so we append it to the last message
                self.history.add_chunk(data['response'])
            except Exception as e:
                print(f"Exception {type(e)=}, {e=}")
        self.update()


def main(page: ft.Page):
    page.title = TITLE

    chatbot = ChatbotApp()
    page.add(chatbot)


ft.app(target=main)
