from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from jobs.models import JobPost, Region


class HomePage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        
        # Get recent job posts
        context['recent_jobs'] = JobPost.objects.live().order_by('-publication_date')[:6]
        
        # Get top-level regions
        context['regions'] = Region.objects.filter(parent__isnull=True)
        
        return context
    
    class Meta:
        verbose_name = "首页"


class AboutPage(Page):
    intro = RichTextField(blank=True, verbose_name="简介")
    body = RichTextField(blank=True, verbose_name="内容")
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    
    class Meta:
        verbose_name = "关于我们页面"
