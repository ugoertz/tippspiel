from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.translation import get_language

from hvad.models import TranslatableModel, TranslatedFields


class Flatpage(TranslatableModel):

    translations = TranslatedFields(
        url = models.CharField(max_length=200, blank=True, verbose_name=_('URL')),
        title = models.CharField(max_length=200, blank=True, verbose_name=_('Titel')),
        content = models.TextField(blank=True, verbose_name=_('Inhalt')),
        )

    def __unicode__(self):
        return '%s' % self.url

