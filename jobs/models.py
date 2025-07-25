from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtailmarkdown.fields import MarkdownField

# Region models for hierarchical location filtering
class Region(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    def __str__(self):
        if self.parent:
            return f"{self.parent} - {self.name}"
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "地区"
        verbose_name_plural = "地区"

# Job category model
class JobCategory(models.Model):
    CATEGORY_CHOICES = [
        ('government', '政府机关'),
        ('institution', '事业单位'),
        ('state_owned', '国企'),
        ('bank', '银行'),
    ]
    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name = "职位类别"
        verbose_name_plural = "职位类别"

# Job tag model
class JobPostTag(TaggedItemBase):
    content_object = ParentalKey(
        'JobPost',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

# Job post model
class JobPost(Page):
    # Basic information
    publication_date = models.DateField("发布日期")
    deadline = models.DateField("截止日期", null=True, blank=True)
    
    # Content fields
    description = MarkdownField(verbose_name="职位描述")
    requirements = MarkdownField(verbose_name="职位要求", blank=True)
    benefits = MarkdownField(verbose_name="福利待遇", blank=True)
    application_process = MarkdownField(verbose_name="申请流程", blank=True)
    
    # Relationships
    category = models.ForeignKey(
        JobCategory,
        on_delete=models.PROTECT,
        related_name='job_posts',
        verbose_name="职位类别"
    )
    
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='job_posts',
        verbose_name="地区"
    )
    
    tags = ClusterTaggableManager(through=JobPostTag, blank=True, verbose_name="标签")
    
    # Search fields
    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('description'),
        index.SearchField('requirements'),
        index.FilterField('publication_date'),
        index.FilterField('category'),
        index.FilterField('region'),
    ]
    
    # Admin panels
    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('deadline'),
        FieldPanel('category'),
        FieldPanel('region'),
        FieldPanel('tags'),
        FieldPanel('description'),
        FieldPanel('requirements'),
        FieldPanel('benefits'),
        FieldPanel('application_process'),
    ]
    
    parent_page_types = ['JobIndexPage']
    subpage_types = []
    
    class Meta:
        verbose_name = "招聘信息"
        verbose_name_plural = "招聘信息"

# Job index page model
class JobIndexPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    subpage_types = ['JobPost']
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Get all job posts
        job_posts = JobPost.objects.live().descendant_of(self).order_by('-publication_date')
        
        # Filter by category
        category_id = request.GET.get('category')
        if category_id:
            job_posts = job_posts.filter(category_id=category_id)
        
        # Filter by region
        region_id = request.GET.get('region')
        if region_id:
            job_posts = job_posts.filter(region_id=region_id)
        
        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            job_posts = job_posts.filter(tags__name=tag)
        
        # Add the job posts to the context
        context['job_posts'] = job_posts
        
        # Add filter options to the context
        context['categories'] = JobCategory.objects.all()
        context['regions'] = Region.objects.filter(parent__isnull=True)
        
        return context
    
    class Meta:
        verbose_name = "招聘信息列表页"
        verbose_name_plural = "招聘信息列表页"
