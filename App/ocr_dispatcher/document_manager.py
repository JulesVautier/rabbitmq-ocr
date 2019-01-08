import datetime
import os
import shutil
import time
import zipfile

from django.core.files import File
from django.core.files.storage import FileSystemStorage

from .models import Document


class DocumentManager(object):
    """
    Class to manage single files, directories or archives
    It create models.Document instances for each files
    Usage: document_list = DocumentManager.save('archive.zip')
    """

    def __init__(self):
        self.archive_extensions = ('.zip')
        self.extraction_path = '/tmp/tmp_dir/'
        self.fs = FileSystemStorage()
        self.document_list = []
        pass

    def save(self, file):
        """ Main function: Open a django.File an return the array of models.Documents saved.
        The file can be a single file or a Zip archive.
        The single file or all files from archives will be uploaded according to django's settings
        """
        document_list = []
        if (file.name.endswith(self.archive_extensions)):
            extract_dir = self.archive_manager(file)
            document_list = self.directory_manager(extract_dir)
            shutil.rmtree(extract_dir)  # delete the temporary directory
        else:
            document_list.append(self.file_manager(file))
        return document_list

    def archive_manager(self, file):
        """
        Extract an archive and return the directory name.
        """
        with zipfile.ZipFile(file) as archive:
            # Add date to the folder name to have an unique name
            st = datetime.datetime.fromtimestamp(time.time()).strftime('_%Y-%m-%d-%H-%M-%S')
            extract_dir = file.name.split('.')[0] + str(st) + '/'
            archive.extractall(self.extraction_path + extract_dir)
            return self.extraction_path + extract_dir

    def directory_manager(self, directory):
        """
        Walk recursively through a directory and call file_manager for each each.
        It return a list of all the models.Document created
        """
        document_list = []
        for root, dirs, files in os.walk(self.extraction_path + directory):
            path = root + '/'
            for file in files:
                local_file = open(path + file, 'rb')
                django_file = File(local_file)
                new_document = self.file_manager(django_file)
                document_list.append(new_document)
                local_file.close()
        return document_list

    def file_manager(self, django_file):
        """
        Create a models.Document
        """
        doc = Document(name=os.path.basename(django_file.name))
        doc.document.save(os.path.basename(django_file.name), django_file)
        doc.save()
        self.document_list.append(doc)
        return doc
