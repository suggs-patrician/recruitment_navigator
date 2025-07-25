from django.contrib import admin
from django.utils.html import format_html
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Region, JobCategory

# Register models in Django admin
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_display_name')
    
    def get_display_name(self, obj):
        return obj.get_name_display()
    get_display_name.short_description = '显示名称'

# Register models as Wagtail snippets
class RegionSnippetViewSet(SnippetViewSet):
    model = Region
    menu_label = '地区'
    icon = 'site'
    list_display = ('name', 'parent')
    search_fields = ('name',)

class JobCategorySnippetViewSet(SnippetViewSet):
    model = JobCategory
    menu_label = '职位类别'
    icon = 'tag'
    list_display = ('name',)

register_snippet(RegionSnippetViewSet)
register_snippet(JobCategorySnippetViewSet)
