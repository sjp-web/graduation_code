// 音乐卡片组件
// 可在多个页面中复用的音乐卡片组件

/**
 * 创建音乐卡片元素
 * @param {Object} music - 音乐数据对象
 * @param {Object} options - 配置选项
 * @returns {HTMLElement} - 音乐卡片DOM元素
 */
export function createMusicCard(music, options = {}) {
    // 默认选项
    const defaults = {
        showControls: true,
        showPlayButton: true,
        showFavorite: true,
        lazyLoad: true,
        cardSize: 'medium', // small, medium, large
        onClick: null,
        onFavoriteClick: null
    };
    
    // 合并选项
    const settings = { ...defaults, ...options };
    
    // 创建卡片容器
    const card = document.createElement('div');
    card.className = `music-card music-card-${settings.cardSize} shadow-sm rounded overflow-hidden h-100 transition-all`;
    card.dataset.musicId = music.id;
    
    // 添加悬停效果
    card.addEventListener('mouseenter', function() {
        this.classList.add('shadow');
        this.style.transform = 'translateY(-5px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.classList.remove('shadow');
        this.style.transform = 'translateY(0)';
    });
    
    // 如果有点击回调，添加点击事件
    if (typeof settings.onClick === 'function') {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            settings.onClick(music);
        });
    }
    
    // 创建封面图片区域
    const imageContainer = document.createElement('div');
    imageContainer.className = 'music-card-image position-relative';
    
    // 添加封面图片
    const image = document.createElement('img');
    if (settings.lazyLoad) {
        image.className = 'card-img-top lazy-load';
        image.dataset.src = music.cover_image || '/static/images/default-cover.jpg';
        image.src = '/static/images/placeholder.jpg'; // 占位图片
    } else {
        image.className = 'card-img-top';
        image.src = music.cover_image || '/static/images/default-cover.jpg';
    }
    image.alt = music.title;
    image.style.height = settings.cardSize === 'small' ? '120px' : (settings.cardSize === 'large' ? '220px' : '180px');
    image.style.objectFit = 'cover';
    imageContainer.appendChild(image);
    
    // 添加播放按钮
    if (settings.showPlayButton) {
        const playButton = document.createElement('a');
        playButton.href = `/music/${music.id}/`;
        playButton.className = 'play-button position-absolute d-flex align-items-center justify-content-center';
        playButton.innerHTML = '<i class="fas fa-play"></i>';
        playButton.style.cssText = `
            bottom: 10px;
            right: 10px;
            width: 45px;
            height: 45px;
            background-color: var(--bs-primary);
            color: white;
            border-radius: 50%;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        `;
        playButton.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        playButton.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
        // 阻止冒泡，避免触发卡片的点击事件
        playButton.addEventListener('click', function(e) {
            e.stopPropagation();
        });
        imageContainer.appendChild(playButton);
    }
    
    card.appendChild(imageContainer);
    
    // 创建卡片内容区域
    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';
    
    // 添加标题
    const title = document.createElement('h5');
    title.className = 'card-title';
    title.textContent = music.title;
    cardBody.appendChild(title);
    
    // 添加音乐信息
    const infoList = document.createElement('div');
    infoList.className = 'd-flex flex-column gap-1 mb-2';
    
    // 艺术家
    const artistInfo = document.createElement('div');
    artistInfo.className = 'd-flex align-items-center';
    artistInfo.innerHTML = `<i class="fas fa-user text-muted me-2 fa-fw"></i><span class="text-truncate">${music.artist}</span>`;
    infoList.appendChild(artistInfo);
    
    // 专辑
    const albumInfo = document.createElement('div');
    albumInfo.className = 'd-flex align-items-center';
    albumInfo.innerHTML = `<i class="fas fa-compact-disc text-muted me-2 fa-fw"></i><span class="text-truncate">${music.album || '未知专辑'}</span>`;
    infoList.appendChild(albumInfo);
    
    // 发行日期
    const releaseDateInfo = document.createElement('div');
    releaseDateInfo.className = 'd-flex align-items-center';
    releaseDateInfo.innerHTML = `<i class="fas fa-calendar-alt text-muted me-2 fa-fw"></i><span>${music.release_date || '未知日期'}</span>`;
    infoList.appendChild(releaseDateInfo);
    
    cardBody.appendChild(infoList);
    
    // 添加卡片底部
    const cardFooter = document.createElement('div');
    cardFooter.className = 'card-footer d-flex justify-content-between align-items-center bg-transparent';
    
    // 添加文件大小信息
    const fileSize = document.createElement('small');
    fileSize.className = 'text-muted';
    fileSize.innerHTML = `<i class="fas fa-file-audio me-1"></i>${formatFileSize(music.file_size)}`;
    cardFooter.appendChild(fileSize);
    
    // 添加控制按钮
    if (settings.showControls) {
        const controls = document.createElement('div');
        controls.className = 'd-flex align-items-center';
        
        // 播放次数
        const playCount = document.createElement('span');
        playCount.className = 'me-2 text-muted';
        playCount.innerHTML = `<i class="fas fa-headphones me-1"></i>${music.play_count || 0}`;
        controls.appendChild(playCount);
        
        // 收藏按钮
        if (settings.showFavorite) {
            const favoriteBtn = document.createElement('button');
            favoriteBtn.type = 'button';
            favoriteBtn.className = 'btn btn-sm btn-link text-decoration-none p-0 favorite-btn';
            favoriteBtn.dataset.musicId = music.id;
            favoriteBtn.dataset.isFavorite = music.is_favorite ? 'true' : 'false';
            favoriteBtn.innerHTML = `<i class="${music.is_favorite ? 'fas fa-heart text-danger' : 'far fa-heart text-muted'}"></i>`;
            
            // 添加收藏点击事件
            favoriteBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                if (typeof settings.onFavoriteClick === 'function') {
                    settings.onFavoriteClick(music, this);
                }
            });
            
            controls.appendChild(favoriteBtn);
        }
        
        cardFooter.appendChild(controls);
    }
    
    card.appendChild(cardBody);
    card.appendChild(cardFooter);
    
    return card;
}

/**
 * 格式化文件大小
 * @param {number} bytes - 字节数
 * @returns {string} - 格式化后的文件大小
 */
function formatFileSize(bytes) {
    if (!bytes) return '0 B';
    const units = ['B', 'KB', 'MB', 'GB'];
    let i = 0;
    for (i; bytes >= 1024 && i < units.length - 1; i++) {
        bytes /= 1024;
    }
    return `${bytes.toFixed(1)} ${units[i]}`;
}

/**
 * 创建并渲染音乐卡片到容器中
 * @param {Array} musicList - 音乐数据列表
 * @param {string|HTMLElement} container - 容器选择器或DOM元素
 * @param {Object} options - 配置选项
 */
export function renderMusicCards(musicList, container, options = {}) {
    // 获取容器元素
    const containerEl = typeof container === 'string' 
        ? document.querySelector(container) 
        : container;
        
    if (!containerEl) {
        console.error('无法找到音乐卡片容器');
        return;
    }
    
    // 清空容器
    if (options.clearContainer !== false) {
        containerEl.innerHTML = '';
    }
    
    // 如果没有音乐，显示空状态
    if (!musicList || musicList.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'text-center py-5';
        emptyState.innerHTML = `
            <i class="fas fa-music fa-3x text-muted mb-3"></i>
            <h3>暂无音乐</h3>
            <p class="text-muted">没有找到符合条件的音乐</p>
        `;
        containerEl.appendChild(emptyState);
        return;
    }
    
    // 为每个音乐创建卡片
    musicList.forEach(music => {
        const card = createMusicCard(music, options);
        
        // 如果使用网格布局，需要包装在列元素中
        if (options.gridLayout) {
            const column = document.createElement('div');
            column.className = options.columnClass || 'col-md-6 col-lg-4 mb-4';
            column.appendChild(card);
            containerEl.appendChild(column);
        } else {
            containerEl.appendChild(card);
        }
    });
    
    // 如果启用延迟加载，初始化延迟加载功能
    if (options.lazyLoad !== false) {
        initLazyLoading();
    }
}

/**
 * 初始化图片延迟加载
 */
function initLazyLoading() {
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
} 