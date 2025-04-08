// 音乐播放器页面入口文件
import { createApp, defineAsyncComponent } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';

// 使用异步组件实现代码分割
const MusicPlayer = defineAsyncComponent(() => 
  import('../components/player/MusicPlayer.js')
);

// 创建页面应用
const createMusicPlayerApp = (container) => {
  // 从容器的data属性中获取需要的数据
  const audioUrl = container.dataset.audioUrl;
  const title = container.dataset.title || '未知歌曲';
  const artist = container.dataset.artist || '未知艺术家';
  const coverImage = container.dataset.coverImage || null;
  
  // 检查必要的数据是否存在
  if (!audioUrl) {
    console.error('音乐播放器缺少音频文件URL');
    return null;
  }
  
  try {
    // 创建Vue应用并挂载
    const app = createApp({
      components: {
        MusicPlayer
      },
      data() {
        return {
          audioUrl,
          title,
          artist,
          coverImage
        };
      },
      template: `
        <music-player 
          :audio-url="audioUrl"
          :title="title"
          :artist="artist" 
          :cover-image="coverImage"
        />
      `
    });
    
    // 挂载到容器
    app.mount(container);
    console.log(`成功渲染播放器: ${title}`);
    return app;
  } catch (error) {
    console.error('渲染Vue播放器时出错:', error);
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
    return null;
  }
};

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', () => {
  // 查找所有需要渲染Vue音乐播放器的容器
  const playerContainers = document.querySelectorAll('.vue-player-container');
  
  if (playerContainers.length > 0) {
    console.log(`找到${playerContainers.length}个音乐播放器挂载点`);
    
    // 为每个容器初始化Vue播放器
    playerContainers.forEach(container => {
      createMusicPlayerApp(container);
    });
  } else {
    console.warn('未找到Vue音乐播放器挂载点');
  }
}); 