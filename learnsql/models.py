from django.db import models

# Create your models here.
class Problems(models.Model):
    pid = models.AutoField(primary_key=True)
    ptitle = models.CharField(max_length=50)
    pdesc = models.TextField()
    mysql = models.TextField()
    postgresql = models.TextField()


class Topics(models.Model):
    topicID = models.IntegerField(primary_key=True)
    topicName = models.CharField(max_length=25)
    topicDesc = models.CharField(max_length=50)
    topicOrd = models.IntegerField()
    topicParent = models.IntegerField()

class TopicProblem(models.Model):
    topicID = models.ForeignKey('Topics',on_delete=models.CASCADE)
    pid = models.ForeignKey('Problems',on_delete=models.CASCADE)


class Tables(models.Model):
    tableName = models.CharField(max_length=32,primary_key=True)
    tableDesc = models.TextField()


class ProblemTable(models.Model):
    pid = models.ForeignKey('Problems',on_delete=models.CASCADE)
    tableName = models.ForeignKey('Tables',on_delete=models.CASCADE)


class User(models.Model):
    uid = models.ForeignKey('user.User',on_delete=models.CASCADE)
    mysqlUserName = models.CharField(max_length=25)
    mysqlUserPassWord = models.CharField(max_length=25)
    mysqlDBName = models.CharField(max_length=25)

    postgresqlUserName = models.CharField(max_length=25)
    postgresqlUserPassWord = models.CharField(max_length=25)
    postgresqlSchemaName = models.CharField(max_length=25)

