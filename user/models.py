from django.db import models

from django.db import models
from django.contrib.auth.hashers import check_password, make_password


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=25)
    name = models.CharField(max_length=25)
    accountname = models.CharField(max_length=25, unique=True)
    studentid = models.CharField(max_length=25)
    passwd = models.CharField(max_length=128)

    def isright(self, password):
        return password == self.passwd or check_password(password, self.passwd)
