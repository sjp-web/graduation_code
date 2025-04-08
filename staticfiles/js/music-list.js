// 音乐列表增强脚本
document.addEventListener('DOMContentLoaded', function() {
    // 为音乐卡片添加动画效果
    const musicCards = document.querySelectorAll('.music-card-modern');
    
    // 添加卡片进入动画
    musicCards.forEach((card, index) => {
        // 设置初始状态：透明和向下偏移
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        // 使用延迟错开动画，形成瀑布效果
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + (index * 50)); // 每张卡片延迟50ms
    });
    
    // 添加音乐卡片悬停音效（可选）
    musicCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            // 播放轻微的音效，增强交互体验
            // 这里可以添加一个微小的音效，增强用户体验
            // 如果想添加音效，可以取消下面的注释
            /*
            const hoverSound = new Audio('/static/sounds/hover.mp3');
            hoverSound.volume = 0.2;
            hoverSound.play();
            */
        });
        
        // 点击卡片播放动画效果
        card.addEventListener('click', function(e) {
            // 如果点击的是播放按钮，则添加波纹动画效果
            if (e.target.closest('.play-btn')) {
                const playBtn = e.target.closest('.play-btn');
                
                // 创建波纹元素
                const ripple = document.createElement('span');
                ripple.classList.add('ripple-effect');
                playBtn.appendChild(ripple);
                
                // 设置波纹位置和动画
                const btnRect = playBtn.getBoundingClientRect();
                ripple.style.width = ripple.style.height = Math.max(btnRect.width, btnRect.height) + 'px';
                ripple.style.left = (e.clientX - btnRect.left - ripple.offsetWidth / 2) + 'px';
                ripple.style.top = (e.clientY - btnRect.top - ripple.offsetHeight / 2) + 'px';
                
                // 动画结束后移除波纹元素
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            }
        });
    });
    
    // 过滤面板效果
    const filterPanel = document.querySelector('.filter-panel-modern');
    if (filterPanel) {
        // 添加表单提交时的加载指示器
        const filterForm = filterPanel.querySelector('form');
        const submitBtn = filterForm.querySelector('button[type="submit"]');
        
        filterForm.addEventListener('submit', (e) => {
            // 禁用按钮并显示加载状态
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> 加载中...';
        });
    }
    
    // 添加滚动动画效果
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.music-collection-header, .filter-panel-modern');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.classList.add('animated');
            }
        });
    };
    
    // 初始化滚动动画
    animateOnScroll();
    
    // 监听滚动事件
    window.addEventListener('scroll', animateOnScroll);
}); 