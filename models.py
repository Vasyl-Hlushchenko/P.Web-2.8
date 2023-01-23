from mongoengine import Document, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField


class Authors(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Qoutes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    qoute = StringField()
