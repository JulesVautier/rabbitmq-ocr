from django.http import HttpResponse

from .rpc_client import ClientRpc
from .models import OcrRequest, OcrResult

def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")

def ocr(request):
    req = OcrRequest(name='issou')
    req.save()
    client_rpc = ClientRpc()
    client_rpc.call(req.id, '1')

    res = OcrRequest.objects.all()
    view = ""
    for request in res:
        view = view + str(request.__repr__()) + '<br>'

    return HttpResponse(view)