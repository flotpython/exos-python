"""
better error reporting:
errors from requests are caught and displayed in a message area
between the title and the dialog
"""

import json
from datetime import datetime
from typing import Iterator

import requests
import flet as ft

# in this version we create servers as INSTANCES of CLASSES
# so we can encapsulate the logic to interact with them
#
# rationale is to be able to talk with servers that implement other APIs
# e.g. litellm that has also been deployed and on more servers

# we keep the idea of specifying our available servers as this dictionary
# but below we'll use this to create actual server INSTANCES

# provided-by-another-channel
from litellm_key import KEY as LITE_LLM_KEY

DEFAULT_SERVER = "CPU"

SERVER_SPECS = {
    # this one is fast because it has GPUs,
    # but it requires a login / password
    'GPU': {
        "type": "ollama",
        "name": "GPU fast",
        "url": "https://ollama-sam.inria.fr",
        "username": "Bob",
        "password": "hiccup",
    },
    # this one is slow because it has no GPUs,
    # but it does not require a login / password
    'CPU': {
        "type": "ollama",
        "name": "CPU slow",
        "url": "http://ollama.pl.sophia.inria.fr:8080",
    },
    'LiteLLM': {
        "type": "litellm",
        "name": "LiteLLM (GPUs)",
        "url": "https://litellm-sam.inria.fr",
        "key": LITE_LLM_KEY,
    }
}

TITLE = "My first Chatbot 13"


class ServerError(Exception):
    """raised when a server request fails"""
    pass


class Server:
    """
    an abstract server class
    """
    def list_model_names(self) -> list[str]:
        pass
    def generate_blocking(self, prompt, model) -> list[str]:
        """
        non-streaming generation - returns a list of text chunks
        """
        pass
    def generate_streaming(self, prompt, model) -> Iterator[str]:
        """
        streaming generation - yields text chunks
        """
        pass


class OllamaServer(Server):
    """
    for servers that comply with ollama's API
    """
    def __init__(self, name, url, username=None, password=None):
        self.name = name
        self.url = url
        self.username = username
        self.password = password

    def _authenticate_extra_args(self) -> dict:
        auth_args = {}
        if self.username is not None:
            auth_args = {
                'auth': (self.username, self.password)
            }
        return auth_args

    def list_model_names(self):
        url = f"{self.url}/api/tags"
        auth_args = self._authenticate_extra_args()
        print(f"Fetching model names from {url} with auth_args={auth_args}")
        try:
            answer = requests.get(url, **auth_args)
        except requests.exceptions.RequestException as exc:
            raise ServerError(f"cannot reach {url}: {exc}") from exc
        if not (200 <= answer.status_code < 300):
            raise ServerError(
                f"HTTP {answer.status_code} on {url}\n{answer.text[:200]}")
        raw = answer.json()
        return [model['name'] for model in raw['models']]

    def generate_blocking(self, prompt, model):
        url = f"{self.url}/api/generate"
        auth_args = self._authenticate_extra_args()
        payload = {'model': model, 'prompt': prompt}
        result = []

        try:
            answer = requests.post(url, json=payload, **auth_args)
        except requests.exceptions.RequestException as exc:
            raise ServerError(f"cannot reach {url}: {exc}") from exc
        if not (200 <= answer.status_code < 300):
            raise ServerError(
                f"HTTP {answer.status_code} on {url}\n{answer.text[:200]}")
        for line in answer.text.split("\n"):
            # splitting artefacts can be ignored
            if not line:
                continue
            # there should be no exception, but just in case...
            try:
                data = json.loads(line)
                # the last JSON chunk contains statistics and is not a message
                if data['done']:
                    break
                result.append(data['response'])
            except Exception as e:
                print(f"Exception {type(e)=}, {e=}")
        return result

    def generate_streaming(self, prompt, model):
        url = f"{self.url}/api/generate"
        auth_args = self._authenticate_extra_args()
        payload = {'model': model, 'prompt': prompt}

        try:
            answer = requests.post(url, json=payload, stream=True, **auth_args)
        except requests.exceptions.RequestException as exc:
            raise ServerError(f"cannot reach {url}: {exc}") from exc
        if not (200 <= answer.status_code < 300):
            raise ServerError(
                f"HTTP {answer.status_code} on {url}\n{answer.text[:200]}")
        for line in answer.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line)
                if data['done']:
                    return
                yield data['response']
            except Exception as e:
                print(f"Exception {type(e)=}, {e=}")


