from django.http import HttpResponse

from .rpc_client import ClientRpc


def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")

def ocr(request):
    client_rpc = ClientRpc()
    client_rpc.call(30)
    return HttpResponse('ok mdr')