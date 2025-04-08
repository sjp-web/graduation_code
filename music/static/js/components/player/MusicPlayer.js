// Vue音乐播放器组件
import { formatTime } from '../../utils/formatters.js';

export default {
  props: {
    audioUrl: {
      type: String,
      required: true
    },
    title: {
      type: String,
      default: '未知歌曲'
    },
    artist: {
      type: String,
      default: '未知艺术家'
    },
    coverImage: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      isPlaying: false,
      duration: 0,
      currentTime: 0,
      volume: 0.7
    };
  },
  computed: {
    progressPercentage() {
      return (this.currentTime / this.duration) * 100;
    }
  },
  methods: {
    // 使用导入的格式化函数
    formatTime,
    
    // 播放/暂停控制
    togglePlay() {
      if (this.isPlaying) {
        this.$refs.audio.pause();
      } else {
        this.$refs.audio.play();
      }
      this.isPlaying = !this.isPlaying;
    },
    
    // 进度条控制
    handleProgressChange(e) {
      const progressBar = this.$refs.progressBar;
      const newTime = (e.offsetX / progressBar.offsetWidth) * this.duration;
      
      this.$refs.audio.currentTime = newTime;
      this.currentTime = newTime;
    },
    
    // 音量控制
    handleVolumeChange(e) {
      this.volume = e.target.value;
      this.$refs.audio.volume = this.volume;
    },
    
    // 后退10秒
    skipBackward() {
      this.$refs.audio.currentTime = Math.max(0, this.currentTime - 10);
    },
    
    // 前进10秒
    skipForward() {
      this.$refs.audio.currentTime = Math.min(this.duration, this.currentTime + 10);
    },
    
    // 初始化音频事件
    initAudioEvents() {
      const audio = this.$refs.audio;
      
      audio.addEventListener('loadeddata', () => {
        this.duration = audio.duration;
        this.currentTime = audio.currentTime;
      });
      
      audio.addEventListener('timeupdate', () => {
        this.currentTime = audio.currentTime;
      });
      
      audio.volume = this.volume;
    }
  },
  mounted() {
    this.initAudioEvents();
  },
  template: `
    <div class="vue-music-player">
      <!-- 封面和信息 -->
      <div class="player-header">
        <img v-if="coverImage" 
          :src="coverImage" 
          :alt="title + ' 封面'" 
          class="cover-image">
        <div class="track-info">
          <h3 class="track-title">{{ title }}</h3>
          <p class="track-artist">{{ artist }}</p>
        </div>
      </div>
      
      <!-- 进度控制 -->
      <div class="progress-container" 
        ref="progressBar" 
        @click="handleProgressChange">
        <div class="progress-bar" 
          :style="{ width: progressPercentage + '%' }">
        </div>
      </div>
      
      <!-- 时间显示 -->
      <div class="time-display">
        <span>{{ formatTime(currentTime) }}</span>
        <span>{{ formatTime(duration) }}</span>
      </div>
      
      <!-- 控制按钮 -->
      <div class="controls">
        <button class="control-button" @click="skipBackward">
          <i class="fas fa-backward"></i>
        </button>
        
        <button class="control-button play-button" @click="togglePlay">
          <i :class="['fas', isPlaying ? 'fa-pause' : 'fa-play']"></i>
        </button>
        
        <button class="control-button" @click="skipForward">
          <i class="fas fa-forward"></i>
        </button>
        
        <div class="volume-control">
          <i class="fas fa-volume-up"></i>
          <input type="range" 
            min="0" 
            max="1" 
            step="0.01" 
            :value="volume" 
            @input="handleVolumeChange" 
            class="volume-slider">
        </div>
      </div>
      
      <!-- 音频元素 -->
      <audio ref="audio" :src="audioUrl"></audio>
    </div>
  `
}; 