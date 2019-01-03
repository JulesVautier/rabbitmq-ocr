from marshmallow_sqlalchemy import ModelSchema
from ..model import ocr_request

class OcrRequestSchema(ModelSchema):
    class Meta:
        model = ocr_request.OcrRequest

class OcrResultSchema(ModelSchema):
    class Meta:
        model = ocr_request.OcrResult

ocr_request_schema = OcrRequestSchema()
ocr_result_schema = OcrResultSchema()