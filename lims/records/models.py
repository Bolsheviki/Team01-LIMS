from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    isbn = models.BigIntegerField();
    name = models.CharField(max_length=100)
    category = models.CharField(blank=True, max_length=30)
    retrieval = models.CharField(blank=True, max_length=30)
    publisher = models.CharField(blank=True, max_length=100)
    image = models.FileField(null=True, upload_to='image/%Y/%m/%d')
    authors = models.CharField(blank=True, max_length=100)
    abstract = models.TextField(blank=True, max_length=500)

    def __unicode__(self):
        return self.name


class BookInstance(models.Model):
    STATE_CHOICES = (
        (u'B', u'Borrowed'),
        (u'U', u'UnBorrowed'),
        (u'D', u'Discard'),
    )
    book = models.ForeignKey(Book)
    state = models.CharField(max_length=10, choices=STATE_CHOICES,
                             default='U')
    renewal = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s(%d)' % (self.book.name, self.id)

class Record(models.Model):
    ACTION_CHOICES = (
        (u'B', u'Borrow'),
        (u'R', u'Return'),
    )
    booki = models.ForeignKey(BookInstance)
    user = models.ForeignKey(User)
    action = models.CharField(max_length=2, choices=ACTION_CHOICES)
    time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s %s' % (self.user.username, self.booki)


class Borrow(models.Model):
    user = models.ForeignKey(User)
    record = models.ForeignKey(Record)

    def __unicode__(self):
        return self.record.__unicode__()


class UserProfile(models.Model):
    LEVEL_CHOICES = (
        (u'U', u'undergraduate'),
        (u'G', u'graduate'),
        (u'S', u'staff'),
    )
    user = models.ForeignKey(User, unique = True)
    level = models.CharField(null=True, max_length=2,
                             choices=LEVEL_CHOICES, default='U')
    debt = models.IntegerField(default = 0)

    def __unicode__(self):
        return '%s %s %s' % (self.user, self.level, self.debt)
