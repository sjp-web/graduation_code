// 使用全局React对象
const { useState, useEffect, useRef, lazy, Suspense, createElement } = React;
const { createRoot } = ReactDOM;

// 使用React.lazy和Suspense实现代码分割
const MusicPlayer = lazy(() => import('./components/ReactMusicPlayer.js'));

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', () => {
  // 查找所有需要渲染React音乐播放器的容器
  const playerContainers = document.querySelectorAll('.react-player-container');
  
  if (playerContainers.length > 0) {
    console.log(`找到${playerContainers.length}个音乐播放器挂载点`);
    
    // 为每个容器初始化React播放器
    playerContainers.forEach(container => {
      // 从容器的data属性中获取需要的数据
      const audioUrl = container.dataset.audioUrl;
      const title = container.dataset.title || '未知歌曲';
      const artist = container.dataset.artist || '未知艺术家';
      const coverImage = container.dataset.coverImage || null;
      
      // 检查必要的数据是否存在
      if (!audioUrl) {
        console.error('音乐播放器缺少音频文件URL');
        return;
      }
      
      try {
        // 创建React根并渲染组件
        const root = createRoot(container);
        root.render(
          createElement(Suspense, { fallback: '加载中...' },
            createElement(MusicPlayer, {
              audioUrl,
              title,
              artist,
              coverImage
            })
          )
        );
        console.log(`成功渲染播放器: ${title}`);
      } catch (error) {
        console.error('渲染React播放器时出错:', error);
        // 回退到原生HTML5播放器
        container.innerHTML = `
          <div class="fallback-player">
            <p>无法加载高级播放器。使用标准播放器:</p>
            <audio controls class="w-100">
              <source src="${audioUrl}" type="audio/mpeg">
              您的浏览器不支持音频播放
            </audio>
          </div>
        `;
      }
    });
  } else {
    console.warn('未找到React音乐播放器挂载点');
  }
}); 