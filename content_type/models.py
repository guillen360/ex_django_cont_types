from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.

class Notes(models.Model):

    table_name = models.ForeignKey(ContentType)
    table_id = models.PositiveIntegerField()

    table_obj = generic.GenericForeignKey('table_name', 'table_id')

    comment = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{0}'.format(self.comment)

class Mammal(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)


    _notes = None

    def talk(self):
        pass

    @property
    def comment(self):
        n = self.get_notes()
        if n:
            return n[0].comment
        else:
            return ''

    def get_notes(self):
        if self._notes:
            return self._notes

        ctype = ContentType.objects.get_for_model(self.__class__)

        try:
            self._notes = Notes.objects.filter(table_name__pk=ctype.id, table_id=self.id)
        # except Notes.DoesNotExist:
        except:
            return None

        if self._notes:
            return self._notes
        else:
            return None



    class Meta:
        abstract = True

class Duck(Mammal):
    type = models.CharField(max_length=255)

    def talk(self):
        return 'Quack, quack'

class Dog(Mammal):
    breed = models.CharField(max_length=255)

    def talk(self):
        return 'bark... bark'


