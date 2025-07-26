/**
 * 三级地区联动选择器
 */
class RegionSelector {
    constructor(provinceSelect, citySelect, countySelect) {
        this.provinceSelect = provinceSelect;
        this.citySelect = citySelect;
        this.countySelect = countySelect;
        
        this.init();
    }
    
    init() {
        // 加载省份数据
        this.loadProvinces();
        
        // 绑定事件
        this.provinceSelect.addEventListener('change', () => this.onProvinceChange());
        this.citySelect.addEventListener('change', () => this.onCityChange());
    }
    
    async loadProvinces() {
        try {
            const response = await fetch('/api/regions/provinces/');
            const data = await response.json();
            
            this.provinceSelect.innerHTML = '<option value="">请选择省份</option>';
            data.provinces.forEach(province => {
                const option = document.createElement('option');
                option.value = province.id;
                option.textContent = province.name;
                this.provinceSelect.appendChild(option);
            });
        } catch (error) {
            console.error('加载省份数据失败:', error);
        }
    }
    
    async onProvinceChange() {
        const provinceId = this.provinceSelect.value;
        
        // 清空城市和县区选择器
        this.citySelect.innerHTML = '<option value="">请选择城市</option>';
        this.countySelect.innerHTML = '<option value="">请选择县区</option>';
        
        if (!provinceId) return;
        
        try {
            const response = await fetch(`/api/regions/cities/?province_id=${provinceId}`);
            const data = await response.json();
            
            data.cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city.id;
                option.textContent = city.name;
                this.citySelect.appendChild(option);
            });
        } catch (error) {
            console.error('加载城市数据失败:', error);
        }
    }
    
    async onCityChange() {
        const cityId = this.citySelect.value;
        
        // 清空县区选择器
        this.countySelect.innerHTML = '<option value="">请选择县区</option>';
        
        if (!cityId) return;
        
        try {
            const response = await fetch(`/api/regions/counties/?city_id=${cityId}`);
            const data = await response.json();
            
            data.counties.forEach(county => {
                const option = document.createElement('option');
                option.value = county.id;
                option.textContent = county.name;
                this.countySelect.appendChild(option);
            });
        } catch (error) {
            console.error('加载县区数据失败:', error);
        }
    }
    
    // 获取选中的地区信息
    getSelectedRegion() {
        const provinceId = this.provinceSelect.value;
        const cityId = this.citySelect.value;
        const countyId = this.countySelect.value;
        
        if (countyId) {
            return { level: 'county', id: countyId };
        } else if (cityId) {
            return { level: 'city', id: cityId };
        } else if (provinceId) {
            return { level: 'province', id: provinceId };
        }
        
        return null;
    }
    
    // 设置选中的地区
    async setSelectedRegion(regionId) {
        try {
            const response = await fetch(`/api/regions/info/?region_id=${regionId}`);
            const data = await response.json();
            
            if (data.error) {
                console.error('获取地区信息失败:', data.error);
                return;
            }
            
            // 根据地区层级设置选择器
            if (data.level === 'province') {
                this.provinceSelect.value = data.id;
                await this.onProvinceChange();
            } else if (data.level === 'city') {
                // 需要先设置省份
                if (data.province) {
                    // 这里需要根据省份名称找到对应的省份ID
                    // 简化处理，实际应用中可能需要更复杂的逻辑
                }
                this.citySelect.value = data.id;
                await this.onCityChange();
            } else if (data.level === 'county') {
                // 需要先设置省份和城市
                this.countySelect.value = data.id;
            }
        } catch (error) {
            console.error('设置地区失败:', error);
        }
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    const provinceSelect = document.getElementById('province-select');
    const citySelect = document.getElementById('city-select');
    const countySelect = document.getElementById('county-select');
    
    if (provinceSelect && citySelect && countySelect) {
        window.regionSelector = new RegionSelector(provinceSelect, citySelect, countySelect);
    }
}); 