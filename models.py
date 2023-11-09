from mongoengine import Document, StringField, ListField, ReferenceField


# Модель для колекції 'authors'

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=30)
    born_location = StringField(max_length=100)
    description = StringField()
    meta = {'allow_inheritance': True}


# Модель для колекції 'quotes'

class Quote(Document):
    tags = ListField(StringField(max_length=200))
    author = ReferenceField(Author)
    quote = StringField()
    meta = {'allow_inheritance': True}