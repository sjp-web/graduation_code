// 使用全局React对象
const { useState, useEffect, useRef, createElement } = React;

// 音乐播放器组件
const MusicPlayer = ({ audioUrl, title, artist, coverImage }) => {
  // 状态管理
  const [isPlaying, setIsPlaying] = useState(false);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [volume, setVolume] = useState(0.7);

  // 引用
  const audioRef = useRef(null);
  const progressBarRef = useRef(null);

  // 初始化音频
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    // 设置音频事件监听器
    const setAudioData = () => {
      setDuration(audio.duration);
      setCurrentTime(audio.currentTime);
    };

    const setAudioTime = () => setCurrentTime(audio.currentTime);
    
    // 事件监听
    audio.addEventListener('loadeddata', setAudioData);
    audio.addEventListener('timeupdate', setAudioTime);
    
    // 设置初始音量
    audio.volume = volume;
    
    // 清理函数
    return () => {
      audio.removeEventListener('loadeddata', setAudioData);
      audio.removeEventListener('timeupdate', setAudioTime);
    };
  }, [audioUrl, volume]);

  // 播放/暂停控制
  const togglePlay = () => {
    const audio = audioRef.current;
    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  };

  // 进度条控制
  const handleProgressChange = (e) => {
    const audio = audioRef.current;
    const progressBar = progressBarRef.current;
    
    // 计算新的当前时间
    const newTime = (e.nativeEvent.offsetX / progressBar.offsetWidth) * duration;
    
    // 更新音频当前时间
    audio.currentTime = newTime;
    setCurrentTime(newTime);
  };

  // 音量控制
  const handleVolumeChange = (e) => {
    const newVolume = e.target.value;
    setVolume(newVolume);
    audioRef.current.volume = newVolume;
  };

  // 格式化时间
  const formatTime = (time) => {
    if (isNaN(time)) return '0:00';
    
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60).toString().padStart(2, '0');
    return `${minutes}:${seconds}`;
  };

  return createElement('div', { className: 'react-music-player' },
    // 封面和信息
    createElement('div', { className: 'player-header' },
      coverImage && createElement('img', {
        src: coverImage,
        alt: `${title} 封面`,
        className: 'cover-image'
      }),
      createElement('div', { className: 'track-info' },
        createElement('h3', { className: 'track-title' }, title),
        createElement('p', { className: 'track-artist' }, artist)
      )
    ),
    
    // 进度控制
    createElement('div', {
      className: 'progress-container',
      ref: progressBarRef,
      onClick: handleProgressChange
    },
      createElement('div', {
        className: 'progress-bar',
        style: { width: `${(currentTime / duration) * 100}%` }
      })
    ),
    
    // 时间显示
    createElement('div', { className: 'time-display' },
      createElement('span', null, formatTime(currentTime)),
      createElement('span', null, formatTime(duration))
    ),
    
    // 控制按钮
    createElement('div', { className: 'controls' },
      createElement('button', {
        className: 'control-button',
        onClick: () => {
          audioRef.current.currentTime = Math.max(0, currentTime - 10);
        }
      },
        createElement('i', { className: 'fas fa-backward' })
      ),
      
      createElement('button', {
        className: 'control-button play-button',
        onClick: togglePlay
      },
        createElement('i', {
          className: `fas ${isPlaying ? 'fa-pause' : 'fa-play'}`
        })
      ),
      
      createElement('button', {
        className: 'control-button',
        onClick: () => {
          audioRef.current.currentTime = Math.min(duration, currentTime + 10);
        }
      },
        createElement('i', { className: 'fas fa-forward' })
      ),
      
      createElement('div', { className: 'volume-control' },
        createElement('i', { className: 'fas fa-volume-up' }),
        createElement('input', {
          type: 'range',
          min: '0',
          max: '1',
          step: '0.01',
          value: volume,
          onChange: handleVolumeChange,
          className: 'volume-slider'
        })
      )
    ),
    
    // 音频元素
    createElement('audio', {
      ref: audioRef,
      src: audioUrl
    })
  );
};

export default MusicPlayer; 