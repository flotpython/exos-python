"""
now supports streaming responses properly
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
    "deepseek-r1:7b",
]


TITLE = "My first Chatbot 08"


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
                fill_color="lightgrey",
            )],
            scroll=ft.ScrollMode.AUTO,
            auto_scroll=True,
            expand=True,
        )

    # insert material - prompt or answer - to allow for different styles
    def add_prompt(self, message):
        self._add_entry(message, "prompt")
    def add_answer(self, message):
        self._add_entry(message, "answer")
    def _add_entry(self, message, kind):
        display = ft.Text(value=message)
        display.color = "blue" if kind == "prompt" else "green"
        display.size = 20 if kind == "prompt" else 16
        display.italic = kind == "prompt"
        self.controls.insert(-1, display)

    # we always insert in the penultimate position
    # given that the last item in controls is the prompt TextField
    def add_chunk(self, chunk):
        self.controls[-2].value += chunk
    def current_prompt(self):
        return self.controls[-1].value

    def enable_prompt(self):
        self.controls[-1].disabled = False
    def disable_prompt(self):
        self.controls[-1].disabled = True

class ChatbotApp(ft.Column):

    def __init__(self):
        header = ft.Text(value="My Chatbot", size=40)

        self.streaming = ft.Checkbox(label="streaming", value=True)
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

        self.submit = ft.ElevatedButton("Send", on_click=self.send_request)

        self.history = History(self)

        row = ft.Row(
            [self.streaming, self.model, self.server, self.submit],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        super().__init__(
            [header, row, self.history],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )



    def send_request(self, _event):
        # disable the button to prevent double submission
        self.submit.disabled = True
        self.history.disable_prompt()
        self.send_request_2(_event)
        self.submit.disabled = False
        self.history.enable_prompt()
        self.update()


    # send the prompt to the server and display the answer
    def send_request_2(self, _event):
        model = self.model.value
        prompt = self.history.current_prompt()
        server_record = SERVERS[self.server.value]
        server_name = server_record['name']
        # the endpoint is always at /api/generate
        url = f"{server_record['url']}/api/generate"

        # record the question asked
        self.history.add_prompt(prompt)
        # create placeholder for the answer
        self.history.add_answer("")
        # update UI
        self.update()

        # send the request
        streaming = self.streaming.value
        print(f"Sending message to {server_name=}, {model=}, {streaming=}, {prompt=}")

        # authenticate if needed
        auth_args = {}
        if 'username' in server_record:
            auth_args = {
                'auth': (server_record['username'], server_record['password'])
            }

        payload = {'model': model, 'prompt': prompt}

        # streaming or non streaming
        if not streaming:
            answer = requests.post(url, json=payload, **auth_args)
            print("HTTP status code:", answer.status_code)
            if answer.status_code != 200:
                print("not 200, aborting")
                return
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
        else:
            # streaming version
            # we need to keep the connection open
            # and read the stream
            with requests.post(url, json=payload, stream=True, **auth_args) as answer:
                print("HTTP status code:", answer.status_code)
                if answer.status_code != 200:
                    print("not 200, aborting")
                    return
                for line in answer.iter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if data['done']:
                            pass
                        self.history.add_chunk(data['response'])
                        self.update()
                    except Exception as e:
                        print(f"Exception {type(e)=}, {e=}")


def main(page: ft.Page):
    page.title = TITLE

    chatbot = ChatbotApp()
    page.add(chatbot)


ft.app(target=main)
