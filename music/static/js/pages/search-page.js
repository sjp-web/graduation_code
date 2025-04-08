// 搜索页面入口文件
import { createApp, defineAsyncComponent } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
import { createConfiguredApp } from '../utils/component-registry.js';

// 使用异步组件实现代码分割
const SearchComponent = defineAsyncComponent(() => 
  import('../components/search/SearchComponent.js')
);

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', () => {
  // 查找搜索组件挂载点
  const searchContainer = document.getElementById('vue-search-app');
  
  if (searchContainer) {
    // 获取初始查询和API路由
    const initialQuery = searchContainer.dataset.initialQuery || '';
    const searchRoute = searchContainer.dataset.searchRoute || '/api/music/search/';
    const suggestionsRoute = searchContainer.dataset.suggestionsRoute || '/api/music/suggestions/';
    
    // 创建Vue应用
    const app = createConfiguredApp({
      components: {
        SearchComponent
      },
      template: `
        <search-component
          :initial-query="initialQuery"
          :search-route="searchRoute"
          :suggestions-route="suggestionsRoute"
        />
      `,
      data() {
        return {
          initialQuery,
          searchRoute,
          suggestionsRoute
        };
      }
    });
    
    // 挂载到容器
    app.mount(searchContainer);
    console.log('搜索应用初始化成功');
  } else {
    console.warn('未找到搜索应用挂载点');
  }
}); 