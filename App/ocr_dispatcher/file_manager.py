import datetime
import os
import time
import zipfile

from .models import Document

ARCHIVE_EXTENSIONS = ('.zip')
EXTRACTION_PATH = './tmp_dir/'

class DocumentManager(object):

    def __init__(self):
        self.files = []
        pass


# TODO CHECK NAME FUNCTION

    def archive_manager(self, file):
        print('archive_manager ', file.name)
        with zipfile.ZipFile(file, "r") as archive:
            #Add date to the folder name to have an unique name
            st = datetime.datetime.fromtimestamp(time.time()).strftime('_%Y-%m-%d-%H-%M-%S')
            folder_name = file.name.split('.')[0] + str(st) + '/'
            archive.extractall(EXTRACTION_PATH + folder_name)
            return folder_name

    def file_manager(self, file):
        print('file_maneger', file)
        self.files.append(file)
        doc = Document(document=file)
        doc.save()
        pass

    def open(self, file):
        print('___________ open ', file.name)
        file_name = file.name
        if (file_name.endswith(ARCHIVE_EXTENSIONS)):
            self.archive_manager(file)
        else:
            self.file_manager(file)
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
