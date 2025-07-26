# 三级地区系统使用说明

## 概述

本项目实现了三级地区系统（省-市-县），用于招聘信息的地区分类和过滤。系统支持：

- 三级层级结构：省份 → 城市 → 县区
- 直辖市特殊处理：直辖市直接下辖县区
- 层级过滤：支持按省份、城市、县区进行职位过滤
- API接口：提供RESTful API支持前端联动选择器

## 数据模型

### Region 模型

```python
class Region(models.Model):
    LEVEL_CHOICES = [
        ('province', '省'),
        ('city', '市'),
        ('county', '县'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="名称")
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name="层级")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="上级地区")
    code = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="地区代码")
```

### 主要方法

#### 类方法
- `get_provinces()`: 获取所有省份
- `get_cities_by_province(province_id)`: 根据省份ID获取城市列表
- `get_counties_by_city(city_id)`: 根据城市ID获取县区列表

#### 实例方法
- `get_full_name()`: 获取完整地区名称（如：北京市 - 朝阳区）
- `get_province()`: 获取所属省份
- `get_city()`: 获取所属城市
- `get_counties()`: 获取下属县区（仅适用于市级）
- `get_cities()`: 获取下属城市（仅适用于省级）

## API 接口

### 1. 获取省份列表
```
GET /api/regions/provinces/
```

响应示例：
```json
{
    "provinces": [
        {"id": 11, "name": "北京市", "code": "110000"},
        {"id": 12, "name": "天津市", "code": "120000"},
        ...
    ]
}
```

### 2. 获取城市列表
```
GET /api/regions/cities/?province_id=13
```

响应示例：
```json
{
    "cities": [
        {"id": 1301, "name": "石家庄市", "code": "130100"},
        {"id": 1302, "name": "唐山市", "code": "130200"},
        ...
    ]
}
```

### 3. 获取县区列表
```
GET /api/regions/counties/?city_id=1301
```

响应示例：
```json
{
    "counties": [
        {"id": 130101, "name": "长安区", "code": "130101"},
        {"id": 130102, "name": "桥西区", "code": "130102"},
        ...
    ]
}
```

### 4. 获取地区详细信息
```
GET /api/regions/info/?region_id=130101
```

响应示例：
```json
{
    "id": 130101,
    "name": "长安区",
    "code": "130101",
    "level": "county",
    "full_name": "河北省 - 石家庄市 - 长安区",
    "province": "河北省",
    "city": "石家庄市"
}
```

## 前端使用

### JavaScript 联动选择器

```html
<select id="province-select">
    <option value="">请选择省份</option>
</select>

<select id="city-select">
    <option value="">请选择城市</option>
</select>

<select id="county-select">
    <option value="">请选择县区</option>
</select>
```

```javascript
// 引入 region_selector.js
const regionSelector = new RegionSelector(
    document.getElementById('province-select'),
    document.getElementById('city-select'),
    document.getElementById('county-select')
);

// 获取选中的地区
const selectedRegion = regionSelector.getSelectedRegion();
```

### 演示页面

访问 `/demo/region-selector/` 查看完整的演示效果。

## 数据初始化

### 初始化地区数据

```bash
python manage.py init_regions
```

这个命令会：
1. 清空现有的地区数据
2. 创建31个省份（包括直辖市）
3. 创建56个主要城市
4. 创建52个县区（以北京、上海、广州、深圳为例）

### 自定义数据

可以修改 `jobs/management/commands/init_regions.py` 文件来添加更多地区数据。

## 职位过滤

在 `JobIndexPage` 中实现了基于三级地区的职位过滤：

```python
# 按省份过滤
if province_id:
    province = Region.objects.filter(id=province_id, level='province').first()
    if province:
        cities = province.get_cities()
        counties = Region.objects.filter(parent__in=cities, level='county')
        job_posts = job_posts.filter(
            region__in=cities | region__in=counties | region=province
        )

# 按城市过滤
if city_id:
    city = Region.objects.filter(id=city_id, level='city').first()
    if city:
        counties = city.get_counties()
        job_posts = job_posts.filter(region__in=counties | region=city)

# 按县区过滤
if county_id:
    job_posts = job_posts.filter(region_id=county_id)
```

## 数据库迁移

如果修改了模型，需要创建并应用迁移：

```bash
python manage.py makemigrations jobs
python manage.py migrate
```

## 注意事项

1. **直辖市处理**：北京、上海、天津、重庆等直辖市直接下辖县区，没有中间的城市层级。

2. **地区代码**：使用标准的行政区划代码（6位数字），便于与外部系统对接。

3. **外键约束**：JobPost的region字段允许为空，避免删除地区时出现外键约束错误。

4. **性能优化**：对于大量数据的场景，建议添加数据库索引：

```python
class Region(models.Model):
    # ... 其他字段 ...
    
    class Meta:
        indexes = [
            models.Index(fields=['level']),
            models.Index(fields=['parent', 'level']),
        ]
```

## 扩展功能

### 添加更多地区数据

可以通过以下方式扩展地区数据：

1. 修改初始化脚本添加更多城市和县区
2. 创建数据导入脚本从外部数据源导入
3. 通过管理界面手动添加

### 支持更多层级

如果需要支持更多层级（如街道、社区），可以：

1. 扩展 `LEVEL_CHOICES`
2. 添加相应的获取方法
3. 更新前端选择器

### 国际化支持

可以添加多语言支持：

```python
class Region(models.Model):
    name_zh = models.CharField(max_length=100, verbose_name="中文名称")
    name_en = models.CharField(max_length=100, verbose_name="英文名称")
    # ...
``` 