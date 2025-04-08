// 音乐上传组件
// 负责音乐文件上传和元数据编辑功能

import { ref, reactive, computed, onMounted } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';

export default {
  name: 'UploadComponent',
  
  props: {
    // 已有的分类选项
    categories: {
      type: Array,
      default: () => []
    },
    // 最大文件大小 (MB)
    maxFileSize: {
      type: Number,
      default: 20
    },
    // 允许的文件类型
    allowedFileTypes: {
      type: Array,
      default: () => ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/flac']
    }
  },
  
  emits: ['upload-success', 'upload-error'],
  
  setup(props, { emit }) {
    // 上传表单数据
    const form = reactive({
      title: '',
      artist: '',
      album: '',
      release_date: '',
      category: '',
      description: '',
      audio_file: null,
      cover_image: null,
      lyrics: '',
      is_public: true
    });
    
    // 表单验证错误
    const errors = reactive({
      title: '',
      artist: '',
      album: '',
      release_date: '',
      category: '',
      description: '',
      audio_file: '',
      cover_image: '',
      lyrics: '',
      general: ''
    });
    
    // 文件预览
    const audioFileName = ref('');
    const audioFileSize = ref('');
    const audioDuration = ref('');
    const audioPreviewUrl = ref('');
    const coverPreviewUrl = ref('');
    
    // 上传状态
    const isUploading = ref(false);
    const uploadProgress = ref(0);
    const isProcessing = ref(false);
    const uploadSuccess = ref(false);
    const uploadedMusicId = ref(null);
    
    // 拖放区域状态
    const isDragging = ref(false);
    
    // 今天的日期（用于日期选择器的最大值）
    const today = new Date().toISOString().split('T')[0];
    
    // 计算属性：表单是否有效
    const isFormValid = computed(() => {
      return (
        form.title.trim() !== '' &&
        form.artist.trim() !== '' &&
        form.category !== '' &&
        form.audio_file !== null &&
        !hasErrors.value
      );
    });
    
    // 计算属性：是否有错误
    const hasErrors = computed(() => {
      return Object.values(errors).some(error => error !== '');
    });
    
    // 重置表单
    const resetForm = () => {
      // 重置表单字段
      Object.keys(form).forEach(key => {
        if (key === 'is_public') {
          form[key] = true;
        } else {
          form[key] = '';
        }
      });
      
      form.audio_file = null;
      form.cover_image = null;
      
      // 重置错误
      Object.keys(errors).forEach(key => {
        errors[key] = '';
      });
      
      // 重置预览
      audioFileName.value = '';
      audioFileSize.value = '';
      audioDuration.value = '';
      audioPreviewUrl.value = '';
      coverPreviewUrl.value = '';
      
      // 重置上传状态
      uploadProgress.value = 0;
      uploadSuccess.value = false;
      uploadedMusicId.value = null;
    };
    
    // 处理音频文件选择
    const handleAudioFileChange = (event) => {
      const file = event.target.files[0];
      validateAndSetAudioFile(file);
    };
    
    // 验证并设置音频文件
    const validateAndSetAudioFile = (file) => {
      if (!file) return;
      
      // 清除之前的错误
      errors.audio_file = '';
      
      // 验证文件类型
      if (!props.allowedFileTypes.includes(file.type)) {
        errors.audio_file = `请上传支持的音频格式: ${props.allowedFileTypes.map(type => type.split('/')[1].toUpperCase()).join(', ')}`;
        return;
      }
      
      // 验证文件大小
      const maxSize = props.maxFileSize * 1024 * 1024; // 转换为字节
      if (file.size > maxSize) {
        errors.audio_file = `文件大小不能超过 ${props.maxFileSize}MB`;
        return;
      }
      
      // 设置文件信息
      form.audio_file = file;
      audioFileName.value = file.name;
      audioFileSize.value = formatFileSize(file.size);
      
      // 获取音频时长
      const audio = new Audio();
      audio.addEventListener('loadedmetadata', () => {
        audioDuration.value = formatDuration(audio.duration);
      });
      audio.src = URL.createObjectURL(file);
      
      // 创建音频预览URL
      audioPreviewUrl.value = URL.createObjectURL(file);
      
      // 如果还没有设置标题和艺术家，尝试从文件名中提取
      if (!form.title || !form.artist) {
        const nameWithoutExt = file.name.replace(/\.[^/.]+$/, '');
        const parts = nameWithoutExt.split(' - ');
        if (parts.length > 1) {
          // 可能的格式: 艺术家 - 标题
          if (!form.artist) form.artist = parts[0].trim();
          if (!form.title) form.title = parts[1].trim();
        } else {
          // 只使用文件名作为标题
          if (!form.title) form.title = nameWithoutExt.trim();
        }
      }
    };
    
    // 处理封面图片选择
    const handleCoverImageChange = (event) => {
      const file = event.target.files[0];
      validateAndSetCoverImage(file);
    };
    
    // 验证并设置封面图片
    const validateAndSetCoverImage = (file) => {
      if (!file) return;
      
      // 清除之前的错误
      errors.cover_image = '';
      
      // 验证文件类型
      const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
      if (!validImageTypes.includes(file.type)) {
        errors.cover_image = '请上传 JPG、PNG 或 GIF 格式的图片';
        return;
      }
      
      // 验证文件大小
      if (file.size > 5 * 1024 * 1024) {
        errors.cover_image = '图片大小不能超过 5MB';
        return;
      }
      
      // 设置封面图片
      form.cover_image = file;
      
      // 创建图片预览
      coverPreviewUrl.value = URL.createObjectURL(file);
    };
    
    // 处理拖放区域事件
    const handleDragOver = (event) => {
      event.preventDefault();
      isDragging.value = true;
    };
    
    const handleDragLeave = () => {
      isDragging.value = false;
    };
    
    const handleDrop = (event) => {
      event.preventDefault();
      isDragging.value = false;
      
      const files = event.dataTransfer.files;
      if (files.length === 0) return;
      
      // 处理音频文件
      const audioFiles = Array.from(files).filter(file => 
        props.allowedFileTypes.includes(file.type)
      );
      
      if (audioFiles.length > 0) {
        validateAndSetAudioFile(audioFiles[0]);
      }
      
      // 处理图片文件
      const imageFiles = Array.from(files).filter(file => 
        ['image/jpeg', 'image/png', 'image/gif'].includes(file.type)
      );
      
      if (imageFiles.length > 0) {
        validateAndSetCoverImage(imageFiles[0]);
      }
    };
    
    // 验证表单
    const validateForm = () => {
      let isValid = true;
      
      // 验证标题
      if (!form.title.trim()) {
        errors.title = '标题不能为空';
        isValid = false;
      } else if (form.title.length > 100) {
        errors.title = '标题不能超过100个字符';
        isValid = false;
      } else {
        errors.title = '';
      }
      
      // 验证艺术家
      if (!form.artist.trim()) {
        errors.artist = '艺术家不能为空';
        isValid = false;
      } else if (form.artist.length > 100) {
        errors.artist = '艺术家名称不能超过100个字符';
        isValid = false;
      } else {
        errors.artist = '';
      }
      
      // 验证分类
      if (!form.category) {
        errors.category = '请选择一个分类';
        isValid = false;
      } else {
        errors.category = '';
      }
      
      // 验证音频文件
      if (!form.audio_file) {
        errors.audio_file = '请上传音频文件';
        isValid = false;
      }
      
      // 验证描述
      if (form.description && form.description.length > 1000) {
        errors.description = '描述不能超过1000个字符';
        isValid = false;
      } else {
        errors.description = '';
      }
      
      // 验证歌词
      if (form.lyrics && form.lyrics.length > 5000) {
        errors.lyrics = '歌词不能超过5000个字符';
        isValid = false;
      } else {
        errors.lyrics = '';
      }
      
      return isValid;
    };
    
    // 提交表单
    const submitForm = async () => {
      // 验证表单
      if (!validateForm()) {
        // 滚动到第一个错误
        const firstError = Object.keys(errors).find(key => errors[key] !== '');
        if (firstError) {
          const errorElement = document.getElementById(`${firstError}-input`);
          if (errorElement) {
            errorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }
        return;
      }
      
      // 开始上传
      isUploading.value = true;
      uploadProgress.value = 0;
      
      try {
        // 创建FormData对象
        const formData = new FormData();
        
        // 添加所有字段
        Object.keys(form).forEach(key => {
          if (form[key] !== null && form[key] !== undefined) {
            // 特殊处理布尔值
            if (typeof form[key] === 'boolean') {
              formData.append(key, form[key] ? 'true' : 'false');
            } else {
              formData.append(key, form[key]);
            }
          }
        });
        
        // 使用XMLHttpRequest来获取上传进度
        const xhr = new XMLHttpRequest();
        
        // 设置进度监听器
        xhr.upload.addEventListener('progress', (event) => {
          if (event.lengthComputable) {
            uploadProgress.value = Math.round((event.loaded / event.total) * 100);
          }
        });
        
        // 创建Promise以使用async/await
        const uploadPromise = new Promise((resolve, reject) => {
          xhr.open('POST', '/api/music/upload/');
          
          // 设置CSRF Token
          const csrfToken = getCookie('csrftoken');
          if (csrfToken) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
          }
          
          xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
              resolve(JSON.parse(xhr.response));
            } else {
              try {
                reject(JSON.parse(xhr.response));
              } catch (e) {
                reject({ error: '上传过程中发生错误' });
              }
            }
          };
          
          xhr.onerror = () => {
            reject({ error: '网络错误，请稍后重试' });
          };
          
          xhr.send(formData);
        });
        
        // 文件上传完成，等待服务器处理
        uploadProgress.value = 100;
        isProcessing.value = true;
        
        // 等待服务器响应
        const response = await uploadPromise;
        
        // 处理成功响应
        isProcessing.value = false;
        uploadSuccess.value = true;
        uploadedMusicId.value = response.id;
        
        // 触发成功事件
        emit('upload-success', response);
        
      } catch (error) {
        // 处理错误
        isProcessing.value = false;
        
        if (error.errors) {
          // 处理字段错误
          Object.keys(error.errors).forEach(key => {
            if (errors[key] !== undefined) {
              errors[key] = error.errors[key];
            }
          });
        }
        
        // 设置通用错误
        errors.general = error.error || '上传失败，请稍后重试';
        
        // 触发错误事件
        emit('upload-error', error);
      } finally {
        isUploading.value = false;
      }
    };
    
    // 播放音频预览
    const playAudioPreview = () => {
      if (audioPreviewUrl.value) {
        const audioElement = new Audio(audioPreviewUrl.value);
        audioElement.play();
      }
    };
    
    // 创建新上传
    const startNewUpload = () => {
      resetForm();
    };
    
    // 跳转到音乐详情页
    const viewUploadedMusic = () => {
      if (uploadedMusicId.value) {
        window.location.href = `/music/${uploadedMusicId.value}/`;
      }
    };
    
    // 获取CSRF Token
    const getCookie = (name) => {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    };
    
    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes';
      
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    // 格式化音频时长
    const formatDuration = (seconds) => {
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    };
    
    // 清除字段错误
    const clearFieldError = (field) => {
      errors[field] = '';
    };
    
    // 页面加载完成后执行
    onMounted(() => {
      // 初始化操作（如果需要）
    });
    
    return {
      form,
      errors,
      audioFileName,
      audioFileSize,
      audioDuration,
      audioPreviewUrl,
      coverPreviewUrl,
      isUploading,
      uploadProgress,
      isProcessing,
      uploadSuccess,
      uploadedMusicId,
      isDragging,
      today,
      isFormValid,
      hasErrors,
      categories: computed(() => props.categories),
      handleAudioFileChange,
      handleCoverImageChange,
      handleDragOver,
      handleDragLeave,
      handleDrop,
      submitForm,
      playAudioPreview,
      startNewUpload,
      viewUploadedMusic,
      clearFieldError
    };
  },
  
  template: `
    <div class="upload-component">
      <!-- 上传成功提示 -->
      <div v-if="uploadSuccess" class="upload-success card mb-4">
        <div class="card-body text-center">
          <div class="success-icon mb-3">
            <i class="fas fa-check-circle text-success fa-5x"></i>
          </div>
          <h3 class="mb-3">上传成功！</h3>
          <p class="mb-4">您的音乐已成功上传并处理完成。您可以查看音乐详情或继续上传新的音乐。</p>
          <div class="d-flex justify-content-center gap-3">
            <button @click="viewUploadedMusic" class="btn btn-primary">
              <i class="fas fa-play me-1"></i> 查看音乐
            </button>
            <button @click="startNewUpload" class="btn btn-outline-secondary">
              <i class="fas fa-plus me-1"></i> 新建上传
            </button>
          </div>
        </div>
      </div>
      
      <!-- 上传表单 -->
      <div v-else class="upload-form">
        <form @submit.prevent="submitForm">
          <!-- 全局错误提示 -->
          <div v-if="errors.general" class="alert alert-danger mb-4">
            <i class="fas fa-exclamation-circle me-2"></i> {{ errors.general }}
          </div>
          
          <!-- 拖放上传区域 -->
          <div 
            class="drop-zone mb-4 p-5 text-center" 
            :class="{ 'dragging': isDragging, 'has-audio': form.audio_file }"
            @dragover="handleDragOver"
            @dragleave="handleDragLeave"
            @drop="handleDrop"
          >
            <div v-if="!form.audio_file" class="upload-placeholder">
              <div class="upload-icon mb-3">
                <i class="fas fa-cloud-upload-alt fa-3x text-primary"></i>
              </div>
              <h4 class="mb-2">拖放音频文件到这里</h4>
              <p class="text-muted mb-3">或者点击下方按钮选择文件</p>
              <div class="mb-3">
                <label for="audio-file-input" class="btn btn-primary">
                  <i class="fas fa-music me-1"></i> 选择音频文件
                </label>
                <input 
                  type="file" 
                  id="audio-file-input" 
                  class="visually-hidden"
                  accept="audio/*" 
                  @change="handleAudioFileChange"
                  :disabled="isUploading"
                  ref="audioFileInput"
                >
              </div>
              <div class="text-muted small">
                支持的格式: MP3, WAV, OGG, FLAC&nbsp;&nbsp;|&nbsp;&nbsp;最大文件大小: {{ maxFileSize }}MB
              </div>
            </div>
            
            <div v-else class="audio-preview">
              <div class="d-flex align-items-center mb-3">
                <div class="audio-icon me-3">
                  <i class="fas fa-music fa-2x text-primary"></i>
                </div>
                <div class="audio-info flex-grow-1 text-start">
                  <h5 class="mb-1">{{ audioFileName }}</h5>
                  <div class="d-flex text-muted small">
                    <span>{{ audioFileSize }}</span>
                    <span class="mx-2">|</span>
                    <span v-if="audioDuration">{{ audioDuration }}</span>
                    <span v-else><i class="fas fa-spinner fa-spin me-1"></i> 获取时长...</span>
                  </div>
                </div>
                <div class="audio-actions">
                  <button type="button" class="btn btn-sm btn-primary me-2" @click="playAudioPreview">
                    <i class="fas fa-play"></i>
                  </button>
                  <label class="btn btn-sm btn-outline-secondary">
                    <i class="fas fa-exchange-alt me-1"></i> 更换
                    <input 
                      type="file" 
                      class="visually-hidden"
                      accept="audio/*" 
                      @change="handleAudioFileChange"
                      :disabled="isUploading"
                    >
                  </label>
                </div>
              </div>
              <div v-if="errors.audio_file" class="text-danger">
                <i class="fas fa-exclamation-circle me-1"></i> {{ errors.audio_file }}
              </div>
            </div>
          </div>
          
          <div class="row">
            <!-- 左列：基本信息 -->
            <div class="col-md-8">
              <div class="card mb-4">
                <div class="card-header">
                  <h5 class="mb-0">音乐信息</h5>
                </div>
                <div class="card-body">
                  <!-- 标题 -->
                  <div class="mb-3">
                    <label for="title-input" class="form-label">标题 <span class="text-danger">*</span></label>
                    <input 
                      type="text" 
                      id="title-input" 
                      v-model="form.title"
                      class="form-control" 
                      :class="{ 'is-invalid': errors.title }"
                      placeholder="输入音乐标题" 
                      @input="clearFieldError('title')"
                      :disabled="isUploading"
                      maxlength="100"
                    >
                    <div v-if="errors.title" class="invalid-feedback">
                      {{ errors.title }}
                    </div>
                  </div>
                  
                  <!-- 艺术家 -->
                  <div class="mb-3">
                    <label for="artist-input" class="form-label">艺术家 <span class="text-danger">*</span></label>
                    <input 
                      type="text" 
                      id="artist-input" 
                      v-model="form.artist"
                      class="form-control" 
                      :class="{ 'is-invalid': errors.artist }"
                      placeholder="输入艺术家名称" 
                      @input="clearFieldError('artist')"
                      :disabled="isUploading"
                      maxlength="100"
                    >
                    <div v-if="errors.artist" class="invalid-feedback">
                      {{ errors.artist }}
                    </div>
                  </div>
                  
                  <!-- 专辑 -->
                  <div class="mb-3">
                    <label for="album-input" class="form-label">专辑</label>
                    <input 
                      type="text" 
                      id="album-input" 
                      v-model="form.album"
                      class="form-control" 
                      :class="{ 'is-invalid': errors.album }"
                      placeholder="输入专辑名称（可选）" 
                      @input="clearFieldError('album')"
                      :disabled="isUploading"
                      maxlength="100"
                    >
                    <div v-if="errors.album" class="invalid-feedback">
                      {{ errors.album }}
                    </div>
                  </div>
                  
                  <div class="row">
                    <!-- 分类 -->
                    <div class="col-md-6 mb-3">
                      <label for="category-input" class="form-label">分类 <span class="text-danger">*</span></label>
                      <select 
                        id="category-input" 
                        v-model="form.category"
                        class="form-select" 
                        :class="{ 'is-invalid': errors.category }"
                        @change="clearFieldError('category')"
                        :disabled="isUploading"
                      >
                        <option value="">选择音乐分类</option>
                        <option value="pop">流行</option>
                        <option value="rock">摇滚</option>
                        <option value="classical">古典</option>
                      </select>
                      <div v-if="errors.category" class="invalid-feedback">
                        {{ errors.category }}
                      </div>
                    </div>
                    
                    <!-- 发行日期 -->
                    <div class="col-md-6 mb-3">
                      <label for="release-date-input" class="form-label">发行日期</label>
                      <input 
                        type="date" 
                        id="release-date-input" 
                        v-model="form.release_date"
                        class="form-control" 
                        :class="{ 'is-invalid': errors.release_date }"
                        :max="today"
                        @input="clearFieldError('release_date')"
                        :disabled="isUploading"
                      >
                      <div v-if="errors.release_date" class="invalid-feedback">
                        {{ errors.release_date }}
                      </div>
                    </div>
                  </div>
                  
                  <!-- 描述 -->
                  <div class="mb-3">
                    <label for="description-input" class="form-label">描述</label>
                    <textarea 
                      id="description-input" 
                      v-model="form.description"
                      class="form-control" 
                      :class="{ 'is-invalid': errors.description }"
                      rows="3" 
                      placeholder="添加关于这首音乐的描述（可选）" 
                      @input="clearFieldError('description')"
                      :disabled="isUploading"
                      maxlength="1000"
                    ></textarea>
                    <div v-if="errors.description" class="invalid-feedback">
                      {{ errors.description }}
                    </div>
                    <div class="form-text" :class="{ 'text-danger': form.description.length > 1000 }">
                      {{ form.description.length }}/1000 字符
                    </div>
                  </div>
                  
                  <!-- 歌词 -->
                  <div class="mb-3">
                    <label for="lyrics-input" class="form-label">歌词</label>
                    <textarea 
                      id="lyrics-input" 
                      v-model="form.lyrics"
                      class="form-control" 
                      :class="{ 'is-invalid': errors.lyrics }"
                      rows="5" 
                      placeholder="添加歌词（可选）" 
                      @input="clearFieldError('lyrics')"
                      :disabled="isUploading"
                      maxlength="5000"
                    ></textarea>
                    <div v-if="errors.lyrics" class="invalid-feedback">
                      {{ errors.lyrics }}
                    </div>
                    <div class="form-text" :class="{ 'text-danger': form.lyrics.length > 5000 }">
                      {{ form.lyrics.length }}/5000 字符
                    </div>
                  </div>
                  
                  <!-- 可见性选项 -->
                  <div class="mb-3">
                    <div class="form-check">
                      <input 
                        type="checkbox" 
                        id="is-public-input" 
                        v-model="form.is_public"
                        class="form-check-input" 
                        :disabled="isUploading"
                      >
                      <label class="form-check-label" for="is-public-input">
                        公开此音乐（所有人都可以看到并收听）
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 右列：封面图片 -->
            <div class="col-md-4">
              <div class="card mb-4">
                <div class="card-header">
                  <h5 class="mb-0">封面图片</h5>
                </div>
                <div class="card-body">
                  <div class="cover-image-upload text-center">
                    <!-- 封面图片预览 -->
                    <div class="cover-preview mb-3">
                      <img 
                        v-if="coverPreviewUrl" 
                        :src="coverPreviewUrl" 
                        alt="封面预览" 
                        class="img-fluid img-thumbnail"
                        style="max-height: 200px;"
                      >
                      <div v-else class="placeholder-image">
                        <i class="fas fa-image fa-5x text-muted"></i>
                      </div>
                    </div>
                    
                    <!-- 封面图片上传控件 -->
                    <div class="mb-3">
                      <label for="cover-image-input" class="btn btn-outline-primary">
                        <i class="fas fa-image me-1"></i> {{ coverPreviewUrl ? '更换封面图片' : '上传封面图片' }}
                      </label>
                      <input 
                        type="file" 
                        id="cover-image-input" 
                        class="visually-hidden"
                        accept="image/jpeg,image/png,image/gif" 
                        @change="handleCoverImageChange"
                        :disabled="isUploading"
                      >
                    </div>
                    
                    <!-- 错误提示 -->
                    <div v-if="errors.cover_image" class="text-danger">
                      <i class="fas fa-exclamation-circle me-1"></i> {{ errors.cover_image }}
                    </div>
                    
                    <!-- 帮助文本 -->
                    <div class="form-text">
                      推荐尺寸: 500x500 像素<br>
                      支持的格式: JPG, PNG, GIF<br>
                      最大文件大小: 5MB
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 上传按钮 -->
          <div class="text-center mb-4">
            <button 
              type="submit"
              class="btn btn-primary btn-lg"
              :disabled="isUploading || isProcessing || !isFormValid"
            >
              <span v-if="isUploading || isProcessing">
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                {{ isProcessing ? '处理中...' : '上传中...' }}
              </span>
              <span v-else>
                <i class="fas fa-cloud-upload-alt me-2"></i> 上传音乐
              </span>
            </button>
          </div>
          
          <!-- 上传进度 -->
          <div v-if="isUploading || isProcessing" class="upload-progress mb-4">
            <h5 class="mb-2">{{ isProcessing ? '服务器处理中...' : '上传进度' }}</h5>
            <div class="progress mb-2">
              <div 
                class="progress-bar" 
                role="progressbar" 
                :style="{ width: uploadProgress + '%' }" 
                :aria-valuenow="uploadProgress" 
                aria-valuemin="0" 
                aria-valuemax="100"
              >
                {{ uploadProgress }}%
              </div>
            </div>
            <p class="text-muted small">
              {{ isProcessing ? '请耐心等待，服务器正在处理您的音乐文件...' : '正在上传文件，请不要关闭页面...' }}
            </p>
          </div>
        </form>
      </div>
    </div>
  `
}; 