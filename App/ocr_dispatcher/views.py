from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .file_manager import DocumentManager
from .rpc_client import ClientRpc
from .models import OcrRequest, OcrResult
from .forms import DocumentForm

def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")

def ocr_view(request):
    #TODO save files

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
    # documents = Document.objects.all()
    documents = None
    return render(request, 'home.html', { 'documents': documents })

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            fs = FileSystemStorage()
            for filename, file in request.FILES.items():
                name = request.FILES[filename].name
                filename = fs.save(name, file)
                print(filename)
            print(form)
            print(request.FILES)
            # fs = FileSystemStorage()
            # filename = fs.save(myfile.name, myfile)
            # uploaded_file_url = fs.url(filename)
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print('\n _________________FILE_MANAGER_DEV___________________________  \n')

            document_manager = DocumentManager()
            print(request.FILES['file'])
            # document_manager.open('/tmp/archive.zip')
            document_manager.open(request.FILES['file'])
            # document_manager.open('/tmp/file.pdf')
            document_manager.save_documents()
            return HttpResponseRedirect('/success/url/')

            print('\n ________________________END_________________________________  \n')
        else:
            print(form.is_valid())
            print(form)

    else:
        form = UploadFileForm()
    return render(request, 'simple_upload.html', {'form': form})