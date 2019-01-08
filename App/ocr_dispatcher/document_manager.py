import datetime
import os
import shutil
import time
import zipfile

from django.core.files import File
from django.core.files.storage import FileSystemStorage

from .models import Document


class DocumentManager(object):

    def __init__(self):
        self.files = []
        self.archive_extensions = ('.zip')
        self.extraction_path = './tmp_dir/'
        self.fs = FileSystemStorage()
        pass

    def archive_manager(self, file):
        print('archive_manager ', file.name)
        with zipfile.ZipFile(file) as archive:
            # Add date to the folder name to have an unique name
            st = datetime.datetime.fromtimestamp(time.time()).strftime('_%Y-%m-%d-%H-%M-%S')
            extract_dir = file.name.split('.')[0] + str(st) + '/'
            archive.extractall(self.extraction_path + extract_dir)
            return extract_dir

    def directory_manager(self, directory):
        document_list = []
        for root, dirs, files in os.walk(self.extraction_path + directory):
            path = root + '/'
            for file in files:
                local_file = open(path + file, 'rb')
                django_file = File(local_file)
                document_list.append(self.file_manager(path + file, django_file))
                local_file.close()
        return document_list

    def file_manager(self, filename, django_file):
        doc = Document(name=os.path.basename(filename))
        doc.document.save('test', django_file)
        doc.save()
        return doc

    def open(self, file):
        """ Open a django.File an return an array of models.Documents
        The file can be a single file or a Zip archive.
        The single file or all files from archives will be uploaded according to django settings
        """
        document_list = []
        if (file.name.endswith(self.archive_extensions)):
            extract_dir = self.archive_manager(file)
            document_list = self.directory_manager(extract_dir)
            shutil.rmtree(extract_dir)  # delete the temporary directory
        else:
            document_list.append(self.file_manager(file.name, file))
        return document_list
