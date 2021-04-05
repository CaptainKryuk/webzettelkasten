from django.contrib import admin
from .models import ContentBlock
from .models import Article

# Register your models here.
admin.site.register(ContentBlock)
admin.site.register(Article)