from django.db import models

class OcrRequest(models.Model):
    name = models.CharField(max_length=50)
    timestamp_created = models.DateTimeField(auto_now_add=True, blank=True)
    timestamp_finished = models.DateTimeField(blank=True)

    def __repr__(self):
        return '<OcrRequest(id={self.id} name={self.name!r})>'.format(self=self)

    class Meta:
        db_table = 'ocr_request'

class OcrResult(models.Model):
    result = models.TextField()
    ocr_request_id = models.ForeignKey(OcrRequest, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ocr_result'
