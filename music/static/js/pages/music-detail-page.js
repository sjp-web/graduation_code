// 音乐详情页面组件
// 页面级组件，负责音乐详情页面的评论和播放功能

import { createApp } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';

// 初始化页面
document.addEventListener('DOMContentLoaded', () => {
    console.log('音乐详情页面初始化中...');
    
    // 获取挂载点
    const mountPoint = document.getElementById('music-detail-app');
    if (!mountPoint) {
        console.log('未找到音乐详情组件挂载点，使用传统JS增强');
        initTraditionalFeatures();
        return;
    }
    
    try {
        // 获取音乐数据
        const musicDataElement = document.getElementById('music-detail-data');
        let musicData = {};
        
        if (musicDataElement && musicDataElement.textContent) {
            try {
                musicData = JSON.parse(musicDataElement.textContent);
                console.log('成功加载音乐详情数据');
            } catch (error) {
                console.error('解析音乐详情数据失败:', error);
            }
        }
        
        // 创建Vue应用
        const app = createApp({
            data() {
                return {
                    music: musicData.music || {},
                    comments: musicData.comments || [],
                    lyrics: musicData.lyrics || '',
                    lyricsLines: musicData.lyricsLines || [],
                    currentUser: musicData.currentUser || null,
                    isPlaying: false,
                    currentTime: 0,
                    duration: 0,
                    volumeLevel: 0.8,
                    isMuted: false,
                    commentContent: '',
                    commentError: '',
                    isSubmitting: false,
                    csrfToken: document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                };
            },
            computed: {
                formattedCurrentTime() {
                    return this.formatTime(this.currentTime);
                },
                formattedDuration() {
                    return this.formatTime(this.duration);
                },
                playProgress() {
                    return this.duration ? (this.currentTime / this.duration) * 100 : 0;
                },
                volumePercent() {
                    return this.isMuted ? 0 : this.volumeLevel * 100;
                },
                canSubmitComment() {
                    return this.commentContent.trim().length > 0 && !this.isSubmitting;
                }
            },
            methods: {
                // 格式化时间为 MM:SS 格式
                formatTime(seconds) {
                    seconds = Math.floor(seconds);
                    const minutes = Math.floor(seconds / 60);
                    seconds = seconds % 60;
                    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
                },
                
                // 播放/暂停切换
                togglePlay() {
                    const audio = document.getElementById('audioPlayer');
                    if (!audio) return;
                    
                    if (this.isPlaying) {
                        audio.pause();
                    } else {
                        audio.play();
                    }
                    this.isPlaying = !this.isPlaying;
                },
                
                // 更新播放时间
                updateTime() {
                    const audio = document.getElementById('audioPlayer');
                    if (!audio) return;
                    
                    this.currentTime = audio.currentTime;
                    if (this.currentTime === this.duration) {
                        this.isPlaying = false;
                    }
                },
                
                // 加载音频元数据
                loadMetadata() {
                    const audio = document.getElementById('audioPlayer');
                    if (!audio) return;
                    
                    this.duration = audio.duration;
                },
                
                // 设置播放位置
                setPlayPosition(event) {
                    const audio = document.getElementById('audioPlayer');
                    if (!audio) return;
                    
                    const progressBar = event.currentTarget;
                    const clickPosition = event.offsetX / progressBar.offsetWidth;
                    audio.currentTime = clickPosition * audio.duration;
                    this.currentTime = audio.currentTime;
                },
                
                // 调整音量
                setVolume(event) {
                    const audio = document.getElementById('audioPlayer');
                    if (!audio) return;
                    
                    const volumeBar = event.currentTarget;
                    const clickPosition = event.offsetX / volumeBar.offsetWidth;
                    this.volumeLevel = Math.max(0, Math.min(1, clickPosition));
                    audio.volume = this.volumeLevel;
                    this.isMuted = this.volumeLevel === 0;
                },
                
                // 静音切换
                toggleMute() {
                    const audio = document.getElementById('audioPlayer');
                    if (!audio) return;
                    
                    if (this.isMuted) {
                        audio.volume = this.volumeLevel;
                        this.isMuted = false;
                    } else {
                        audio.volume = 0;
                        this.isMuted = true;
                    }
                },
                
                // 提交评论
                async submitComment() {
                    if (!this.canSubmitComment) return;
                    
                    this.isSubmitting = true;
                    this.commentError = '';
                    
                    try {
                        const response = await fetch(window.location.pathname, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'X-CSRFToken': this.csrfToken
                            },
                            body: new URLSearchParams({
                                content: this.commentContent
                            }),
                            credentials: 'same-origin'
                        });
                        
                        if (response.ok) {
                            // 假设服务器返回的是新评论数据
                            // 在实际情况下，你可能需要刷新整个页面或处理返回数据
                            // 这里我们简单地添加一个新评论并清空输入框
                            this.comments.push({
                                id: Date.now(), // 临时ID
                                content: this.commentContent,
                                user: this.currentUser,
                                created_at: new Date().toISOString()
                            });
                            this.commentContent = '';
                            
                            // 重新加载页面以获取最新数据
                            window.location.reload();
                        } else {
                            throw new Error('评论提交失败');
                        }
                    } catch (error) {
                        console.error('提交评论失败:', error);
                        this.commentError = '评论提交失败，请稍后再试';
                    } finally {
                        this.isSubmitting = false;
                    }
                },
                
                // 删除评论
                async deleteComment(commentId) {
                    if (!confirm('确定要删除此评论吗？')) return;
                    
                    try {
                        const response = await fetch(window.location.pathname, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'X-CSRFToken': this.csrfToken
                            },
                            body: new URLSearchParams({
                                comment_id: commentId
                            }),
                            credentials: 'same-origin'
                        });
                        
                        if (response.ok) {
                            // 从列表中移除评论
                            this.comments = this.comments.filter(comment => comment.id !== commentId);
                            
                            // 重新加载页面以获取最新数据
                            window.location.reload();
                        } else {
                            throw new Error('评论删除失败');
                        }
                    } catch (error) {
                        console.error('删除评论失败:', error);
                        alert('评论删除失败，请稍后再试');
                    }
                },
                
                // 下载音乐
                downloadMusic() {
                    if (this.music.id) {
                        window.location.href = `/music/download/${this.music.id}/`;
                    }
                }
            },
            mounted() {
                // 初始化音频播放器
                const audio = document.getElementById('audioPlayer');
                if (audio) {
                    // 监听音频事件
                    audio.addEventListener('timeupdate', this.updateTime);
                    audio.addEventListener('loadedmetadata', this.loadMetadata);
                    
                    // 设置初始音量
                    audio.volume = this.volumeLevel;
                }
            },
            template: `
                <div class="music-detail-page">
                    <!-- 可以根据需要添加Vue模板内容 -->
                </div>
            `
        });
        
        // 挂载应用
        app.mount(mountPoint);
        console.log('音乐详情页面组件挂载成功');
        
    } catch (error) {
        console.error('音乐详情页面初始化失败:', error);
        // 初始化传统功能
        initTraditionalFeatures();
    }
    
    // 确保备用播放器逻辑
    initFallbackPlayer();
});

// 初始化备用播放器
function initFallbackPlayer() {
    const vueContainer = document.querySelector('.vue-player-container');
    const fallbackPlayer = document.getElementById('fallbackPlayer');
    
    if (vueContainer && fallbackPlayer) {
        // 等待2秒检查Vue播放器是否渲染成功
        setTimeout(() => {
            // 如果Vue播放器内部没有内容，显示备用播放器
            if (vueContainer.children.length === 0) {
                console.log('Vue播放器未渲染，显示备用播放器');
                fallbackPlayer.classList.remove('d-none');
                
                // 从容器中获取音乐信息
                const audioUrl = vueContainer.dataset.audioUrl;
                const title = vueContainer.dataset.title;
                
                // 设置音频源
                if (fallbackPlayer.querySelector('source')) {
                    fallbackPlayer.querySelector('source').src = audioUrl;
                    fallbackPlayer.load();
                }
            }
        }, 2000);
    }
}

// 初始化传统功能（当Vue无法挂载时）
function initTraditionalFeatures() {
    console.log('使用传统JS增强功能');
    
    // 评论表单提交效果
    const commentForm = document.querySelector('.card-footer form');
    if (commentForm) {
        commentForm.addEventListener('submit', function(event) {
            const submitButton = this.querySelector('button[type="submit"]');
            const textarea = this.querySelector('textarea');
            
            if (textarea && textarea.value.trim() === '') {
                event.preventDefault();
                textarea.classList.add('is-invalid');
                return false;
            }
            
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>提交中...';
            }
        });
    }
    
    // 评论删除确认
    const deleteButtons = document.querySelectorAll('form button[type="submit"]');
    deleteButtons.forEach(button => {
        if (button.closest('form').querySelector('input[name="comment_id"]')) {
            button.addEventListener('click', function(event) {
                if (!confirm('确定要删除此评论吗？')) {
                    event.preventDefault();
                    return false;
                }
                
                this.disabled = true;
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>删除中...';
            });
        }
    });
}

// 导出页面初始化函数，便于外部调用
export function initMusicDetailPage() {
    console.log('手动初始化音乐详情页面');
    document.dispatchEvent(new Event('DOMContentLoaded'));
} 