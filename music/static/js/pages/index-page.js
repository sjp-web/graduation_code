// 首页页面组件
// 页面级组件，负责首页特效和轮播功能

import { createApp } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';

// 初始化页面
document.addEventListener('DOMContentLoaded', () => {
    console.log('首页页面初始化中...');
    
    // 初始化回到顶部功能
    initScrollToTop();
    
    // 获取挂载点
    const mountPoint = document.getElementById('index-app');
    if (!mountPoint) {
        console.log('未找到首页组件挂载点，使用传统JS增强');
        initTraditionalFeatures();
        return;
    }
    
    try {
        // 获取音乐数据
        const musicDataElement = document.getElementById('music-data');
        let musicData = {};
        
        if (musicDataElement && musicDataElement.textContent) {
            try {
                musicData = JSON.parse(musicDataElement.textContent);
                console.log('成功加载音乐数据');
            } catch (error) {
                console.error('解析音乐数据失败:', error);
            }
        } else {
            // 尝试从全局变量获取
            if (window.musicAppData) {
                musicData = window.musicAppData;
                console.log('从全局变量加载音乐数据');
            }
        }
        
        // 创建Vue应用
        const app = createApp({
            data() {
                return {
                    music: musicData.music || [],
                    categories: musicData.categories || [],
                    currentSort: musicData.currentSort || 'title',
                    currentCategory: musicData.currentCategory || '',
                    currentQuery: musicData.currentQuery || '',
                    loading: false,
                    error: null
                };
            },
            computed: {
                filteredMusic() {
                    return this.music;
                },
                categoryOptions() {
                    return [
                        { value: '', label: '所有分类' },
                        ...this.categories.map(cat => ({ 
                            value: cat.id || cat.value, 
                            label: cat.name || cat.label 
                        }))
                    ];
                }
            },
            methods: {
                // 应用过滤
                applyFilter() {
                    this.loading = true;
                    // 构建查询参数
                    const params = new URLSearchParams();
                    if (this.currentQuery) params.append('query', this.currentQuery);
                    if (this.currentCategory) params.append('category', this.currentCategory);
                    if (this.currentSort) params.append('sort', this.currentSort);
                    
                    // 更新URL而不刷新页面
                    const newUrl = `${window.location.pathname}?${params.toString()}`;
                    window.history.pushState({ path: newUrl }, '', newUrl);
                    
                    // 在实际应用中，这里应该请求后端API获取新数据
                    // 这里我们模拟一个请求延迟
                    setTimeout(() => {
                        this.loading = false;
                    }, 500);
                },
                
                // 清除过滤
                clearFilters() {
                    this.currentQuery = '';
                    this.currentCategory = '';
                    this.applyFilter();
                },
                
                // 播放音乐
                playMusic(songId) {
                    window.location.href = `/music/detail/${songId}/`;
                }
            },
            template: `
                <div class="index-page-app">
                    <!-- 过滤面板 -->
                    <div class="filter-panel-modern">
                        <form @submit.prevent="applyFilter" class="filter-form-modern">
                            <div class="form-group">
                                <label for="query">搜索</label>
                                <input type="text" 
                                       id="query" 
                                       v-model="currentQuery" 
                                       class="form-control" 
                                       placeholder="搜索歌曲、艺术家或专辑...">
                            </div>
                            
                            <div class="form-group">
                                <label for="category">分类</label>
                                <select id="category" 
                                        v-model="currentCategory" 
                                        class="form-control">
                                    <option v-for="option in categoryOptions" 
                                            :key="option.value" 
                                            :value="option.value">
                                        {{ option.label }}
                                    </option>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label for="sort">排序方式</label>
                                <select id="sort" 
                                        v-model="currentSort" 
                                        class="form-control">
                                    <option value="title">按标题</option>
                                    <option value="artist">按艺术家</option>
                                    <option value="date">按发行日期</option>
                                    <option value="popularity">按热度</option>
                                </select>
                            </div>
                            
                            <div class="btn-group">
                                <button type="submit" 
                                        class="btn btn-primary" 
                                        :disabled="loading">
                                    <i :class="loading ? 'fas fa-spinner fa-spin' : 'fas fa-filter'" class="me-1"></i> 
                                    {{ loading ? '筛选中...' : '筛选' }}
                                </button>
                                <button v-if="currentQuery || currentCategory" 
                                        type="button" 
                                        @click="clearFilters" 
                                        class="btn btn-outline-secondary">
                                    <i class="fas fa-times me-1"></i> 清除筛选
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            `
        });
        
        // 挂载应用
        app.mount(mountPoint);
        console.log('首页页面组件挂载成功');
        
    } catch (error) {
        console.error('首页页面初始化失败:', error);
        // 初始化传统功能
        initTraditionalFeatures();
    }
});

// 回到顶部功能
function initScrollToTop() {
    const scrollBtn = document.getElementById('scrollToTop');
    if (!scrollBtn) return;
    
    // 显示/隐藏按钮
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
        }
    });
    
    // 点击回到顶部
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// 初始化传统功能（当Vue无法挂载时）
function initTraditionalFeatures() {
    console.log('使用传统JS增强功能');
    
    // 音乐卡片悬停效果
    const musicCards = document.querySelectorAll('.music-card-modern');
    musicCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover');
        });
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover');
        });
    });
    
    // 过滤表单提交事件优化
    const filterForm = document.querySelector('.filter-form-modern');
    if (filterForm) {
        filterForm.addEventListener('submit', function(event) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> 筛选中...';
            }
        });
    }
}

// 导出页面初始化函数，便于外部调用
export function initIndexPage() {
    console.log('手动初始化首页页面');
    document.dispatchEvent(new Event('DOMContentLoaded'));
} 