from django.db import models


# Create your models here.
class Book(models.Model):
    isbn = models.BigIntegerField();
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    retrieval = models.CharField(max_length=30)
    publisher = models.CharField(max_length=100)
    image = models.FileField(upload_to='image/%Y/%m/%d')
    authors = models.CharField(max_length=100)
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
    state = models.CharField(max_length=10, choices=STATE_CHOICES)
    renewal = models.BooleanField()

    def __unicode__(self):
        return book.name


class User(models.Model):
    UTYPE_CHOICES = (
        (u'N', u'Normal User'),
        (u'C', u'Counter Administrator'),
        (u'U', u'User Administrator'),
        (u'B', u'Book Administrator'),
    )
    LEVEL_CHOICES = (
        (u'U', u'undergraduate'),
        (u'G', u'graduate'),
        (u'S', u'staff'),
    )
    uid = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    utype = models.CharField(max_length=2, choices=UTYPE_CHOICES)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    debt = models.IntegerField()
    
    def __unicode__(self):
        return user.name


class Record(models.Model):
    ACTION_CHOICES = (
        (u'B', u'Borrow'),
        (u'R', u'Return'),
    )
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=2, choices=ACTION_CHOICES)


class Borrow(models.Model):
    user = models.ForeignKey(User)
    record = models.ForeignKey(Record)

