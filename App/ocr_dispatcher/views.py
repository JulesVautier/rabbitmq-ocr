from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .file_manager import DocumentManager
from .rpc_client import ClientRpc
from .models import OcrRequest, OcrResult, Document
from .forms import DocumentForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def ocr_view(request):
    # TODO save files

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
            print(form)
            form.save()
            fs = FileSystemStorage()
            for filename, file in request.FILES.items():
                name = file.name
                fs.save(file.name, file)
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })
