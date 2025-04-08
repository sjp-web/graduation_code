// 音乐列表页面组件
// 页面级组件，负责协调音乐列表页面的功能

import { createApp } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';

// 初始化页面
document.addEventListener('DOMContentLoaded', () => {
    console.log('音乐列表页面初始化中...');
    
    // 初始化筛选功能
    initFilters();
    
    // 初始化排序功能
    initSorting();
    
    // 初始化音乐卡片交互
    initMusicCards();
    
    // 初始化分页功能
    initPagination();
    
    console.log('音乐列表页面初始化完成');
});

// 初始化筛选功能
function initFilters() {
    const filterForm = document.getElementById('filter-form');
    if (!filterForm) return;
    
    // 获取所有筛选控件
    const categorySelect = document.getElementById('category-filter');
    const yearSelect = document.getElementById('year-filter');
    const artistSelect = document.getElementById('artist-filter');
    
    // 监听筛选控件变化
    [categorySelect, yearSelect, artistSelect].forEach(select => {
        if (select) {
            select.addEventListener('change', function() {
                // 提交表单以应用筛选
                filterForm.submit();
            });
        }
    });
    
    // 清除筛选按钮
    const clearFiltersBtn = document.getElementById('clear-filters');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 重置所有筛选控件
            if (categorySelect) categorySelect.value = '';
            if (yearSelect) yearSelect.value = '';
            if (artistSelect) artistSelect.value = '';
            
            // 提交表单以清除筛选
            filterForm.submit();
        });
    }
}

// 初始化排序功能
function initSorting() {
    const sortDropdown = document.getElementById('sort-dropdown');
    if (!sortDropdown) return;
    
    const sortOptions = sortDropdown.querySelectorAll('.sort-option');
    sortOptions.forEach(option => {
        option.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 获取排序字段和方向
            const field = this.dataset.field;
            const direction = this.dataset.direction;
            
            // 更新隐藏字段的值
            document.getElementById('sort_field').value = field;
            document.getElementById('sort_direction').value = direction;
            
            // 提交表单以应用排序
            document.getElementById('filter-form').submit();
        });
    });
}

// 初始化音乐卡片交互
function initMusicCards() {
    // 延迟加载音乐封面
    const lazyImages = document.querySelectorAll('img.lazy-load');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy-load');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // 回退方案，对于不支持IntersectionObserver的浏览器
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
        });
    }
    
    // 初始化收藏按钮
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    favoriteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // 获取音乐ID和当前收藏状态
            const musicId = this.dataset.musicId;
            const isFavorite = this.dataset.isFavorite === 'true';
            
            // 发送请求更新收藏状态
            fetch('/api/favorites/toggle/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    music_id: musicId,
                    is_favorite: !isFavorite
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 更新UI
                    this.dataset.isFavorite = (!isFavorite).toString();
                    this.querySelector('i').className = !isFavorite ? 
                        'fas fa-heart text-danger' : 'far fa-heart';
                    
                    // 显示提示信息
                    showToast(!isFavorite ? '已添加到收藏' : '已从收藏中移除');
                }
            })
            .catch(error => {
                console.error('收藏操作失败:', error);
                showToast('操作失败，请稍后重试', 'danger');
            });
        });
    });
}

// 初始化分页功能
function initPagination() {
    const paginationLinks = document.querySelectorAll('.page-link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // 阻止默认行为，以便我们可以添加自定义逻辑
            if (this.classList.contains('disabled')) {
                e.preventDefault();
                return;
            }
            
            // 可以在这里添加页面过渡效果
            document.querySelector('.music-list-container').classList.add('fading-out');
        });
    });
}

// 获取Cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 显示提示信息
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        // 创建Toast容器
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
    }
    
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    document.getElementById('toast-container').appendChild(toast);
    
    // 使用Bootstrap的Toast API
    const toastInstance = new bootstrap.Toast(toast, {
        delay: 3000
    });
    toastInstance.show();
    
    // 自动移除DOM元素
    toast.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// 导出页面初始化函数，便于外部调用
export function initMusicListPage() {
    document.dispatchEvent(new Event('DOMContentLoaded'));
} 