from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=30, unique=True);
    title = models.CharField(max_length=100)
    authors = models.CharField(blank=True, max_length=100)
    translators = models.CharField(blank=True, max_length=100)
    publisher = models.CharField(blank=True, max_length=100)
#    category = models.CharField(unique=True, blank=True, max_length=30)
#    retrieval = models.CharField(unique=True, blank=True, max_length=30)

    def __unicode__(self):
        return self.title

LEVEL_CHOICES = (
    (u'U', u'undergraduate'),
    (u'G', u'graduate'),
    (u'S', u'staff'),
)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    level = models.CharField(null=True, max_length=2,
                             choices=LEVEL_CHOICES, default='U')
    debt = models.IntegerField(default = 0)

    def __unicode__(self):
        return '%s %s %s' % (self.user, self.level, self.debt)


class BookInstance(models.Model):
    STATE_CHOICES = (
        (u'B', u'Borrowed'),
        (u'U', u'UnBorrowed'),
        (u'D', u'Discard'),
    )
    book = models.ForeignKey(Book)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='U')
    removed = models.BooleanField(default=False)
    renewal = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s(%d)%s' % (self.book.title, self.id, '--removed' if self.removed else '')


class Record(models.Model):
    ACTION_CHOICES = (
        (u'B', u'Borrow'),
        (u'R', u'Return'),
    )
    booki = models.ForeignKey(BookInstance)
    user = models.ForeignKey(UserProfile)
    action = models.CharField(max_length=2, choices=ACTION_CHOICES)
    time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s %s' % (self.user.user.username, self.booki)


class Borrow(models.Model):
    user = models.ForeignKey(UserProfile)
    record = models.ForeignKey(Record)

    def __unicode__(self):
        return self.record.__unicode__()

