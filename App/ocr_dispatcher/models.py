from django.db import models

class OcrRequest(models.Model):
    name = models.CharField(max_length=50)
    timestamp_created = models.DateTimeField(auto_now_add=True, blank=True)
    timestamp_finished = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=30, default='WAITING')
    number_files = models.IntegerField(default=1)


    def __repr__(self):
        return 'OcrRequest(id={self.id} name={self.name!r}) Status={self.status}'.format(self=self)

    class Meta:
        db_table = 'ocr_request'


class File(models.Model):
    name = models.TextField(default='test_file')
    path = models.TextField(default='very/long/path')
    type = models.CharField(max_length=20, default='pdf')
    syndic_id = models.IntegerField(default=1)
    copro_id = models.IntegerField(default=1)

    class Meta:
        db_table = 'file'


class OcrResult(models.Model):
    ocr_request = models.ForeignKey(OcrRequest, on_delete=models.CASCADE)
    result = models.TextField()
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    syndic_id = models.IntegerField(default=1)
    copro_id = models.IntegerField(default=1)

    class Meta:
        db_table = 'ocr_result'

