import sys

import django
from django.apps import AppConfig



class OcrDispatcherConfig(AppConfig):
    name = 'ocr_dispatcher'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True

        # from .rpc_client import ClientRpc
        # from .models import OcrRequest
        #
        # req = OcrRequest(name='issou')
        # req.save()
        # client_rpc = ClientRpc()
        # client_rpc.call(req.id, '1')

        from .rpc_listener import ListenerRpc

        listener = ListenerRpc()
        listener.start()
