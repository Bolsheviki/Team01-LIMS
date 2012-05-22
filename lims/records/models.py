from django.db import models


# Create your models here.
class Book(models.Model):
    isbn = models.BigIntegerField();
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    retrieval = models.CharField(max_length=30)
    publisher = models.CharField(max_length=100)
    abstract = models.TextField(blank=True, max_length=500)
    image = models.ImageField(upload_to=None)
    
    authors = models.ManyToManyField(Author)

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


class User(models.Model):
    UTYPE_CHOICES = (
        (u'N', u'Normal User'),
        (u'C', u'Cpunter Administrator'),
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
    utype = models.CharField(choices=UTYPE_CHOICES)
    level = models.CharField(choices=LEVEL_CHOICES)
    debt = models.IntegerField()


class Recored(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)


class Author(models.Model):
    ROLE_CHOICES = (
        (u'W', u'Writer'),
        (u'T', u'Translator'),
    )
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    
    def __unicode__(self):
        return u'%s %s' % (self.name, self.role)

