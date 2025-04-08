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
      playingIndex: -1 // 当前正在播放的音频索引
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
      // 处理"歌曲名 - 艺术家"格式
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
      this.totalPages = 0;
    },
    
    // 处理点击建议框外部的事件
    handleOutsideClick(event) {
      const component = this.$el;
      if (component && !component.contains(event.target)) {
        this.showSuggestions = false;
      }
    },
    
    // 处理键盘导航
    handleKeyDown(event) {
      if (!this.showSuggestions || this.suggestions.length === 0) return;
      
      // 向下箭头
      if (event.key === 'ArrowDown') {
        event.preventDefault();
        this.selectedResult = Math.min(this.selectedResult + 1, this.suggestions.length - 1);
        this.scrollToSelectedSuggestion();
      }
      
      // 向上箭头
      else if (event.key === 'ArrowUp') {
        event.preventDefault();
        this.selectedResult = Math.max(this.selectedResult - 1, -1);
        this.scrollToSelectedSuggestion();
      }
      
      // 回车键
      else if (event.key === 'Enter') {
        if (this.selectedResult >= 0) {
          event.preventDefault();
          this.selectSuggestion(this.suggestions[this.selectedResult]);
        } else if (this.effectiveQuery) {
          this.showSuggestions = false;
          this.search();
        }
      }
      
      // ESC键
      else if (event.key === 'Escape') {
        this.showSuggestions = false;
      }
    },
    
    // 滚动到选中的建议
    scrollToSelectedSuggestion() {
      this.$nextTick(() => {
        const selectedElement = document.querySelector('.search-suggestions .active');
        if (selectedElement) {
          selectedElement.scrollIntoView({ block: 'nearest' });
        }
      });
    },
    
    // 跳转到音乐详情页
    goToMusicDetail(id) {
      window.location.href = `/music/detail/${id}/`;
    },
    
    // 切换预览播放
    togglePreview(index) {
      // 如果点击当前播放项，则停止播放
      if (this.playingIndex === index) {
        this.stopPreview();
        return;
      }
      
      // 停止当前播放
      this.stopPreview();
      
      // 设置新的播放索引
      this.playingIndex = index;
      
      // 获取音频元素
      const audio = this.$refs[`audio_${index}`][0];
      if (!audio) return;
      
      // 播放
      audio.play().catch(err => {
        console.error('预览播放失败:', err);
        this.playingIndex = -1;
      });
      
      // 监听播放结束事件
      audio.onended = () => {
        this.playingIndex = -1;
      };
    },
    
    // 停止预览播放
    stopPreview() {
      if (this.playingIndex >= 0) {
        const audio = this.$refs[`audio_${this.playingIndex}`][0];
        if (audio) {
          audio.pause();
          audio.currentTime = 0;
        }
        this.playingIndex = -1;
      }
    },
    
    // 获取播放按钮图标
    getPlayButtonIcon(index) {
      return this.playingIndex === index ? 'fa-pause' : 'fa-play';
    }
  }
}; 