class LitellmServer(Server):
    """
    for servers that comply with LiteLLM's API
    """
    def __init__(self, name, url, key):
        self.name = name
        self.url = url
        self.key = key

    def _authenticate_headers(self) -> dict:
        if not self.key:
            return {}
        return dict(headers={"X-API-KEY": LITE_LLM_KEY})

    def list_model_names(self):
        url = f"{self.url}/models"
        extra_args = self._authenticate_headers()
        try:
            req = requests.get(url, **extra_args)
        except requests.exceptions.RequestException as exc:
            raise ServerError(f"cannot reach {url}: {exc}") from exc
        if not (200 <= req.status_code < 300):
            raise ServerError(
                f"HTTP {req.status_code} on {url}\n{req.text[:200]}")
        raw = req.json()
        return [
            chunk['id'] for chunk in raw['data']
        ]

    def generate_blocking(self, prompt, model):
        url = f"{self.url}/v1/completions"
        payload = {
            "model": model,
            "prompt": prompt,
        }
        try:
            req = requests.post(
                url,
                json=payload,
                **self._authenticate_headers()
            )
        except requests.exceptions.RequestException as exc:
            raise ServerError(f"cannot reach {url}: {exc}") from exc
        if not (200 <= req.status_code < 300):
            raise ServerError(
                f"HTTP {req.status_code} on {url}\n{req.text[:200]}")
        raw = req.json()
        result = []
        if 'choices' in raw:
            for choice in raw['choices']:
                result.append(choice['text'])
        return result


    def generate_streaming(self, prompt, model):
        url = f"{self.url}/v1/completions"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
        }
        try:
            req = requests.post(
                url,
                json=payload,
                stream=True,
                **self._authenticate_headers()
            )
        except requests.exceptions.RequestException as exc:
            raise ServerError(f"cannot reach {url}: {exc}") from exc
        if not (200 <= req.status_code < 300):
            raise ServerError(
                f"HTTP {req.status_code} on {url}\n{req.text[:200]}")
        for chunk in req.iter_lines():
            if not chunk:
                continue
            try:
                chunk = chunk.decode('utf-8')
                # remove extra 'data: ' prefix
                if chunk.startswith("data: "):
                    chunk = chunk[6:]
                data = json.loads(chunk)
                if 'choices' in data:
                    for choice in data['choices']:
                        yield choice['text']
            except Exception as e:
                print(f"Exception {type(e)=}, {e=}")


