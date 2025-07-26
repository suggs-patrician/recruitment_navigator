from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Region, JobPost, Subscription
from django.core.serializers import serialize
from django.db.models import Q
import json

def region_selector_demo(request):
    """地区选择器演示页面"""
    return render(request, 'jobs/region_selector_demo.html')

# Create your views here.

@require_http_methods(["GET"])
def get_provinces(request):
    """获取所有省份"""
    provinces = Region.get_provinces()
    data = [{'id': p.id, 'name': p.name, 'code': p.code} for p in provinces]
    return JsonResponse({'provinces': data})

@require_http_methods(["GET"])
def get_cities(request):
    """根据省份ID获取城市列表"""
    province_id = request.GET.get('province_id')
    if not province_id:
        return JsonResponse({'cities': []})
    
    cities = Region.get_cities_by_province(province_id)
    data = [{'id': c.id, 'name': c.name, 'code': c.code} for c in cities]
    return JsonResponse({'cities': data})

@require_http_methods(["GET"])
def get_counties(request):
    """根据城市ID获取县区列表"""
    city_id = request.GET.get('city_id')
    if not city_id:
        return JsonResponse({'counties': []})
    
    counties = Region.get_counties_by_city(city_id)
    data = [{'id': c.id, 'name': c.name, 'code': c.code} for c in counties]
    return JsonResponse({'counties': data})

@require_http_methods(["GET"])
def get_region_info(request):
    """获取地区详细信息"""
    region_id = request.GET.get('region_id')
    if not region_id:
        return JsonResponse({'error': '缺少region_id参数'})
    
    try:
        region = Region.objects.get(id=region_id)
        data = {
            'id': region.id,
            'name': region.name,
            'code': region.code,
            'level': region.level,
            'full_name': region.get_full_name(),
            'province': region.get_province().name if region.get_province() else None,
            'city': region.get_city().name if region.get_city() else None,
        }
        return JsonResponse(data)
    except Region.DoesNotExist:
        return JsonResponse({'error': '地区不存在'})

@require_http_methods(["GET"])
def get_recent_jobs(request):
    """获取最新岗位信息"""
    limit = request.GET.get('limit', 5)
    try:
        limit = int(limit)
    except ValueError:
        limit = 5
    
    # 获取最新的岗位信息
    recent_jobs = JobPost.objects.live().order_by('-publication_date')[:limit]
    
    jobs_data = []
    for job in recent_jobs:
        job_data = {
            'id': job.id,
            'title': job.title,
            'url': job.get_url(),
            'category': job.category.get_name_display() if job.category else '',
            'region': job.region.get_full_name() if job.region else '',
            'publication_date': job.publication_date.strftime('%Y-%m-%d'),
            'tags': [tag.name for tag in job.tags.all()],
        }
        jobs_data.append(job_data)
    
    # 如果没有真实数据，返回模拟数据
    if not jobs_data:
        import random
        from datetime import datetime, timedelta
        
        mock_companies = [
            '国家能源集团', '中国银行', '中国建设银行', '中国工商银行', '中国农业银行',
            '国家电网', '中国石油', '中国石化', '中国移动', '中国联通',
            '中国电信', '中国建筑', '中国中铁', '中国铁建', '中国交建',
            '中国电建', '中国能建', '中国中车', '中国船舶', '中国兵器'
        ]
        
        mock_titles = [
            '2025年社会招聘公告', '校园招聘启事', '社会公开招聘', '人才引进公告',
            '专业技术岗位招聘', '管理岗位公开招聘', '应届毕业生招聘', '社会人员招聘',
            '高层次人才引进', '紧缺专业人才招聘', '储备干部招聘', '技术工程师招聘'
        ]
        
        mock_locations = [
            '北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都',
            '西安', '天津', '重庆', '青岛', '大连', '厦门', '苏州', '无锡'
        ]
        
        # 生成模拟数据
        for i in range(min(limit, 10)):
            company = random.choice(mock_companies)
            title = random.choice(mock_titles)
            location = random.choice(mock_locations)
            # 生成最近7天内的随机日期
            days_ago = random.randint(0, 7)
            date = datetime.now() - timedelta(days=days_ago)
            
            job_data = {
                'id': i + 1,
                'title': title,
                'url': f'/jobs/{i + 1}/',
                'category': company,
                'region': location,
                'publication_date': date.strftime('%Y-%m-%d'),
                'tags': [],
            }
            jobs_data.append(job_data)
    
    return JsonResponse({
        'jobs': jobs_data,
        'total': len(jobs_data)
    })

@csrf_exempt
@require_http_methods(["POST"])
def subscribe(request):
    """订阅岗位提醒"""
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        channel = data.get('channel', 'web')
        
        if not phone:
            return JsonResponse({'error': '手机号不能为空'}, status=400)
        
        # 简单的手机号验证
        if not phone.isdigit() or len(phone) != 11:
            return JsonResponse({'error': '请输入正确的手机号'}, status=400)
        
        # 检查是否已经订阅
        existing_subscription = Subscription.objects.filter(phone=phone, channel=channel).first()
        if existing_subscription:
            if existing_subscription.is_active:
                return JsonResponse({
                    'success': True,
                    'message': '您已经订阅过了，我们会继续为您推送最新岗位信息。'
                })
            else:
                # 重新激活订阅
                existing_subscription.is_active = True
                existing_subscription.save()
                return JsonResponse({
                    'success': True,
                    'message': '订阅已重新激活！我们将为您推送最新的岗位信息。'
                })
        
        # 创建新订阅
        subscription = Subscription.objects.create(
            phone=phone,
            channel=channel
        )
        
        return JsonResponse({
            'success': True,
            'message': '订阅成功！我们将为您推送最新的岗位信息。'
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
