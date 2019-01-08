import datetime
import os
import time
import zipfile

from django.core.files import File
from django.core.files.storage import FileSystemStorage

# from App.App import settings
from .models import Document

ARCHIVE_EXTENSIONS = ('.zip')
EXTRACTION_PATH = './tmp_dir/'


class DocumentManager(object):

    def __init__(self):
        self.files = []
        self.archive_extensions = ARCHIVE_EXTENSIONS
        self.extraction_path = EXTRACTION_PATH
        self.fs = FileSystemStorage()
        pass

    # TODO CHECK NAME FUNCTION

    def archive_manager(self, file):
        print('archive_manager ', file.name)
        with zipfile.ZipFile(file) as archive:
            # Add date to the folder name to have an unique name
            st = datetime.datetime.fromtimestamp(time.time()).strftime('_%Y-%m-%d-%H-%M-%S')
            extract_dir = file.name.split('.')[0] + str(st) + '/'
            archive.extractall(self.extraction_path + extract_dir)
            return extract_dir

    def directory_manager(self, directory):
        for root, dirs, files in os.walk(EXTRACTION_PATH + directory):
            path = root + '/'
            for file in files:
                local_file = open(path + file, 'rb')
                django_file = File(local_file)
                self.file_manager(path + file, django_file)
                # local_file.close()


    def file_manager(self, filename, django_file):
        print('file_manager', filename)
        doc = Document(name = os.path.basename(filename))
        # doc.document.save(os.path.basename(filename), django_file)
        doc.document.save('test', django_file)
        doc.save()
        print('saved ', doc.document.name)
        pass

    def open(self, file):
        print('___________ open ', file.name)
        file_name = file.name
        if (file_name.endswith(ARCHIVE_EXTENSIONS)):
            extract_dir = self.archive_manager(file)
            self.directory_manager(extract_dir)
        else:
            self.file_manager(file.name, file)
        pass

    def save_documents(self):
        for file in self.files:
            print(file)
            # TODO save in DB
            # save in DB in tmp then in id/name
            # TODO save in google cloud
            pass
        pass
    # return array [ Documents ]
