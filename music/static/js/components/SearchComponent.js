// Vue搜索组件，提供即时搜索和结果预览功能
export default {
  name: 'SearchComponent',
  props: {
    initialQuery: {
      type: String,
      default: ''
    },
    searchRoute: {
      type: String,
      required: true
    },
    suggestionsRoute: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      query: this.initialQuery,
      suggestions: [],
      searchResults: [],
      isLoading: false,
      showSuggestions: false,
      showAdvanced: false,
      advancedFilters: {
        artist: '',
        album: '',
        year: ''
      },
      availableYears: [],
      currentPage: 1,
      totalPages: 0,
      resultsPerPage: 5,
      searchTimeout: null,
      viewMode: 'list', // 'list' 或 'grid'
      totalResults: 0,
      selectedResult: -1,
      lastApiCallTime: 0,
      minApiCallInterval: 300, // 毫秒，防抖阈值
      playingIndex: -1 // 新增：当前正在播放的音频索引
    };
  },
  computed: {
    hasResults() {
      return this.searchResults.length > 0;
    },
    hasMoreResults() {
      return this.currentPage < this.totalPages;
    },
    effectiveQuery() {
      return this.query.trim();
    },
    showLoadMore() {
      return this.hasMoreResults && !this.isLoading;
    }
  },
  watch: {
    query(newQuery) {
      // 清除上一个定时器
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }
      
      // 如果查询为空，清空建议
      if (!newQuery.trim()) {
        this.suggestions = [];
        this.showSuggestions = false;
        return;
      }
      
      // 设置节流的搜索请求
      this.searchTimeout = setTimeout(() => {
        this.fetchSuggestions();
      }, 300);
    }
  },
  mounted() {
    // 加载可用年份数据
    this.loadYears();
    
    // 如果有初始查询，执行搜索
    if (this.initialQuery) {
      this.search();
    }
    
    // 点击页面其他位置时隐藏建议
    document.addEventListener('click', this.handleOutsideClick);
    
    // 添加键盘导航事件监听
    document.addEventListener('keydown', this.handleKeyDown);
  },
  beforeUnmount() {
    // 移除事件监听器，防止内存泄漏
    document.removeEventListener('click', this.handleOutsideClick);
    document.removeEventListener('keydown', this.handleKeyDown);
  },
  methods: {
    // 加载可用年份数据
    async loadYears() {
      try {
        const response = await fetch('/api/years/');
        const data = await response.json();
        this.availableYears = data.years;
      } catch (error) {
        console.error('加载年份数据失败:', error);
      }
    },
    
    // 获取搜索建议
    async fetchSuggestions() {
      // 如果查询太短或为空，不执行搜索
      if (this.effectiveQuery.length < 2) {
        this.suggestions = [];
        this.showSuggestions = false;
        return;
      }
      
      // 检查API调用频率
      const now = Date.now();
      if (now - this.lastApiCallTime < this.minApiCallInterval) {
        return;
      }
      this.lastApiCallTime = now;
      
      try {
        const response = await fetch(`${this.suggestionsRoute}?q=${encodeURIComponent(this.effectiveQuery)}`);
        const data = await response.json();
        this.suggestions = data.suggestions;
        this.showSuggestions = this.suggestions.length > 0;
        this.selectedResult = -1; // 重置选择
      } catch (error) {
        console.error('获取搜索建议失败:', error);
        this.showSuggestions = false;
      }
    },
    
    // 执行搜索
    async search(page = 1) {
      if (!this.effectiveQuery && !this.hasAdvancedFilters()) {
        return;
      }
      
      this.isLoading = true;
      this.showSuggestions = false;
      this.currentPage = page;
      
      try {
        // 构建URL查询参数
        const params = new URLSearchParams();
        params.append('q', this.effectiveQuery);
        params.append('page', page);
        
        // 添加高级筛选参数
        if (this.advancedFilters.artist) {
          params.append('artist', this.advancedFilters.artist);
        }
        if (this.advancedFilters.album) {
          params.append('album', this.advancedFilters.album);
        }
        if (this.advancedFilters.year) {
          params.append('year', this.advancedFilters.year);
        }
        
        // 添加JSON格式参数
        params.append('format', 'json');
        
        const response = await fetch(`${this.searchRoute}?${params.toString()}`);
        const data = await response.json();
        
        if (page === 1) {
          this.searchResults = data.results;
        } else {
          // 追加结果
          this.searchResults = [...this.searchResults, ...data.results];
        }
        
        this.totalResults = data.total;
        this.totalPages = data.total_pages;
        
        // 如果是第一页且有结果，滚动到结果区域
        if (page === 1 && this.searchResults.length > 0) {
          this.$nextTick(() => {
            const resultsContainer = document.getElementById('search-results');
            if (resultsContainer) {
              resultsContainer.scrollIntoView({ behavior: 'smooth' });
            }
          });
        }
      } catch (error) {
        console.error('搜索失败:', error);
      } finally {
        this.isLoading = false;
      }
    },
    
    // 选择搜索建议
    selectSuggestion(suggestion) {
      // 新代码：处理"歌曲名 - 艺术家"格式
      // 建议格式为"歌曲名 - 艺术家"，我们需要提取歌曲名和艺术家
      if (suggestion.includes(' - ')) {
        const [title, artist] = suggestion.split(' - ');
        // 设置歌曲名为主查询
        this.query = title;
        // 设置艺术家为高级筛选条件
        this.advancedFilters.artist = artist;
        // 显示高级筛选面板
        this.showAdvanced = true;
      } else {
        // 不含分隔符的情况，保持原有处理
        this.query = suggestion;
      }
      
      this.showSuggestions = false;
      this.search();
    },
    
    // 加载更多结果
    loadMore() {
      if (this.hasMoreResults && !this.isLoading) {
        this.search(this.currentPage + 1);
      }
    },
    
    // 切换视图模式
    toggleViewMode(mode) {
      this.viewMode = mode;
    },
    
    // 检查是否有高级筛选条件
    hasAdvancedFilters() {
      return this.advancedFilters.artist || 
             this.advancedFilters.album || 
             this.advancedFilters.year;
    },
    
    // 切换高级搜索面板
    toggleAdvanced() {
      this.showAdvanced = !this.showAdvanced;
    },
    
    // 重置搜索条件
    resetSearch() {
      this.query = '';
      this.advancedFilters = {
        artist: '',
        album: '',
        year: ''
      };
      this.searchResults = [];
      this.totalResults = 0;
    },
    
    // 页面点击事件，关闭搜索建议
    handleOutsideClick(event) {
      const searchContainer = this.$el.querySelector('.search-container');
      if (searchContainer && !searchContainer.contains(event.target)) {
        this.showSuggestions = false;
      }
    },
    
    // 键盘导航
    handleKeyDown(event) {
      // 如果建议不显示，不处理键盘事件
      if (!this.showSuggestions) {
        return;
      }
      
      switch (event.key) {
        case 'ArrowDown':
          // 向下选择
          event.preventDefault();
          this.selectedResult = Math.min(this.selectedResult + 1, this.suggestions.length - 1);
          break;
        case 'ArrowUp':
          // 向上选择
          event.preventDefault();
          this.selectedResult = Math.max(this.selectedResult - 1, -1);
          break;
        case 'Enter':
          // 选择当前项目
          if (this.selectedResult >= 0 && this.selectedResult < this.suggestions.length) {
            event.preventDefault();
            this.selectSuggestion(this.suggestions[this.selectedResult]);
          }
          break;
        case 'Escape':
          // 关闭建议
          event.preventDefault();
          this.showSuggestions = false;
          break;
      }
    },
    
    // 直接前往音乐详情页
    goToMusicDetail(id) {
      window.location.href = `/music/${id}/`;
    },
    
    // 播放音频预览
    togglePreview(index) {
      const audioElements = document.querySelectorAll('.preview-audio');
      const audioElement = audioElements[index];
      const progressBars = document.querySelectorAll('.results-list .progress-bar, .results-grid .progress-bar');
      const progressBar = progressBars[index];
      
      // 暂停其他所有音频
      audioElements.forEach((audio, i) => {
        if (i !== index && !audio.paused) {
          audio.pause();
          // 重置其他进度条
          if (progressBars[i]) {
            progressBars[i].style.width = '0%';
          }
        }
      });
      
      // 切换当前音频播放状态
      if (audioElement.paused) {
        audioElement.play();
        this.playingIndex = index;  // 更新当前播放索引
        
        // 添加时间更新事件监听器
        audioElement.addEventListener('timeupdate', () => {
          const percent = (audioElement.currentTime / audioElement.duration) * 100;
          if (progressBar) {
            progressBar.style.width = percent + '%';
          }
        });
        
        // 播放结束时重置进度条和播放状态
        audioElement.addEventListener('ended', () => {
          if (progressBar) {
            progressBar.style.width = '0%';
          }
          this.playingIndex = -1;  // 重置播放索引
        });
      } else {
        audioElement.pause();
        this.playingIndex = -1;  // 重置播放索引
      }
    },
    
    // 获取播放按钮的图标
    getPlayButtonIcon(index) {
      return this.playingIndex === index ? 'fa-pause' : 'fa-play';
    }
  },
  template: `
    <div class="vue-search-component">
      <!-- 搜索表单 -->
      <div class="search-container">
        <div class="card shadow-lg mb-4">
          <div class="card-body p-4">
            <div class="input-group input-group-lg mb-3">
              <input type="text" 
                     v-model="query" 
                     class="form-control" 
                     placeholder="输入歌曲名称、艺术家或专辑..."
                     @focus="fetchSuggestions"
                     @input="fetchSuggestions"
                     aria-label="搜索音乐">
              <button type="button" class="btn btn-primary" @click="search()">
                <i class="fas fa-search"></i>
              </button>
            </div>
            
            <!-- 搜索建议下拉 -->
            <div v-if="showSuggestions" class="search-suggestions card">
              <ul class="list-group list-group-flush">
                <li v-for="(suggestion, index) in suggestions" 
                    :key="index" 
                    class="list-group-item" 
                    :class="{'active': index === selectedResult}"
                    @click="selectSuggestion(suggestion)">
                  <i class="fas fa-music me-2"></i>{{ suggestion }}
                </li>
              </ul>
            </div>
            
            <!-- 高级筛选 -->
            <div class="advanced-filters" v-show="showAdvanced">
              <div class="row g-3 mb-3">
                <div class="col-md-4">
                  <label class="form-label">艺术家</label>
                  <input type="text" v-model="advancedFilters.artist" class="form-control">
                </div>
                <div class="col-md-4">
                  <label class="form-label">专辑</label>
                  <input type="text" v-model="advancedFilters.album" class="form-control">
                </div>
                <div class="col-md-4">
                  <label class="form-label">发行年份</label>
                  <select v-model="advancedFilters.year" class="form-select">
                    <option value="">所有年份</option>
                    <option v-for="year in availableYears" :key="year" :value="year">
                      {{ year }}
                    </option>
                  </select>
                </div>
              </div>
              
              <div class="text-end">
                <button type="button" class="btn btn-outline-secondary me-2" @click="resetSearch">
                  <i class="fas fa-times me-1"></i>重置
                </button>
                <button type="button" class="btn btn-primary" @click="search()">
                  <i class="fas fa-filter me-1"></i>应用筛选
                </button>
              </div>
            </div>
            
            <!-- 高级筛选切换按钮 -->
            <div class="text-center mt-3">
              <button type="button" 
                      class="btn btn-link btn-sm text-decoration-none" 
                      @click="toggleAdvanced">
                <i class="fas fa-sliders-h me-1"></i>
                {{ showAdvanced ? '收起高级筛选' : '高级筛选' }}
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 搜索结果区域 -->
      <div id="search-results" v-if="hasResults || isLoading">
        <!-- 结果计数和视图切换 -->
        <div class="d-flex justify-content-between align-items-center mb-4" v-if="hasResults">
          <h3 class="h4 text-muted mb-0">找到 {{ totalResults }} 个结果</h3>
          <div class="btn-group">
            <button type="button" 
                    class="btn btn-outline-primary btn-sm" 
                    :class="{'active': viewMode === 'grid'}"
                    @click="toggleViewMode('grid')">
              <i class="fas fa-th-large"></i>
            </button>
            <button type="button" 
                    class="btn btn-outline-primary btn-sm" 
                    :class="{'active': viewMode === 'list'}"
                    @click="toggleViewMode('list')">
              <i class="fas fa-list"></i>
            </button>
          </div>
        </div>
        
        <!-- 加载中指示器 -->
        <div class="text-center my-5" v-if="isLoading && !hasResults">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">加载中...</span>
          </div>
          <p class="mt-2 text-muted">正在搜索，请稍候...</p>
        </div>
        
        <!-- 列表视图 -->
        <div v-if="viewMode === 'list' && hasResults" class="results-list">
          <div class="card shadow-sm hover-shadow-lg transition-all mb-3" 
               v-for="(result, index) in searchResults" 
               :key="result.id">
            <div class="card-body">
              <div class="row align-items-center">
                <!-- 封面图片 -->
                <div class="col-auto">
                  <img v-if="result.cover_url" 
                       :src="result.cover_url" 
                       alt="专辑封面" 
                       class="rounded-3" 
                       style="width: 80px; height: 80px; object-fit: cover;"
                       @click="goToMusicDetail(result.id)">
                  <div v-else 
                       class="bg-light rounded-3 d-flex align-items-center justify-content-center" 
                       style="width: 80px; height: 80px;"
                       @click="goToMusicDetail(result.id)">
                    <i class="fas fa-compact-disc fa-2x text-muted"></i>
                  </div>
                </div>
                
                <!-- 音乐信息 -->
                <div class="col">
                  <h5 class="card-title mb-1">
                    <a :href="'/music/' + result.id + '/'" class="text-decoration-none">
                      {{ result.title }}
                    </a>
                  </h5>
                  <p class="text-muted small mb-2">
                    <i class="fas fa-user me-1"></i>{{ result.artist }}
                    <span class="mx-2">|</span>
                    <i class="fas fa-compact-disc me-1"></i>{{ result.album }}
                    <span class="mx-2">|</span>
                    <i class="fas fa-calendar-alt me-1"></i>{{ result.release_date }}
                  </p>
                  
                  <!-- 播放控制 -->
                  <div class="d-flex align-items-center">
                    <button class="btn btn-sm btn-outline-primary me-2" 
                            @click="togglePreview(index)">
                      <i :class="['fas', getPlayButtonIcon(index)]"></i>
                    </button>
                    <div class="progress flex-grow-1" style="height: 5px;">
                      <div class="progress-bar bg-primary" role="progressbar" style="width: 0%"></div>
                    </div>
                    <audio :src="result.audio_url" 
                           class="preview-audio d-none" 
                           preload="none"
                           @ended="$event.target.currentTime = 0">
                    </audio>
                  </div>
                </div>
                
                <!-- 操作按钮 -->
                <div class="col-auto">
                  <a :href="'/music/' + result.id + '/'" class="btn btn-outline-primary btn-sm">
                    <i class="fas fa-info-circle me-1"></i>详情
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 网格视图 -->
        <div v-if="viewMode === 'grid' && hasResults" class="results-grid">
          <div class="row g-4">
            <div class="col-md-4 col-sm-6" v-for="(result, index) in searchResults" :key="result.id">
              <div class="card h-100 hover-shadow-lg transition-all">
                <!-- 封面图片 -->
                <div class="position-relative" style="padding-top: 100%;">
                  <img v-if="result.cover_url" 
                       :src="result.cover_url" 
                       class="position-absolute top-0 start-0 w-100 h-100 object-fit-cover"
                       alt="专辑封面">
                  <div v-else class="position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center bg-light">
                    <i class="fas fa-compact-disc fa-3x text-muted"></i>
                  </div>
                  <!-- 播放按钮 -->
                  <button class="btn btn-primary btn-sm position-absolute bottom-0 end-0 m-2"
                          @click="togglePreview(index)">
                    <i :class="['fas', getPlayButtonIcon(index)]"></i>
                  </button>
                </div>
                
                <div class="card-body">
                  <h5 class="card-title">
                    <a :href="'/music/' + result.id + '/'" class="text-decoration-none">
                      {{ result.title }}
                    </a>
                  </h5>
                  <p class="card-text text-muted">
                    {{ result.artist }} · {{ result.album }}
                  </p>
                  <audio :src="result.audio_url" 
                         class="preview-audio d-none" 
                         preload="none"
                         @ended="$event.target.currentTime = 0">
                  </audio>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 加载更多按钮 -->
        <div class="text-center mt-4">
          <button v-if="showLoadMore" 
                  class="btn btn-outline-primary"
                  @click="loadMore">
            <i class="fas fa-sync me-2"></i>加载更多
          </button>
          <div v-if="isLoading && hasResults" class="spinner-border text-primary" role="status">
            <span class="visually-hidden">加载中...</span>
          </div>
        </div>
      </div>
      
      <!-- 无结果提示 -->
      <div v-if="!hasResults && !isLoading && (effectiveQuery || hasAdvancedFilters())" class="text-center my-5">
        <div class="display-1 text-muted mb-3">
          <i class="fas fa-search"></i>
        </div>
        <h3 class="text-muted">未找到匹配的音乐</h3>
        <p class="text-muted">请尝试使用其他关键词或筛选条件</p>
      </div>
    </div>
  `
}; 