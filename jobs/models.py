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

# Subscription model
class Subscription(models.Model):
    CHANNEL_CHOICES = [
        ('web', '网站'),
        ('wechat', '微信'),
        ('app', 'APP'),
    ]
    
    phone = models.CharField(max_length=20, verbose_name="手机号")
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES, default='web', verbose_name="订阅渠道")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="订阅时间")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    
    class Meta:
        verbose_name = "订阅用户"
        verbose_name_plural = "订阅用户"
        unique_together = ['phone', 'channel']
    
    def __str__(self):
        return f"{self.phone} ({self.get_channel_display()})"

# Region models for hierarchical location filtering
class Region(models.Model):
    LEVEL_CHOICES = [
        ('province', '省'),
        ('city', '市'),
        ('county', '县'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="名称")
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name="层级")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="上级地区")
    code = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="地区代码", help_text="用于唯一标识地区，如：110000")
    
    def __str__(self):
        if self.parent:
            return f"{self.parent} - {self.name}"
        return self.name
    
    def get_full_name(self):
        """获取完整地区名称，如：北京市 - 朝阳区"""
        if self.parent:
            return f"{self.parent.get_full_name()} - {self.name}"
        return self.name
    
    def get_province(self):
        """获取所属省份"""
        if self.level == 'province':
            return self
        elif self.level == 'city':
            return self.parent
        elif self.level == 'county':
            return self.parent.parent if self.parent else None
        return None
    
    def get_city(self):
        """获取所属城市"""
        if self.level == 'city':
            return self
        elif self.level == 'county':
            return self.parent
        return None
    
    def get_counties(self):
        """获取下属县区（仅适用于市级）"""
        if self.level == 'city':
            return self.children.filter(level='county')
        return Region.objects.none()
    
    def get_cities(self):
        """获取下属城市（仅适用于省级）"""
        if self.level == 'province':
            return self.children.filter(level='city')
        return Region.objects.none()
    
    @classmethod
    def get_provinces(cls):
        """获取所有省份"""
        return cls.objects.filter(level='province')
    
    @classmethod
    def get_cities_by_province(cls, province_id):
        """根据省份ID获取城市列表"""
        return cls.objects.filter(parent_id=province_id, level='city')
    
    @classmethod
    def get_counties_by_city(cls, city_id):
        """根据城市ID获取县区列表"""
        return cls.objects.filter(parent_id=city_id, level='county')
    
    class Meta:
        ordering = ['code', 'name']
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
        verbose_name="地区",
        null=True,
        blank=True
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
        category_param = request.GET.get('category')
        if category_param:
            # 支持按category名称或ID过滤
            if category_param.isdigit():
                job_posts = job_posts.filter(category_id=category_param)
            else:
                job_posts = job_posts.filter(category__name=category_param)
        
        # Filter by region (支持三级地区过滤)
        province_id = request.GET.get('province')
        city_id = request.GET.get('city')
        county_id = request.GET.get('county')
        
        if county_id:
            # 如果选择了县区，直接过滤
            job_posts = job_posts.filter(region_id=county_id)
        elif city_id:
            # 如果选择了城市，过滤该城市及其下属县区的职位
            city = Region.objects.filter(id=city_id, level='city').first()
            if city:
                counties = city.get_counties()
                job_posts = job_posts.filter(region__in=counties) | job_posts.filter(region=city)
        elif province_id:
            # 如果选择了省份，过滤该省份及其下属城市、县区的职位
            province = Region.objects.filter(id=province_id, level='province').first()
            if province:
                cities = province.get_cities()
                counties = Region.objects.filter(parent__in=cities, level='county')
                job_posts = job_posts.filter(region__in=cities) | job_posts.filter(region__in=counties) | job_posts.filter(region=province)
        
        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            job_posts = job_posts.filter(tags__name=tag)
        
        # Filter by publication date range
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        if date_from:
            job_posts = job_posts.filter(publication_date__gte=date_from)
        
        if date_to:
            job_posts = job_posts.filter(publication_date__lte=date_to)
        
        # Full-text search
        search_query = request.GET.get('search')
        if search_query:
            from django.db.models import Q
            job_posts = job_posts.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(requirements__icontains=search_query) |
                Q(benefits__icontains=search_query) |
                Q(application_process__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        # Add the job posts to the context
        context['job_posts'] = job_posts
        
        # Add filter options to the context
        context['categories'] = JobCategory.objects.all()
        context['provinces'] = Region.get_provinces()
        
        # 根据选择的省份获取城市列表
        if province_id:
            context['cities'] = Region.get_cities_by_province(province_id)
        else:
            context['cities'] = Region.objects.none()
        
        # 根据选择的城市获取县区列表
        if city_id:
            context['counties'] = Region.get_counties_by_city(city_id)
        else:
            context['counties'] = Region.objects.none()
        
        return context
    
    class Meta:
        verbose_name = "招聘信息列表页"
        verbose_name_plural = "招聘信息列表页"
