// 推荐音乐组件
// 使用ESM模块规范
import { ref, computed, onMounted, nextTick } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';

// 推荐组件定义
export default {
  name: 'RecommendComponent',
  
  setup() {
    // 状态管理
    const isLoading = ref(true);
    const recommendedMusic = ref([]);
    const errorMessage = ref('');
    
    // 获取是否为管理员的状态
    const isStaff = ref(false);
    if (window.recommendAppData && typeof window.recommendAppData.isStaff !== 'undefined') {
      isStaff.value = window.recommendAppData.isStaff;
      console.log("管理员状态:", isStaff.value);
    }
    
    // 获取推荐音乐数据
    const fetchRecommendedMusic = async () => {
      try {
        console.log("开始获取推荐音乐数据");
        isLoading.value = true;
        
        // 尝试从页面中获取预加载的数据
        const musicJsonElement = document.getElementById('recommended-music-json-data');
        if (musicJsonElement && musicJsonElement.textContent) {
          const jsonText = musicJsonElement.textContent.trim();
          console.log("找到预加载JSON数据长度:", jsonText.length);
          
          if (jsonText.length > 2) {  // 确保JSON不是空数组[]
            try {
              const parsedData = JSON.parse(jsonText);
              console.log("JSON解析成功, 数据项数:", parsedData.length);
              
              if (Array.isArray(parsedData) && parsedData.length > 0) {
                recommendedMusic.value = parsedData;
                console.log(`成功加载了 ${recommendedMusic.value.length} 首推荐音乐`);
                
                // 更新全局数据状态
                if (window.recommendAppData) {
                  window.recommendAppData.music = parsedData;
                }
                
                // 强制结束加载状态
                setTimeout(() => {
                  isLoading.value = false;
                  console.log("强制结束加载状态");
                }, 300);
              } else {
                console.warn("解析的JSON是空数组或非数组");
                errorMessage.value = "没有找到推荐音乐数据";
                isLoading.value = false;
              }
            } catch (parseError) {
              console.error("JSON解析失败:", parseError);
              errorMessage.value = "JSON数据格式错误";
              isLoading.value = false;
            }
          } else {
            console.warn("JSON数据为空");
            errorMessage.value = "推荐数据为空";
            isLoading.value = false;
          }
        } else {
          console.warn("未找到预加载的JSON数据元素");
          
          // 尝试回退到API请求
          try {
            const response = await fetch('/api/recommended_music/');
            if (!response.ok) {
              throw new Error(`服务器响应错误: ${response.status}`);
            }
            const data = await response.json();
            if (data.music && data.music.length > 0) {
              recommendedMusic.value = data.music;
              console.log(`从API加载了 ${recommendedMusic.value.length} 首推荐音乐`);
            } else {
              errorMessage.value = "API未返回推荐音乐数据";
            }
          } catch (apiError) {
            console.error("API请求失败:", apiError);
            errorMessage.value = `API请求失败: ${apiError.message}`;
          } finally {
            isLoading.value = false;
          }
        }
      } catch (error) {
        console.error('获取推荐音乐失败:', error);
        errorMessage.value = `获取推荐音乐失败: ${error.message}`;
        isLoading.value = false;
      } finally {
        console.log("数据加载完成，加载状态:", isLoading.value);
        console.log("当前推荐音乐数量:", recommendedMusic.value.length);
        
        // 通知父组件数据已准备就绪
        if (window.recommendEvents && window.recommendEvents.emit) {
          window.recommendEvents.emit('data-ready', {
            success: recommendedMusic.value.length > 0,
            count: recommendedMusic.value.length
          });
        }
      }
    };
    
    // 计算属性：是否有推荐音乐
    const hasRecommendedMusic = computed(() => {
      return recommendedMusic.value && recommendedMusic.value.length > 0;
    });
    
    // 生命周期钩子
    onMounted(() => {
      console.log("Vue组件已挂载，开始获取数据");
      fetchRecommendedMusic();
    });
    
    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (!bytes) return '0 B';
      const units = ['B', 'KB', 'MB', 'GB'];
      let i = 0;
      for (i; bytes >= 1024 && i < units.length - 1; i++) {
        bytes /= 1024;
      }
      return `${bytes.toFixed(1)} ${units[i]}`;
    };
    
    return {
      isLoading,
      recommendedMusic,
      errorMessage,
      hasRecommendedMusic,
      formatFileSize,
      isStaff
    };
  },
  template: `
    <div class="vue-recommend-container">
      <!-- 加载状态 -->
      <div v-if="isLoading" class="loading-spinner-container text-center py-5">
        <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
          <span class="visually-hidden">加载中...</span>
        </div>
        <p class="mt-3 text-primary">正在加载推荐音乐...</p>
      </div>
      
      <!-- 错误信息 -->
      <div v-if="errorMessage && !isLoading" class="error-message alert alert-danger">
        <i class="fas fa-exclamation-circle me-2"></i>{{ errorMessage }}
      </div>
      
      <!-- 推荐音乐列表 -->
      <div v-if="!isLoading" class="row g-4">
        <div v-for="music in recommendedMusic" :key="music.id" class="col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm hover-shadow-lg transition-all">
            <!-- 封面图片 -->
            <div class="position-relative">
              <img v-if="music.cover_image" :src="music.cover_image" class="card-img-top" :alt="music.title" 
                   style="height: 200px; object-fit: cover;">
              <div v-else class="card-img-top bg-light d-flex align-items-center justify-content-center" 
                   style="height: 200px;">
                <i class="fa-solid fa-compact-disc fa-3x text-muted"></i>
              </div>
              <!-- 播放按钮 -->
              <div class="position-absolute bottom-0 end-0 m-3">
                <a :href="'/music/' + music.id + '/'" class="btn btn-primary btn-lg rounded-circle shadow">
                  <i class="fa-solid fa-play"></i>
                </a>
              </div>
            </div>

            <!-- 音乐信息 -->
            <div class="card-body">
              <h5 class="card-title mb-3">
                <a :href="'/music/' + music.id + '/'" class="text-decoration-none stretched-link">
                  {{ music.title }}
                </a>
              </h5>
              <div class="d-flex flex-column gap-2">
                <div class="d-flex align-items-center">
                  <i class="fas fa-user me-2 text-muted"></i>
                  <span class="text-truncate">{{ music.artist }}</span>
                </div>
                <div class="d-flex align-items-center">
                  <i class="fas fa-compact-disc me-2 text-muted"></i>
                  <span class="text-truncate">{{ music.album }}</span>
                </div>
                <div class="d-flex align-items-center">
                  <i class="fas fa-calendar-alt me-2 text-muted"></i>
                  <span>{{ music.release_date }}</span>
                </div>
              </div>
              
              <!-- 推荐原因 -->
              <div v-if="music.recommendation_reason" class="recommendation-reason mt-3">
                <i class="fas fa-info-circle me-2"></i>
                <span>{{ music.recommendation_reason }}</span>
              </div>
            </div>
            
            <div class="card-footer bg-transparent">
              <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted">
                  <i class="fas fa-file-audio me-1"></i>
                  {{ formatFileSize(music.file_size) }}
                </small>
                <div>
                  <span class="text-muted me-2">
                    <i class="fas fa-headphones me-1"></i>{{ music.play_count || 0 }}
                  </span>
                  <span class="text-muted">
                    <i class="fas fa-heart me-1"></i>{{ music.likes_count || 0 }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 无推荐音乐时的提示 -->
      <div v-if="!isLoading && !hasRecommendedMusic && !errorMessage" class="empty-state text-center py-5">
        <i class="fas fa-music fa-3x text-muted mb-3"></i>
        <h3 class="h4">没有找到推荐的音乐</h3>
        <p class="text-muted">您可以先浏览一些音乐，我们之后会为您推荐您可能喜欢的音乐</p>
      </div>
    </div>
  `
}; 