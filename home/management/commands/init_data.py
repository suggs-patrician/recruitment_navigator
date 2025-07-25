from django.core.management.base import BaseCommand
from django.utils import timezone
from wagtail.models import Site
from home.models import HomePage, AboutPage
from jobs.models import JobIndexPage, JobPost, JobCategory, Region
import datetime


class Command(BaseCommand):
    help = '初始化网站基础数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化数据...')
        
        # 获取根页面
        site = Site.objects.get(is_default_site=True)
        root_page = site.root_page
        
        # 获取首页
        try:
            home_page = HomePage.objects.get(slug='home')
        except HomePage.DoesNotExist:
            self.stdout.write(self.style.ERROR('首页不存在'))
            return
        
        # 检查关于我们页面是否存在
        if not AboutPage.objects.filter(slug='关于我们').exists():
            self.stdout.write('关于我们页面不存在，请在管理后台创建')
        else:
            self.stdout.write('关于我们页面已存在')
        
        # 创建职位类别
        categories_data = [
            'government',
            'institution', 
            'state_owned',
            'bank',
        ]
        
        for category_name in categories_data:
            category, created = JobCategory.objects.get_or_create(
                name=category_name
            )
            if created:
                self.stdout.write(f'创建职位类别: {category.get_name_display()}')
        
        # 创建地区信息
        regions_data = [
            '北京市',
            '上海市',
            '广东省',
            '江苏省',
            '浙江省',
            '山东省',
            '河南省',
            '四川省',
            '湖北省',
            '湖南省',
        ]
        
        for name in regions_data:
            region, created = Region.objects.get_or_create(
                name=name
            )
            if created:
                self.stdout.write(f'创建地区: {name}')
        
        # 获取招聘信息页面
        try:
            job_index = JobIndexPage.objects.get(slug='招聘信息')
        except JobIndexPage.DoesNotExist:
            self.stdout.write(self.style.ERROR('招聘信息页面不存在，请先在管理后台创建'))
            return
        
        # 创建示例招聘信息
        sample_jobs = [
            {
                'title': '北京市教育局招聘教师',
                'organization': '北京市教育局',
                'location': '北京市',
                'category': 'government',
                'region': '北京市',
                'description': '招聘中小学教师，要求师范类专业毕业，有教师资格证。',
                'requirements': '1. 师范类专业本科及以上学历\n2. 持有教师资格证\n3. 普通话二级甲等以上',
                'salary': '8000-12000元/月',
                'application_deadline': timezone.now() + datetime.timedelta(days=30),
            },
            {
                'title': '上海市人民医院招聘医生',
                'organization': '上海市人民医院',
                'location': '上海市',
                'category': 'institution',
                'region': '上海市',
                'description': '招聘内科、外科医生，要求医学专业毕业，有执业医师证。',
                'requirements': '1. 医学专业本科及以上学历\n2. 持有执业医师证\n3. 有相关工作经验优先',
                'salary': '12000-20000元/月',
                'application_deadline': timezone.now() + datetime.timedelta(days=25),
            },
            {
                'title': '中国石油广东分公司招聘工程师',
                'organization': '中国石油广东分公司',
                'location': '广州市',
                'category': 'state_owned',
                'region': '广东省',
                'description': '招聘石油工程师，要求石油工程或相关专业毕业。',
                'requirements': '1. 石油工程或相关专业本科及以上学历\n2. 英语四级以上\n3. 有相关实习经验优先',
                'salary': '10000-15000元/月',
                'application_deadline': timezone.now() + datetime.timedelta(days=20),
            },
            {
                'title': '中国银行江苏分行招聘客户经理',
                'organization': '中国银行江苏分行',
                'location': '南京市',
                'category': 'bank',
                'region': '江苏省',
                'description': '招聘客户经理，负责个人和企业客户开发维护。',
                'requirements': '1. 金融、经济类专业本科及以上学历\n2. 有银行或金融行业经验优先\n3. 沟通能力强，有团队合作精神',
                'salary': '8000-15000元/月',
                'application_deadline': timezone.now() + datetime.timedelta(days=15),
            },
            {
                'title': '浙江大学招聘研究员',
                'organization': '浙江大学',
                'location': '杭州市',
                'category': 'institution',
                'region': '浙江省',
                'description': '招聘计算机科学研究员，从事人工智能相关研究。',
                'requirements': '1. 计算机科学博士学位\n2. 有人工智能研究经验\n3. 发表过高质量学术论文',
                'salary': '15000-25000元/月',
                'application_deadline': timezone.now() + datetime.timedelta(days=35),
            },
        ]
        
        for job_data in sample_jobs:
            # 获取类别和地区对象
            try:
                category = JobCategory.objects.get(name=job_data['category'])
                region = Region.objects.get(name=job_data['region'])
            except (JobCategory.DoesNotExist, Region.DoesNotExist):
                continue
            
            # 检查是否已存在
            if not JobPost.objects.filter(title=job_data['title']).exists():
                job_post = JobPost(
                    title=job_data['title'],
                    category=category,
                    region=region,
                    description=job_data['description'],
                    requirements=job_data['requirements'],
                    deadline=job_data['application_deadline'].date(),
                    publication_date=timezone.now().date(),
                )
                job_index.add_child(instance=job_post)
                job_post.save_revision().publish()
                self.stdout.write(f'创建招聘信息: {job_data["title"]}')
        
        self.stdout.write(self.style.SUCCESS('数据初始化完成！'))