SERVERS = {}
for key, spec in SERVER_SPECS.items():
    match spec['type']:
        case 'ollama':
            SERVERS[key] = OllamaServer(
                name=spec['name'],
                url=spec['url'],
                username=spec.get('username', None),
                password=spec.get('password', None),
            )
        case 'litellm':
            SERVERS[key] = LitellmServer(
                name=spec['name'],
                url=spec['url'],
                key=spec['key'],
            )


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
        # we keep a cache of available models on each server
        self.model_names_per_server = {}

        header = ft.Text(value=TITLE, size=40)

        # a message area to display errors and status messages
        # placed between the title and the controls
        self.message_text = ft.Text(value="", color="grey", size=12)
        self.message_area = ft.Container(
            content=ft.Column(
                [self.message_text],
                scroll=ft.ScrollMode.AUTO,
                auto_scroll=True,
            ),
            width=float("inf"),
            height=60,
            border=ft.border.all(1, "grey"),
            border_radius=5,
            padding=5,
        )

        self.streaming = ft.Checkbox(label="streaming", value=True)
        #  will be populated later
        self.model = ft.Dropdown(
            # options=[],
            # width=300,
            expand=True,
        )
        self.server = ft.Dropdown(
            options=[ft.dropdown.Option(server)
                     for server in SERVER_SPECS.keys()],
            value=DEFAULT_SERVER,
            width=100,
            on_change=lambda event: self.update_models(),
        )

        self.submit = ft.ElevatedButton("Send", on_click=self.send_request)

        self.history = History(self)

        row = ft.Row(
            [self.streaming, self.model, self.server, self.submit],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        super().__init__(
            [header, self.message_area, row, self.history],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        # go fetch the relevant models for the selected server
        # as explained below, at this point we are not yet in the page
        # so we cannot yet call update() at this point
        self.update_models(update=False)

    def show_message(self, message):
        """display a message in the message area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"{timestamp} {message}"
        if self.message_text.value:
            self.message_text.value += f"\n{line}"
        else:
            self.message_text.value = line

    def fetch_models(self):
        # already fetched ?
        # if empty, try again
        if (self.server.value in self.model_names_per_server
            and self.model_names_per_server[self.server.value]):
            return
        server_instance = SERVERS[self.server.value]
        model_names = server_instance.list_model_names()
        # for usability: sort the models alphabetically
        model_names.sort()
        self.model_names_per_server[self.server.value] = model_names

    def update_models(self, *, update=True):
        # preserve current setting as far as possible
        current_model = self.model.value
        try:
            self.fetch_models()
        except (ServerError, requests.exceptions.RequestException) as exc:
            self.show_message(f"fetching models: {exc}")
            self.model_names_per_server[self.server.value] = []
            if update:
                self.update()
            return
        available_models = self.model_names_per_server[self.server.value]
        # replace the current options with the new ones
        self.model.options = [
            ft.dropdown.Option(model) for model in available_models
        ]
        # preserve setting if possible, otherwise pick first one
        if current_model in available_models:
            self.model.value = current_model
        else:
            # pick a mistral model by default
            for model in available_models:
                if model.startswith("mistral-"):
                    self.model.value = model
                    break
            # otherwise, pick the first model that not a 'all-...'
            # this is a workaround because somehow the first model on GPU
            # namely - all-minilm:22m-l6-v2-fp16
            # returns an error saying the model does not support generate
            else:
                self.model.value = next(
                    (model for model in available_models
                     if not model.startswith("all-")),
                    None,
                )
        # a subtle point here: because we call update_models in the constructor,
        # and because at that time the app is not yet in the page
        # we cannot call update() in that circumstance()
        # BUT since this method is bound the the 'change' event on the server widget
        # in that circumstance we need to update
        if update:
            self.update()

    def send_request(self, _event):
        # disable the button to prevent double submission
        # self.submit.disabled = True
        self.submit.style = ft.ButtonStyle(bgcolor="red")
        self.history.disable_prompt()
        self.send_request_2(_event)
        # self.submit.disabled = False
        self.submit.style = ft.ButtonStyle(bgcolor="green")
        self.history.enable_prompt()
        self.update()


    # send the prompt to the server and display the answer
    def send_request_2(self, _event):
        model = self.model.value
        prompt = self.history.current_prompt()
        server_instance = SERVERS[self.server.value]

        # record the question asked
        self.history.add_prompt(prompt)
        # create placeholder for the answer
        self.history.add_answer("")
        context = f"➡️ {server_instance.name} / {model}) ...\n"
        self.history.add_chunk(context)
        # update UI
        self.update()

        # send the request
        streaming = self.streaming.value

        print(f"Sending message to {server_instance.name}, {model=}, {streaming=}, {prompt=}")

        try:
            # streaming or non streaming
            if not streaming:
                # not streaming = blocking
                answers = server_instance.generate_blocking(prompt, model)
                for text in answers:
                    self.history.add_chunk(text)
                self.update()
            else:
                # streaming version
                answers = server_instance.generate_streaming(prompt, model)
                for text in answers:
                    self.history.add_chunk(text)
                    self.update()
        except (ServerError, requests.exceptions.RequestException) as exc:
            self.show_message(f"send request: {exc}")
            self.update()


def main(page: ft.Page):
    page.title = TITLE

    chatbot = ChatbotApp()
    page.add(chatbot)


ft.app(target=main)
