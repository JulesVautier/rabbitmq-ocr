
ARCHIVE_EXTENSIONS = ('.zip', '.tar', '.tar.gz')

class DocumentManager(object):

    def __init__(self):
        self.files = []
        pass

    def archive_manager(self, archive: str):

        pass

    def pdf_manager(self, file: str):
        self.files.append(file)
        pass

    def open(self, file: str):
        print(file)
        if (file.endswith('.pdf')):
            self.pdf_manager(file)
        elif (file.endswith(ARCHIVE_EXTENSIONS)):
            self.archive_manager(file)
        pass

    def save_documents(self):
        for file in self.files:
            print(file)
            #TODO save in DB
            #TODO save in google cloud
            pass
        pass
    #return array [ Documents ]

