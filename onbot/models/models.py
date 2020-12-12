from tortoise import fields
from tortoise.models import Model


class Question(Model):
    id = fields.IntField(pk=True)
    question = fields.TextField()
    answer = fields.TextField()
    temp_answer = fields.TextField(null=True)


class User(Model):
    id = fields.IntField(pk=True)
    uid = fields.BigIntField(unique=True)
    name = fields.TextField()
    uname = fields.CharField(max_length=100, unique=True, null=True)
