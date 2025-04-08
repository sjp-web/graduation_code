// Vue音乐播放器组件
export default {
  name: 'MusicPlayer',
  props: {
    audioUrl: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    artist: {
      type: String,
      required: true
    },
    coverUrl: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      audio: null,
      isPlaying: false,
      isMuted: false,
      currentTime: 0,
      duration: 0,
      volume: 100,
      progressPercent: 0,
      dragging: false
    };
  },
  computed: {
    // 格式化当前时间显示
    formattedCurrentTime() {
      return this.formatTime(this.currentTime);
    },
    // 格式化总时长显示
    formattedDuration() {
      return this.formatTime(this.duration);
    },
    // 获取音量图标样式
    volumeIcon() {
      if (this.isMuted || this.volume === 0) {
        return 'fa-volume-mute';
      } else if (this.volume < 50) {
        return 'fa-volume-down';
      } else {
        return 'fa-volume-up';
      }
    },
    // 悬停提示文本
    volumeTooltip() {
      return this.isMuted ? '取消静音' : '静音';
    },
    // 播放按钮图标样式
    playIcon() {
      return this.isPlaying ? 'fa-pause' : 'fa-play';
    },
    // 悬停提示文本
    playTooltip() {
      return this.isPlaying ? '暂停' : '播放';
    }
  },
  mounted() {
    // 初始化音频对象
    this.audio = new Audio(this.audioUrl);
    
    // 设置事件监听
    this.audio.addEventListener('timeupdate', this.updateProgress);
    this.audio.addEventListener('loadedmetadata', this.setDuration);
    this.audio.addEventListener('ended', this.handleEnded);
    
    // 设置音量
    this.audio.volume = this.volume / 100;
    
    // 记录初始加载
    console.log(`加载音频: ${this.title} - ${this.artist}`);
  },
  beforeUnmount() {
    // 移除事件监听，防止内存泄漏
    if (this.audio) {
      this.audio.removeEventListener('timeupdate', this.updateProgress);
      this.audio.removeEventListener('loadedmetadata', this.setDuration);
      this.audio.removeEventListener('ended', this.handleEnded);
      
      // 停止播放并释放资源
      this.audio.pause();
      this.audio.src = '';
      this.audio = null;
    }
  },
  methods: {
    // 格式化时间显示
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      seconds = Math.floor(seconds % 60);
      return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    },
    
    // 切换播放/暂停状态
    togglePlay() {
      if (this.isPlaying) {
        this.audio.pause();
      } else {
        this.audio.play();
      }
      this.isPlaying = !this.isPlaying;
    },
    
    // 切换静音状态
    toggleMute() {
      this.isMuted = !this.isMuted;
      this.audio.muted = this.isMuted;
    },
    
    // 更新播放进度
    updateProgress() {
      if (!this.dragging) {
        this.currentTime = this.audio.currentTime;
        this.progressPercent = (this.currentTime / this.duration) * 100;
      }
    },
    
    // 设置总时长
    setDuration() {
      this.duration = this.audio.duration;
    },
    
    // 播放结束处理
    handleEnded() {
      this.isPlaying = false;
      this.currentTime = 0;
      this.progressPercent = 0;
    },
    
    // 调整音量
    updateVolume(e) {
      const volume = parseInt(e.target.value);
      this.volume = volume;
      this.audio.volume = volume / 100;
      
      // 如果音量大于0但当前是静音状态，则取消静音
      if (volume > 0 && this.isMuted) {
        this.isMuted = false;
        this.audio.muted = false;
      }
    },
    
    // 调整播放进度
    seekTo(e) {
      const rect = e.target.getBoundingClientRect();
      const pos = (e.clientX - rect.left) / rect.width;
      this.progressPercent = pos * 100;
      this.currentTime = pos * this.duration;
      this.audio.currentTime = this.currentTime;
    },
    
    // 开始拖动进度条
    startDrag() {
      this.dragging = true;
    },
    
    // 结束拖动进度条
    endDrag() {
      this.dragging = false;
      this.audio.currentTime = this.currentTime;
    }
  },
  template: `
    <div class="vue-music-player">
      <div class="player-info">
        <div class="cover-image" v-if="coverUrl">
          <img :src="coverUrl" :alt="title" />
        </div>
        <div class="track-info">
          <div class="track-title">{{ title }}</div>
          <div class="track-artist">{{ artist }}</div>
        </div>
      </div>
      
      <div class="player-controls">
        <button 
          class="play-btn" 
          @click="togglePlay" 
          :title="playTooltip"
        >
          <i :class="['fas', playIcon, 'fa-lg']"></i>
        </button>
        
        <div class="progress-container">
          <div class="time current-time">{{ formattedCurrentTime }}</div>
          <div 
            class="progress" 
            @click="seekTo"
            @mousedown="startDrag"
            @mouseup="endDrag"
            @mouseleave="endDrag"
          >
            <div 
              class="progress-bar" 
              :style="{ width: progressPercent + '%' }"
            ></div>
          </div>
          <div class="time duration">{{ formattedDuration }}</div>
        </div>
        
        <div class="volume-control">
          <button 
            class="mute-btn" 
            @click="toggleMute"
            :title="volumeTooltip"
          >
            <i :class="['fas', volumeIcon, 'fa-lg']"></i>
          </button>
          <input 
            type="range" 
            class="volume-slider" 
            min="0" 
            max="100" 
            :value="volume"
            @input="updateVolume"
          />
        </div>
      </div>
    </div>
  `
}; 