from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class UserOrig(models.Model):
    email = models.CharField(max_length=200)
    files_directory = models.CharField(max_length=200)

    def __str__(self):
        return self.email


class Picture(models.Model):
    #user = models.ForeignKey(UserOrig, related_name='pictures', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='pictures', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200)
    highlighted = models.TextField()

    #def __str__(self):
    #    return self.user.email + ' ' + self.file_name

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
