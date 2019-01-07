import sys

import django
from django.apps import AppConfig



class OcrDispatcherConfig(AppConfig):
    name = 'ocr_dispatcher'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True

        # from .rpc_listener import ListenerRpc
        #
        # listener = ListenerRpc()
        # listener.start()

        from .file_manager import DocumentManager
