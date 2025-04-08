// Vue搜索应用入口文件
import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
import SearchComponent from './components/SearchComponent.js';

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', () => {
  // 查找搜索组件挂载点
  const searchContainer = document.getElementById('vue-search');
  
  if (searchContainer) {
    // 从DOM数据属性获取初始查询和路由信息
    const initialQuery = searchContainer.dataset.query || '';
    const searchRoute = searchContainer.dataset.searchRoute || '/search/';
    const suggestionsRoute = searchContainer.dataset.suggestionsRoute || '/search/suggestions/';
    
    // 创建Vue应用并挂载
    const app = createApp({
      components: {
        SearchComponent
      },
      data() {
        return {
          initialQuery,
          searchRoute,
          suggestionsRoute
        };
      },
      template: `
        <search-component 
          :initial-query="initialQuery"
          :search-route="searchRoute" 
          :suggestions-route="suggestionsRoute"
        />
      `
    });
    
    // 挂载到容器
    app.mount(searchContainer);
    
    console.log('Vue搜索组件已初始化');
  } else {
    console.warn('未找到Vue搜索组件挂载点');
  }
}); 