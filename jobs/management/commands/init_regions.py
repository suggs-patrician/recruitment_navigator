from django.core.management.base import BaseCommand
from jobs.models import Region

class Command(BaseCommand):
    help = '初始化三级地区数据（省-市-县）'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化地区数据...')
        
        # 先更新JobPost的region字段为None，避免外键约束
        from jobs.models import JobPost
        JobPost.objects.all().update(region=None)
        
        # 清空现有数据
        Region.objects.all().delete()
        
        # 创建省份数据
        provinces_data = [
            {'name': '北京市', 'code': '110000', 'level': 'province'},
            {'name': '天津市', 'code': '120000', 'level': 'province'},
            {'name': '河北省', 'code': '130000', 'level': 'province'},
            {'name': '山西省', 'code': '140000', 'level': 'province'},
            {'name': '内蒙古自治区', 'code': '150000', 'level': 'province'},
            {'name': '辽宁省', 'code': '210000', 'level': 'province'},
            {'name': '吉林省', 'code': '220000', 'level': 'province'},
            {'name': '黑龙江省', 'code': '230000', 'level': 'province'},
            {'name': '上海市', 'code': '310000', 'level': 'province'},
            {'name': '江苏省', 'code': '320000', 'level': 'province'},
            {'name': '浙江省', 'code': '330000', 'level': 'province'},
            {'name': '安徽省', 'code': '340000', 'level': 'province'},
            {'name': '福建省', 'code': '350000', 'level': 'province'},
            {'name': '江西省', 'code': '360000', 'level': 'province'},
            {'name': '山东省', 'code': '370000', 'level': 'province'},
            {'name': '河南省', 'code': '410000', 'level': 'province'},
            {'name': '湖北省', 'code': '420000', 'level': 'province'},
            {'name': '湖南省', 'code': '430000', 'level': 'province'},
            {'name': '广东省', 'code': '440000', 'level': 'province'},
            {'name': '广西壮族自治区', 'code': '450000', 'level': 'province'},
            {'name': '海南省', 'code': '460000', 'level': 'province'},
            {'name': '重庆市', 'code': '500000', 'level': 'province'},
            {'name': '四川省', 'code': '510000', 'level': 'province'},
            {'name': '贵州省', 'code': '520000', 'level': 'province'},
            {'name': '云南省', 'code': '530000', 'level': 'province'},
            {'name': '西藏自治区', 'code': '540000', 'level': 'province'},
            {'name': '陕西省', 'code': '610000', 'level': 'province'},
            {'name': '甘肃省', 'code': '620000', 'level': 'province'},
            {'name': '青海省', 'code': '630000', 'level': 'province'},
            {'name': '宁夏回族自治区', 'code': '640000', 'level': 'province'},
            {'name': '新疆维吾尔自治区', 'code': '650000', 'level': 'province'},
        ]
        
        provinces = {}
        for data in provinces_data:
            province = Region.objects.create(**data)
            provinces[data['code']] = province
            self.stdout.write(f'创建省份: {province.name}')
        
        # 创建城市数据（以几个主要城市为例）
        cities_data = [
            # 北京市（直辖市，没有下属城市）
            # 天津市（直辖市，没有下属城市）
            # 河北省
            {'name': '石家庄市', 'code': '130100', 'level': 'city', 'parent': provinces['130000']},
            {'name': '唐山市', 'code': '130200', 'level': 'city', 'parent': provinces['130000']},
            {'name': '秦皇岛市', 'code': '130300', 'level': 'city', 'parent': provinces['130000']},
            {'name': '邯郸市', 'code': '130400', 'level': 'city', 'parent': provinces['130000']},
            {'name': '邢台市', 'code': '130500', 'level': 'city', 'parent': provinces['130000']},
            {'name': '保定市', 'code': '130600', 'level': 'city', 'parent': provinces['130000']},
            {'name': '张家口市', 'code': '130700', 'level': 'city', 'parent': provinces['130000']},
            {'name': '承德市', 'code': '130800', 'level': 'city', 'parent': provinces['130000']},
            {'name': '沧州市', 'code': '130900', 'level': 'city', 'parent': provinces['130000']},
            {'name': '廊坊市', 'code': '131000', 'level': 'city', 'parent': provinces['130000']},
            {'name': '衡水市', 'code': '131100', 'level': 'city', 'parent': provinces['130000']},
            # 上海市（直辖市，没有下属城市）
            # 江苏省
            {'name': '南京市', 'code': '320100', 'level': 'city', 'parent': provinces['320000']},
            {'name': '无锡市', 'code': '320200', 'level': 'city', 'parent': provinces['320000']},
            {'name': '徐州市', 'code': '320300', 'level': 'city', 'parent': provinces['320000']},
            {'name': '常州市', 'code': '320400', 'level': 'city', 'parent': provinces['320000']},
            {'name': '苏州市', 'code': '320500', 'level': 'city', 'parent': provinces['320000']},
            {'name': '南通市', 'code': '320600', 'level': 'city', 'parent': provinces['320000']},
            {'name': '连云港市', 'code': '320700', 'level': 'city', 'parent': provinces['320000']},
            {'name': '淮安市', 'code': '320800', 'level': 'city', 'parent': provinces['320000']},
            {'name': '盐城市', 'code': '320900', 'level': 'city', 'parent': provinces['320000']},
            {'name': '扬州市', 'code': '321000', 'level': 'city', 'parent': provinces['320000']},
            {'name': '镇江市', 'code': '321100', 'level': 'city', 'parent': provinces['320000']},
            {'name': '泰州市', 'code': '321200', 'level': 'city', 'parent': provinces['320000']},
            {'name': '宿迁市', 'code': '321300', 'level': 'city', 'parent': provinces['320000']},
            # 浙江省
            {'name': '杭州市', 'code': '330100', 'level': 'city', 'parent': provinces['330000']},
            {'name': '宁波市', 'code': '330200', 'level': 'city', 'parent': provinces['330000']},
            {'name': '温州市', 'code': '330300', 'level': 'city', 'parent': provinces['330000']},
            {'name': '嘉兴市', 'code': '330400', 'level': 'city', 'parent': provinces['330000']},
            {'name': '湖州市', 'code': '330500', 'level': 'city', 'parent': provinces['330000']},
            {'name': '绍兴市', 'code': '330600', 'level': 'city', 'parent': provinces['330000']},
            {'name': '金华市', 'code': '330700', 'level': 'city', 'parent': provinces['330000']},
            {'name': '衢州市', 'code': '330800', 'level': 'city', 'parent': provinces['330000']},
            {'name': '舟山市', 'code': '330900', 'level': 'city', 'parent': provinces['330000']},
            {'name': '台州市', 'code': '331000', 'level': 'city', 'parent': provinces['330000']},
            {'name': '丽水市', 'code': '331100', 'level': 'city', 'parent': provinces['330000']},
            # 广东省
            {'name': '广州市', 'code': '440100', 'level': 'city', 'parent': provinces['440000']},
            {'name': '韶关市', 'code': '440200', 'level': 'city', 'parent': provinces['440000']},
            {'name': '深圳市', 'code': '440300', 'level': 'city', 'parent': provinces['440000']},
            {'name': '珠海市', 'code': '440400', 'level': 'city', 'parent': provinces['440000']},
            {'name': '汕头市', 'code': '440500', 'level': 'city', 'parent': provinces['440000']},
            {'name': '佛山市', 'code': '440600', 'level': 'city', 'parent': provinces['440000']},
            {'name': '江门市', 'code': '440700', 'level': 'city', 'parent': provinces['440000']},
            {'name': '湛江市', 'code': '440800', 'level': 'city', 'parent': provinces['440000']},
            {'name': '茂名市', 'code': '440900', 'level': 'city', 'parent': provinces['440000']},
            {'name': '肇庆市', 'code': '441200', 'level': 'city', 'parent': provinces['440000']},
            {'name': '惠州市', 'code': '441300', 'level': 'city', 'parent': provinces['440000']},
            {'name': '梅州市', 'code': '441400', 'level': 'city', 'parent': provinces['440000']},
            {'name': '汕尾市', 'code': '441500', 'level': 'city', 'parent': provinces['440000']},
            {'name': '河源市', 'code': '441600', 'level': 'city', 'parent': provinces['440000']},
            {'name': '阳江市', 'code': '441700', 'level': 'city', 'parent': provinces['440000']},
            {'name': '清远市', 'code': '441800', 'level': 'city', 'parent': provinces['440000']},
            {'name': '东莞市', 'code': '441900', 'level': 'city', 'parent': provinces['440000']},
            {'name': '中山市', 'code': '442000', 'level': 'city', 'parent': provinces['440000']},
            {'name': '潮州市', 'code': '445100', 'level': 'city', 'parent': provinces['440000']},
            {'name': '揭阳市', 'code': '445200', 'level': 'city', 'parent': provinces['440000']},
            {'name': '云浮市', 'code': '445300', 'level': 'city', 'parent': provinces['440000']},
        ]
        
        cities = {}
        for data in cities_data:
            city = Region.objects.create(**data)
            cities[data['code']] = city
            self.stdout.write(f'创建城市: {city.name}')
        
        # 创建县区数据（以几个主要城市为例）
        counties_data = [
            # 北京市
            {'name': '东城区', 'code': '110101', 'level': 'county', 'parent': provinces['110000']},
            {'name': '西城区', 'code': '110102', 'level': 'county', 'parent': provinces['110000']},
            {'name': '朝阳区', 'code': '110105', 'level': 'county', 'parent': provinces['110000']},
            {'name': '丰台区', 'code': '110106', 'level': 'county', 'parent': provinces['110000']},
            {'name': '石景山区', 'code': '110107', 'level': 'county', 'parent': provinces['110000']},
            {'name': '海淀区', 'code': '110108', 'level': 'county', 'parent': provinces['110000']},
            {'name': '门头沟区', 'code': '110109', 'level': 'county', 'parent': provinces['110000']},
            {'name': '房山区', 'code': '110111', 'level': 'county', 'parent': provinces['110000']},
            {'name': '通州区', 'code': '110112', 'level': 'county', 'parent': provinces['110000']},
            {'name': '顺义区', 'code': '110113', 'level': 'county', 'parent': provinces['110000']},
            {'name': '昌平区', 'code': '110114', 'level': 'county', 'parent': provinces['110000']},
            {'name': '大兴区', 'code': '110115', 'level': 'county', 'parent': provinces['110000']},
            {'name': '怀柔区', 'code': '110116', 'level': 'county', 'parent': provinces['110000']},
            {'name': '平谷区', 'code': '110117', 'level': 'county', 'parent': provinces['110000']},
            {'name': '密云区', 'code': '110118', 'level': 'county', 'parent': provinces['110000']},
            {'name': '延庆区', 'code': '110119', 'level': 'county', 'parent': provinces['110000']},
            # 上海市
            {'name': '黄浦区', 'code': '310101', 'level': 'county', 'parent': provinces['310000']},
            {'name': '徐汇区', 'code': '310104', 'level': 'county', 'parent': provinces['310000']},
            {'name': '长宁区', 'code': '310105', 'level': 'county', 'parent': provinces['310000']},
            {'name': '静安区', 'code': '310106', 'level': 'county', 'parent': provinces['310000']},
            {'name': '普陀区', 'code': '310107', 'level': 'county', 'parent': provinces['310000']},
            {'name': '虹口区', 'code': '310109', 'level': 'county', 'parent': provinces['310000']},
            {'name': '杨浦区', 'code': '310110', 'level': 'county', 'parent': provinces['310000']},
            {'name': '闵行区', 'code': '310112', 'level': 'county', 'parent': provinces['310000']},
            {'name': '宝山区', 'code': '310113', 'level': 'county', 'parent': provinces['310000']},
            {'name': '嘉定区', 'code': '310114', 'level': 'county', 'parent': provinces['310000']},
            {'name': '浦东新区', 'code': '310115', 'level': 'county', 'parent': provinces['310000']},
            {'name': '金山区', 'code': '310116', 'level': 'county', 'parent': provinces['310000']},
            {'name': '松江区', 'code': '310117', 'level': 'county', 'parent': provinces['310000']},
            {'name': '青浦区', 'code': '310118', 'level': 'county', 'parent': provinces['310000']},
            {'name': '奉贤区', 'code': '310120', 'level': 'county', 'parent': provinces['310000']},
            {'name': '崇明区', 'code': '310151', 'level': 'county', 'parent': provinces['310000']},
            # 广州市
            {'name': '荔湾区', 'code': '440103', 'level': 'county', 'parent': cities['440100']},
            {'name': '越秀区', 'code': '440104', 'level': 'county', 'parent': cities['440100']},
            {'name': '海珠区', 'code': '440105', 'level': 'county', 'parent': cities['440100']},
            {'name': '天河区', 'code': '440106', 'level': 'county', 'parent': cities['440100']},
            {'name': '白云区', 'code': '440111', 'level': 'county', 'parent': cities['440100']},
            {'name': '黄埔区', 'code': '440112', 'level': 'county', 'parent': cities['440100']},
            {'name': '番禺区', 'code': '440113', 'level': 'county', 'parent': cities['440100']},
            {'name': '花都区', 'code': '440114', 'level': 'county', 'parent': cities['440100']},
            {'name': '南沙区', 'code': '440115', 'level': 'county', 'parent': cities['440100']},
            {'name': '从化区', 'code': '440117', 'level': 'county', 'parent': cities['440100']},
            {'name': '增城区', 'code': '440118', 'level': 'county', 'parent': cities['440100']},
            # 深圳市
            {'name': '罗湖区', 'code': '440303', 'level': 'county', 'parent': cities['440300']},
            {'name': '福田区', 'code': '440304', 'level': 'county', 'parent': cities['440300']},
            {'name': '南山区', 'code': '440305', 'level': 'county', 'parent': cities['440300']},
            {'name': '宝安区', 'code': '440306', 'level': 'county', 'parent': cities['440300']},
            {'name': '龙岗区', 'code': '440307', 'level': 'county', 'parent': cities['440300']},
            {'name': '盐田区', 'code': '440308', 'level': 'county', 'parent': cities['440300']},
            {'name': '龙华区', 'code': '440309', 'level': 'county', 'parent': cities['440300']},
            {'name': '坪山区', 'code': '440310', 'level': 'county', 'parent': cities['440300']},
            {'name': '光明区', 'code': '440311', 'level': 'county', 'parent': cities['440300']},
        ]
        
        for data in counties_data:
            county = Region.objects.create(**data)
            self.stdout.write(f'创建县区: {county.name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'成功初始化地区数据！共创建了 {len(provinces)} 个省份，{len(cities)} 个城市，{len(counties_data)} 个县区')
        ) 