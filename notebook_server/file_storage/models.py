from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from private_storage.fields import PrivateFileField
from django.dispatch import dispatcher
from django.db.models import signals




class CustomFileFieldOld(models.FileField):
    """Allows model instance to specify upload_to dynamically.

    Model class should have a method like:

        def get_upload_to(self, attname):
            return 'path/to/%d' % self.id

    Based on: http://code.djangoproject.com/wiki/CustomUploadAndFilters
    """

    def __init__(self, *args, **kwargs):
        if not 'upload_to' in kwargs:
            kwargs['upload_to'] = 'dummy'
        self.prime_upload = kwargs.get('prime_upload', False)
        if 'prime_upload' in kwargs:
            del (kwargs['prime_upload'])
        super(CustomFileFieldOld, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        """Hook up events so we can access the instance."""
        super(CustomFileFieldOld, self).contribute_to_class(cls, name)
        if self.prime_upload:
            dispatcher.connect(self._get_upload_to, signals.post_init, sender=cls)
        dispatcher.connect(self._get_upload_to, signals.pre_save, sender=cls)

    def _get_upload_to(self, instance=None):
        """Get dynamic upload_to value from the model instance."""
        if hasattr(instance, 'get_upload_to'):
            self.upload_to = instance.get_upload_to(self.attname)

 #   def db_type(self):
  #      """Required by Django for ORM."""
   #     return 'varchar(100)'


class CustomFileField(models.FileField):
    """Allows model instance to specify upload_to dynamically.

    Model class should have a method like:

        def get_upload_to(self, attname):
            return 'path/to/%d' % self.id

    Based on: http://code.djangoproject.com/wiki/CustomUploadAndFilters
    """

    def contribute_to_class(self, cls, name):
        """Hook up events so we can access the instance."""
        super(CustomFileField, self).contribute_to_class(cls, name)
      #  dispatcher.connect(self._post_init, signals.post_init, sender=cls)

    def _post_init(self, instance=None):
        """Get dynamic upload_to value from the model instance."""
        if hasattr(instance, 'get_upload_to'):
            self.upload_to = instance.get_upload_to(self.attname)




class CustomImageField(models.FileField):
    """Allows model instance to specify upload_to dynamically.

    Model class should have a method like:

        def get_upload_to(self, attname):
            return 'path/to/%d' % self.id

    Based on: http://code.djangoproject.com/wiki/CustomUploadAndFilters
    """
    def __init__(self, *args, **kwargs):
        if not 'upload_to' in kwargs:
            kwargs['upload_to'] = 'dummy'
        self.prime_upload = kwargs.get('prime_upload', False)
        if 'prime_upload' in kwargs:
            del(kwargs['prime_upload'])
        super(CustomImageField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """Hook up events so we can access the instance."""
        super(CustomImageField, self).contribute_to_class(cls, name)
        if self.prime_upload:
            signals.post_init.connect(self._get_upload_to, sender=cls)
        signals.pre_save.connect(self._get_upload_to, sender=cls)

    def _get_upload_to(self, instance=None, **kwargs):
        """Get dynamic upload_to value from the model instance."""
        if hasattr(instance, 'get_upload_to'):
            self.upload_to = instance.get_upload_to(self.attname)



class UserOrig(models.Model):
    email = models.CharField(max_length=200)
    files_directory = models.CharField(max_length=200)

    def __str__(self):
        return self.email


class Picture(models.Model):
    #user = models.ForeignKey(UserOrig, related_name='pictures', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='pictures', on_delete=models.CASCADE)
    file_name = models.TextField()
    highlighted = models.TextField()

    #def __str__(self):
    #    return self.user.email + ' ' + self.file_name

    def get_upload_to(self, attname):
        return '%s' % self.owner.username

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def save(self, *args, **kwargs):
    """
    Use the `pygments` library to create a highlighted HTML
    representation of the code snippet.
    """
    lexer = get_lexer_by_name(self.language)
    linenos = self.linenos and 'table' or False
    options = self.title and {'title': self.title} or {}
    formatter = HtmlFormatter(style=self.style, linenos=linenos,
                              full=True, **options)
    self.highlighted = highlight(self.code, lexer, formatter)
    super(Picture, self).save(*args, **kwargs)
