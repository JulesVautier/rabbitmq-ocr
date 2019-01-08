from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .document_manager import DocumentManager
from .rpc_client import ClientRpc
from .models import OcrRequest, OcrResult, Document
from .forms import DocumentForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def ocr_view(request):
    req = OcrRequest(name='test')
    req.save()

    client_rpc = ClientRpc()
    client_rpc.call(req.id, '1')

    res = OcrRequest.objects.all()
    view = ""
    for request in res:
        view = view + str(request.__repr__()) + '<br>'

    return HttpResponse(view)


def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', {'documents': documents})


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document_manager = DocumentManager()
            for filename, file in request.FILES.items():
                document_manager.save(file)
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })
