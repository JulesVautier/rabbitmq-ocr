import subprocess
from time import sleep

from django.apps import AppConfig


class OcrDispatcherConfig(AppConfig):
    name = 'ocr_dispatcher'

    # subprocess.call(['python', 'rpc_client.py'])