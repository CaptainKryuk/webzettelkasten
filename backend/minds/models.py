from django.db import models
from base.models import AbstractDateTimeModel
from django.template.defaultfilters import slugify

import datetime
import re

import random

# Create your models here.
class Idea(AbstractDateTimeModel):
    """
    Main class includes text etc
    """
    title = models.CharField("Заголовок идеи", max_length=255, blank=True)

    slug = models.SlugField(max_length=255, blank=True)

    text = models.TextField("Весь текст", blank=True)

    tags = models.ManyToManyField("minds.Tag", verbose_name="Тэги", blank=True)

    base_name = models.CharField("Сокращенное имя", max_length=255, blank=True)

    status = models.CharField("Статус идеи", choices=(('draft', 'draft'), ('completed', 'completed')), default='draft', max_length=255)

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        self.slug = slugify(self.title)
        self.base_name = '-'.join([re.sub(r'\W', r'-', self.title), str(now.day), str(now.month), str(now.year)])
        super(Idea, self).save(*args, **kwargs)
    
    def update_tags(self, new_tags: list):
        if len(new_tags) > self.tags.count():
            self.add_tag_list(new_tags)
            return 
        self.find_remove_tag(new_tags)
    
    def find_remove_tag(self, new_tags: list):
        for tag in self.tags.all():
            if not tag in new_tags:
                self.remove_tag(tag)

    def add_tag_list(self, tag_list: list):
        for tag in tag_list:
            self.add_tag(tag)

    def add_tag(self, name: str):
        exist_tag = Tag.objects.filter(name=name).first()
        if exist_tag:
            self.tags.add(exist_tag)
            return
        
        # create new tag
        new_tag = Tag(name=name)
        new_tag.save()
        self.tags.add(new_tag)
    
    def remove_tag(self, name):
        """ delete tag from idea """
        tag = Tag.objects.filter(name=name).first()
        if tag and tag in self.tags.all():
            self.tags.remove(tag.id)

    class Meta:
        ordering = ('-created',)


class Tag(models.Model):
    name = models.CharField("Имя тэга", max_length=100)

    color = models.CharField("Цвет тэга", max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id', )

    def save(self):
        if not self.pk:
            colors = [
                '#CFC5E7',
                '#DDC0E5',
                '#E6CAEB',
                '#EBDEF0',
                '#E0D7F0',
                '#C6CCE9',
                '#D1DEE8',
                '#BDD7F1',
                '#C9E5FC',
                '#DFF0FD',
                '#BDE3DB',
                '#C0EBE2',
                '#D8F3EE',
                '#C0E1CE',
                '#C4F0D6',
                '#DBF6E7',
                '#DAD6BD',
                '#E2E2C2',
                '#EDEFC7',
                '#DBB9CB',
                '#EDBCCF',
                '#F6C4D4',
                '#FAD1DF',
                '#F6D7D8',
                '#F7C6C6',
                '#FCCFC3',
                '#FEDCD3',
                '#FCD8C2',
                '#FFE3C4',
                '#FFF3C9',
            ]
            self.color = random.choice(colors)
        super(Tag, self).save()