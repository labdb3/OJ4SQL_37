from django.db import models
import user.models as user_models
from django.utils.translation import gettext_lazy as _


class Problem(models.Model):
    class JudgeType(models.TextChoices):
        UNDEFINED = 'UN', _('undefined')
        ORDERED = 'OD', _('ordered')
        UNORDERED = 'UD', _('unordered')
        ORDERED_DECIMALQ = 'OQ', _('ordered_decimalq')
        UNORDERED_DECIMALQ = 'UQ', _('unordered_decimalq')
        CUSTOM = 'CM', _('custom')
    pid = models.AutoField(primary_key=True)
    gid = models.ForeignKey('Group', on_delete=models.CASCADE)
    description = models.TextField()
    title = models.CharField(max_length=50)
    mysql = models.TextField(default='', blank=True)
    postgresql = models.TextField(default='', blank=True)
    opengauss = models.TextField(default='', blank=True)
    judge = models.CharField(
        max_length=2, choices=JudgeType.choices, default=JudgeType.UNDEFINED)
    judge_kwargs = models.TextField(default='', blank=True)
    testdb = models.CharField(max_length=16, default=None, blank=False)
    difficulty = models.SmallIntegerField(default=0, blank=True)
    invisible = models.BooleanField(default=False, blank=True)


class Group(models.Model):
    class EchoType(models.TextChoices):
        NOEVAL_NOANS = 'NN', _('noeval_noans')
        NOEVAL_ANS = 'NY', _('noeval_ans')
        EVAL_NOANS = 'YN', _('eval_noans')
        EVAL_ANS = 'YY', _('eval_ans')

    class PermChoice(models.TextChoices):
        OPEN = 'O', _('open')
        READ = 'R', _('read')
        UNSEEN = 'U', _('unseen')
    gid = models.AutoField(primary_key=True)
    gname = models.CharField(max_length=16, default='')
    description = models.TextField(default='', blank=True)
    basedescription = models.TextField(default='', blank=True)
    exec_user = models.BooleanField(default=False)
    do_eval = models.BooleanField(default=False)
    display_anssql = models.BooleanField(default=False)
    echo_result = models.BooleanField(default=False)
    perm = models.CharField(
        max_length=1, choices=PermChoice.choices, default=PermChoice.UNSEEN)
    savesubmission = models.BooleanField(default=True)


class UserGroup(models.Model):
    uid = models.ForeignKey('user.User', on_delete=models.CASCADE)
    gid = models.ForeignKey('Group', on_delete=models.CASCADE)


class Submission(models.Model):
    sid = models.AutoField(primary_key=True)
    uid = models.ForeignKey('user.User', on_delete=models.CASCADE)
    pid = models.ForeignKey('Problem', on_delete=models.CASCADE)
    code = models.TextField()
    resulttype = models.IntegerField(blank=True, null=True)
    info = models.TextField()
    timespent = models.SmallIntegerField(blank=True, null=True)
    datetime = models.DateTimeField()
    lang_type = models.CharField(max_length=16)
    user_result = models.TextField(default='', blank=True)
