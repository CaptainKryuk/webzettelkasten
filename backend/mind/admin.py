from django.contrib import admin
from .models import ContentBlock
from .models import Article

# Register your models here.
admin.site.register(ContentBlock)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'blocks')

    def blocks(self, obj):
        from django.utils.html import format_html

        return format_html("{}", '\n'.join([block.inner_text for block in obj.contentblock_set.all()]))

    blocks.short_description = u'Блоки с контентом'
    blocks.admin_ordering_field = 'get_variants'
    blocks.allow_tags = True