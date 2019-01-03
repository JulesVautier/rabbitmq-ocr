import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

engine = sa.create_engine('sqlite:///:memory:')
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

class OcrRequest(Base):
    __tablename__ = 'ocr_request'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    timestamp_created = sa.Column(sa.DateTime)
    timestamp_finished = sa.Column(sa.DateTime)

    def __repr__(self):
        return '<OcrRequest(id={self.id} name={self.name!r})>'.format(self=self)

class OcrResult(Base):
    __tablename__ = 'ocr_result'
    id = sa.Column(sa.Integer, primary_key=True)
    result = sa.Column(sa.JSON)
    ocr_request_id = sa.Column(sa.Integer, sa.ForeignKey('ocr_request.id'))
    ocr_request = relationship("OcrRequest", backref=backref('ocr_result'))

Base.metadata.create_all(engine)