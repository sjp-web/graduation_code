// 推荐页面组件
// 页面级组件，负责协调推荐音乐页面的功能

import { createApp } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';
import RecommendComponent from '../components/recommend/RecommendComponent.js';

// 初始化页面
document.addEventListener('DOMContentLoaded', () => {
    console.log('推荐页面初始化中...');
    
    // 获取挂载点
    const mountPoint = document.getElementById('vue-recommend-app');
    if (!mountPoint) {
        console.error('未找到推荐组件挂载点');
        return;
    }
    
    try {
        // 创建Vue应用并挂载
        const app = createApp(RecommendComponent);
        
        // 注册全局属性
        if (window.recommendAppData) {
            app.config.globalProperties.appData = window.recommendAppData;
        }
        
        // 挂载应用
        app.mount(mountPoint);
        console.log('推荐页面组件挂载成功');
        
        // 通知页面组件已加载完成
        document.dispatchEvent(new CustomEvent('recommendPageLoaded'));
    } catch (error) {
        console.error('推荐页面初始化失败:', error);
    }
});

// 导出页面初始化函数，便于外部调用
export function initRecommendPage() {
    console.log('手动初始化推荐页面');
    document.dispatchEvent(new Event('DOMContentLoaded'));
} 