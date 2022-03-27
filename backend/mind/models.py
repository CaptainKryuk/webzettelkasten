from statistics import mode
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

    source = models.TextField(blank=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Все статьи"

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        self.slug = slugify(self.title)
        self.base_name = '-'.join([re.sub(r'\W', r'-', self.title), str(now.day), str(now.month), str(now.year)])

        flag = False
        if not self.pk:
            flag = True
            # set order number
            last_article = Article.objects.filter(user=self.user).order_by('order_number').last()
            if last_article:
                self.order_number = last_article.order_number + 1
            else:
                self.order_number = 0
            
        super(Article, self).save(*args, **kwargs)

        # need ready instance to create new block
        # create detaul text block
        if flag:
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

    def add_tag(self, name: str, color: str):
        exist_tag = Tag.objects.filter(name=name).first()
        if exist_tag:
            self.tags.add(exist_tag)
            return
        
        # create new tag
        new_tag = Tag(name=name, color=color)
        new_tag.save()
        self.tags.add(new_tag)
    
    def remove_tag(self, name):
        """ delete tag from idea """
        tag = Tag.objects.filter(name=name).first()
        if tag and tag in self.tags.all():
            self.tags.remove(tag.id)


    def __str__(self) -> str:
        return self.title



class ContentBlock(models.Model):
    """
    Base fields for every elements
    """
    BLOCK_TYPES = (
        ('text', 'text'),
        ('title', 'title'),
        ('code', 'code'),
        ('list', 'list'),
        ('markdown', 'markdown'),
        ('img', 'img')
    )

    order_number = models.IntegerField("Место по порядку", blank=True, default=0)

    article = models.ForeignKey(Article, verbose_name="Статья", on_delete=models.CASCADE)

    block_type = models.CharField("Тип блока", choices=BLOCK_TYPES, max_length=20, default='text')


    # * if block title
    TITLE_LEVELS = (
        ('h1', 'h1'),
        ('h2', 'h2'),
        ('h3', 'h3')
    )
    level = models.CharField("Уровень заголовка", max_length=3, blank=True, default='h1')

    title_text = models.TextField("Текст заголовка", blank=True)


    # * if block code
    LANGUAGES = (
        ('python', 'python'),
        ('js', 'js'),
        ('sql', 'sql'),
        ('vuejs', 'vuejs')
    )
    code_lang = models.CharField("Язык программирования блока", max_length=20, choices=LANGUAGES, default="python")

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
            else:
                # * when block added to the center we must get all blocks which have order_number > then current and increase it by 1
                current_block = ContentBlock.objects.filter(article=self.article, order_number=self.order_number).first()
                if current_block:
                    shift_blocks = ContentBlock.objects.filter(order_number__gte=self.order_number)
                    for block in shift_blocks:
                        block.order_number += 1
                        block.save()

        super(ContentBlock, self).save(*args, **kwargs)



class BlockImage(AbstractDateTimeModel):
    block = models.ForeignKey(ContentBlock, on_delete=models.CASCADE)
    # * if block type is img
    file = models.ImageField(verbose_name="Картинка", blank=False, null=True)
    filesize = models.IntegerField("Размер файла")
    filename = models.CharField("Название файла", max_length=255)      



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
            if not self.color:
                colors = [
                    '#F44336',
                    '#E91E63',
                    '#9C27B0',
                    '#673AB7',
                    '#3F51B5',
                    '#2196F3',
                    '#00BCD4',
                    '#009688',
                    '#4CAF50',
                    '#CDDC39',
                    '#FFEB3B',
                    '#FF9800',
                    '#FF5722',
                    '#795548',
                    '#9E9E9E',
                    '#607D8B'
                ]
                self.color = random.choice(colors)
        super(Tag, self).save(*args, **kwargs)