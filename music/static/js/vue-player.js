// Vue音乐播放器入口文件
import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
import MusicPlayer from './components/MusicPlayer.js';

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', () => {
  // 查找播放器挂载点
  const playerContainer = document.getElementById('vue-music-player');
  
  if (playerContainer) {
    // 从DOM数据属性获取音乐信息
    const musicData = {
      audioUrl: playerContainer.dataset.audioUrl,
      title: playerContainer.dataset.title,
      artist: playerContainer.dataset.artist,
      coverUrl: playerContainer.dataset.coverUrl || null
    };
    
    // 创建Vue应用并挂载
    const app = createApp({
      components: {
        MusicPlayer
      },
      data() {
        return {
          music: musicData
        };
      },
      template: `
        <music-player 
          :audio-url="music.audioUrl"
          :title="music.title"
          :artist="music.artist" 
          :cover-url="music.coverUrl"
        />
      `
    });
    
    // 挂载到容器
    app.mount(playerContainer);
    
    console.log('Vue音乐播放器已初始化');
  } else {
    console.warn('未找到Vue音乐播放器挂载点');
  }
}); 