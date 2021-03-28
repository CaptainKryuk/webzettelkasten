from django.db import models
from base.models import AbstractDateTimeModel
from pytils.translit import slugify

import datetime
import re

import random


class Article(AbstractDateTimeModel):
    """
    * compile and store all blocks with data
    """
    prepopulated_fields = {"slug": ("title", )}

    title = models.CharField("Заголовок новости", max_length=400, blank=True)

    base_name = models.CharField("Сокращенное название", max_length=500, blank=True)

    slug = models.CharField(max_length=400, blank=True)

    tags = models.ManyToManyField("mind.Tag", verbose_name="Тэги", blank=True)

    status = models.CharField("Статус статьи", choices=(('draft', 'draft'), ('completed', 'completed')), default='draft', max_length=12)

    order_number = models.IntegerField("Место по порядку", blank=True)

    user = models.ForeignKey('users.User', verbose_name="Пользователь, написавший статью", on_delete=models.CASCADE)

    class Meta:
        ordering = ('order_number', '-created')
        verbose_name = "Статья"
        verbose_name_plural = "Все статьи"

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        self.slug = slugify(self.title)
        self.base_name = '-'.join([re.sub(r'\W', r'-', self.title), str(now.day), str(now.month), str(now.year)])

        if not self.pk:
            # set order number
            last_article = Article.objects.filter(user=self.user).last()
            if last_article:
                self.order_number = last_article.order_number + 1
            else:
                self.order_number = 0
            
        super(Article, self).save(*args, **kwargs)

        # need ready instance to create new block
        # create detaul text block
        block = ContentBlock.objects.create(article=self)


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



class ContentBlock(models.Model):
    """
    Base fields for every elements
    """
    BLOCK_TYPES = (
        ('text', 'text'),
        ('title', 'title'),
        ('list', 'list')
    )

    order_number = models.IntegerField("Место по порядку", blank=True, default=0)

    article = models.ForeignKey(Article, verbose_name="Статья", on_delete=models.CASCADE)

    block_type = models.CharField("Тип блока", choices=BLOCK_TYPES, max_length=20, default='text')


    # * if block title settings
    TITLE_LEVELS = (
        ('h1', 'h1'),
        ('h2', 'h2'),
        ('h3', 'h3')
    )
    level = models.CharField("Уровень заголовка", max_length=3, blank=True)

    title_text = models.TextField("Текст заголовка", blank=True)


    # * if block text settings
    inner_text = models.TextField("HTML текст, который будет обрабатываться", blank=True)       


    class Meta:
        ordering = ('order_number', )

    def __str__(self,):
        if self.block_type == 'text':
            return f'TextBlock {self.id} -- {self.inner_text[:10]}'
        return 'Another block'

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.order_number:
                # set order number
                last_block = ContentBlock.objects.filter(article=self.article).last()
                if last_block:
                    self.order_number = last_block.order_number + 1
                else:
                    self.order_number = 0
            if self.order_number:
                # find blocks with greater order_number
                blocks = ContentBlock.objects.filter(order_number__gte=self.order_number)
                for b in blocks:
                    b.order_number += 1
                    b.save()

        super(ContentBlock, self).save(*args, **kwargs)




# Create your models here.
class Idea(AbstractDateTimeModel):
    """
    Main class includes text etc
    """
    title = models.CharField("Заголовок идеи", max_length=255, blank=True)

    slug = models.SlugField(max_length=255, blank=True)

    text = models.TextField("Весь текст", blank=True)

    tags = models.ManyToManyField("mind.Tag", verbose_name="Тэги", blank=True)

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

    def save(self, *args, **kwargs):
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
        super(Tag, self).save(*args, **kwargs)