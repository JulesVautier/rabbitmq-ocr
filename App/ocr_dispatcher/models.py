from rest_framework import serializers
from django.db import models

class OcrRequest(models.Model):
    name = models.CharField(max_length=50)
    timestamp_created = models.DateTimeField(auto_now_add=True, blank=True)
    timestamp_finished = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=30, default='WAITING')
    number_files = models.IntegerField(default=1)


    def __repr__(self):
        return 'OcrRequest(id={self.id} name={self.name!r}) status={self.status}'.format(self=self)

    class Meta:
        db_table = 'ocr_request'


class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    type = models.CharField(max_length=20, default='pdf')
    syndic_id = models.IntegerField(blank=True, null=True)
    copro_id = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'document'


# class File(models.Model):
#     description = models.CharField(max_length=255, blank=True)
#     document = models.FileField(upload_to='documents/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)


class OcrResult(models.Model):
    ocr_request = models.ForeignKey(OcrRequest, on_delete=models.CASCADE)
    result = models.TextField()
    file = models.ForeignKey(Document, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='WAITING')


    class Meta:
        db_table = 'ocr_result'


class OcrResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcrResult
        fields = '__all__'

    def create(self, validated_data):
        return OcrResult(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
