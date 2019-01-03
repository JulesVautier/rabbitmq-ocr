from django.http import HttpResponse

from .rpc_client import ClientRpc
from .models import OcrRequest, OcrResult

def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")

def ocr(request):
    client_rpc = ClientRpc()
    client_rpc.call(30)
    req = OcrRequest(name='issou')
    req.save()

    res = OcrRequest.objects.all()
    print(res)
    return HttpResponse(str(res))