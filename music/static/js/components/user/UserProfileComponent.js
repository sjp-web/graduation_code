// 用户信息组件
// 负责显示和编辑用户个人资料信息

import { ref, reactive, onMounted, computed } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';

export default {
  name: 'UserProfileComponent',
  
  props: {
    // 初始用户数据
    initialUserData: {
      type: Object,
      default: () => ({})
    },
    // 是否处于编辑模式
    isEditMode: {
      type: Boolean,
      default: false
    },
    // 是否是当前用户查看自己的资料
    isCurrentUser: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['profile-updated', 'cancel-edit'],
  
  setup(props, { emit }) {
    // 用户数据
    const userData = reactive({
      username: '',
      display_name: '',
      email: '',
      bio: '',
      avatar: '',
      date_joined: '',
      last_login: '',
      ...props.initialUserData
    });
    
    // 表单数据
    const formData = reactive({
      display_name: userData.display_name || '',
      email: userData.email || '',
      bio: userData.bio || '',
      avatar: null,
    });
    
    // 表单验证错误
    const formErrors = reactive({
      display_name: '',
      email: '',
      bio: '',
      avatar: '',
      general: ''
    });
    
    // 头像预览
    const avatarPreview = ref(userData.avatar || '');
    const isUploading = ref(false);
    const uploadProgress = ref(0);
    
    // 用户统计数据
    const stats = reactive({
      totalPlays: 0,
      favoritesCount: 0,
      commentsCount: 0,
      uploadsCount: 0
    });
    
    // 加载统计数据
    const loadUserStats = async () => {
      try {
        const response = await fetch(`/api/user/${userData.id}/stats/`);
        if (!response.ok) throw new Error('无法加载用户统计数据');
        
        const data = await response.json();
        stats.totalPlays = data.total_plays || 0;
        stats.favoritesCount = data.favorites_count || 0;
        stats.commentsCount = data.comments_count || 0;
        stats.uploadsCount = data.uploads_count || 0;
      } catch (error) {
        console.error('加载用户统计数据失败:', error);
      }
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知';
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    // 处理头像变更
    const handleAvatarChange = (event) => {
      const file = event.target.files[0];
      if (!file) return;
      
      // 验证文件类型
      const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
      if (!validTypes.includes(file.type)) {
        formErrors.avatar = '请上传 JPG、PNG 或 GIF 格式的图片';
        return;
      }
      
      // 验证文件大小
      if (file.size > 2 * 1024 * 1024) {
        formErrors.avatar = '图片大小不能超过 2MB';
        return;
      }
      
      // 清除错误
      formErrors.avatar = '';
      formData.avatar = file;
      
      // 创建预览
      const reader = new FileReader();
      reader.onload = (e) => {
        avatarPreview.value = e.target.result;
      };
      reader.readAsDataURL(file);
    };
    
    // 验证表单
    const validateForm = () => {
      let isValid = true;
      
      // 验证显示名称
      if (!formData.display_name.trim()) {
        formErrors.display_name = '显示名称不能为空';
        isValid = false;
      } else {
        formErrors.display_name = '';
      }
      
      // 验证电子邮件
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!formData.email.trim()) {
        formErrors.email = '电子邮件不能为空';
        isValid = false;
      } else if (!emailRegex.test(formData.email)) {
        formErrors.email = '请输入有效的电子邮件地址';
        isValid = false;
      } else {
        formErrors.email = '';
      }
      
      // 验证简介
      if (formData.bio && formData.bio.length > 500) {
        formErrors.bio = '简介不能超过 500 个字符';
        isValid = false;
      } else {
        formErrors.bio = '';
      }
      
      return isValid;
    };
    
    // 提交表单
    const submitForm = async () => {
      if (!validateForm()) return;
      
      try {
        isUploading.value = true;
        
        // 创建 FormData 对象
        const form = new FormData();
        form.append('display_name', formData.display_name);
        form.append('email', formData.email);
        form.append('bio', formData.bio);
        
        if (formData.avatar) {
          form.append('avatar', formData.avatar);
        }
        
        // 发送请求
        const response = await fetch('/api/user/profile/update/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: form
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || '更新个人资料失败');
        }
        
        const updatedData = await response.json();
        
        // 更新本地数据
        userData.display_name = updatedData.display_name;
        userData.email = updatedData.email;
        userData.bio = updatedData.bio;
        userData.avatar = updatedData.avatar;
        
        // 触发更新事件
        emit('profile-updated', updatedData);
        
      } catch (error) {
        console.error('更新个人资料失败:', error);
        formErrors.general = error.message || '更新个人资料失败，请稍后重试';
      } finally {
        isUploading.value = false;
      }
    };
    
    // 取消编辑
    const cancelEdit = () => {
      // 重置表单数据
      formData.display_name = userData.display_name;
      formData.email = userData.email;
      formData.bio = userData.bio;
      formData.avatar = null;
      
      // 重置预览
      avatarPreview.value = userData.avatar;
      
      // 清除错误
      Object.keys(formErrors).forEach(key => {
        formErrors[key] = '';
      });
      
      // 触发取消事件
      emit('cancel-edit');
    };
    
    // 获取 CSRF Token
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
    
    // 加载初始数据
    onMounted(() => {
      if (props.isCurrentUser) {
        loadUserStats();
      }
    });
    
    return {
      userData,
      formData,
      formErrors,
      avatarPreview,
      isUploading,
      uploadProgress,
      stats,
      formatDate,
      handleAvatarChange,
      submitForm,
      cancelEdit,
      isEditMode: computed(() => props.isEditMode),
      isCurrentUser: computed(() => props.isCurrentUser)
    };
  },
  
  template: `
    <div class="user-profile-component">
      <!-- 查看模式 -->
      <div v-if="!isEditMode" class="user-profile-view">
        <div class="row">
          <!-- 用户头像和基本信息 -->
          <div class="col-md-4 text-center">
            <div class="avatar-container mb-3">
              <img 
                :src="userData.avatar || '/static/images/default-avatar.png'" 
                :alt="userData.display_name || userData.username" 
                class="rounded-circle img-thumbnail avatar-lg"
              >
            </div>
            <h3 class="mb-1">{{ userData.display_name || userData.username }}</h3>
            <p class="text-muted mb-3">{{ userData.email }}</p>
            
            <div class="user-stats mb-4">
              <div class="row g-2">
                <div class="col-6 col-sm-3 col-md-6">
                  <div class="stat-item">
                    <div class="stat-value">{{ stats.totalPlays }}</div>
                    <div class="stat-label">播放次数</div>
                  </div>
                </div>
                <div class="col-6 col-sm-3 col-md-6">
                  <div class="stat-item">
                    <div class="stat-value">{{ stats.favoritesCount }}</div>
                    <div class="stat-label">收藏数量</div>
                  </div>
                </div>
                <div class="col-6 col-sm-3 col-md-6">
                  <div class="stat-item">
                    <div class="stat-value">{{ stats.commentsCount }}</div>
                    <div class="stat-label">评论数量</div>
                  </div>
                </div>
                <div class="col-6 col-sm-3 col-md-6">
                  <div class="stat-item">
                    <div class="stat-value">{{ stats.uploadsCount }}</div>
                    <div class="stat-label">上传数量</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="isCurrentUser" class="edit-button-container">
              <button @click="$emit('edit-profile')" class="btn btn-primary">
                <i class="fas fa-edit me-1"></i> 编辑资料
              </button>
            </div>
          </div>
          
          <!-- 用户详细信息 -->
          <div class="col-md-8">
            <div class="card">
              <div class="card-body">
                <h4 class="card-title mb-4">个人资料</h4>
                
                <div class="profile-info">
                  <div class="mb-3">
                    <h6 class="text-muted mb-1">用户名</h6>
                    <p>{{ userData.username }}</p>
                  </div>
                  
                  <div class="mb-3">
                    <h6 class="text-muted mb-1">注册时间</h6>
                    <p>{{ formatDate(userData.date_joined) }}</p>
                  </div>
                  
                  <div class="mb-3">
                    <h6 class="text-muted mb-1">上次登录</h6>
                    <p>{{ formatDate(userData.last_login) }}</p>
                  </div>
                  
                  <div class="mb-3">
                    <h6 class="text-muted mb-1">个人简介</h6>
                    <p v-if="userData.bio">{{ userData.bio }}</p>
                    <p v-else class="text-muted fst-italic">暂无简介</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 编辑模式 -->
      <div v-else class="user-profile-edit">
        <form @submit.prevent="submitForm" class="card">
          <div class="card-header">
            <h4 class="mb-0">编辑个人资料</h4>
          </div>
          
          <div class="card-body">
            <!-- 全局错误提示 -->
            <div v-if="formErrors.general" class="alert alert-danger">
              {{ formErrors.general }}
            </div>
            
            <div class="row">
              <!-- 头像上传 -->
              <div class="col-md-4 mb-4 text-center">
                <div class="avatar-upload mb-3">
                  <img 
                    :src="avatarPreview || '/static/images/default-avatar.png'" 
                    alt="头像预览" 
                    class="rounded-circle img-thumbnail avatar-lg mb-3"
                  >
                  
                  <div class="upload-controls">
                    <div class="mb-3">
                      <label for="avatar-input" class="form-label">更改头像</label>
                      <input 
                        type="file" 
                        id="avatar-input" 
                        class="form-control" 
                        accept="image/jpeg,image/png,image/gif"
                        @change="handleAvatarChange"
                      >
                      <div v-if="formErrors.avatar" class="text-danger mt-1">
                        {{ formErrors.avatar }}
                      </div>
                      <div class="form-text">
                        支持JPG、PNG和GIF格式，最大2MB
                      </div>
                    </div>
                    
                    <div v-if="isUploading" class="upload-progress">
                      <div class="progress">
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
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 表单字段 -->
              <div class="col-md-8">
                <!-- 显示名称 -->
                <div class="mb-3">
                  <label for="display-name" class="form-label">显示名称</label>
                  <input 
                    type="text" 
                    id="display-name" 
                    v-model="formData.display_name"
                    class="form-control"
                    :class="{ 'is-invalid': formErrors.display_name }"
                  >
                  <div v-if="formErrors.display_name" class="invalid-feedback">
                    {{ formErrors.display_name }}
                  </div>
                </div>
                
                <!-- 电子邮件 -->
                <div class="mb-3">
                  <label for="email" class="form-label">电子邮件</label>
                  <input 
                    type="email" 
                    id="email" 
                    v-model="formData.email"
                    class="form-control"
                    :class="{ 'is-invalid': formErrors.email }"
                  >
                  <div v-if="formErrors.email" class="invalid-feedback">
                    {{ formErrors.email }}
                  </div>
                </div>
                
                <!-- 个人简介 -->
                <div class="mb-3">
                  <label for="bio" class="form-label">个人简介</label>
                  <textarea 
                    id="bio" 
                    v-model="formData.bio"
                    class="form-control"
                    :class="{ 'is-invalid': formErrors.bio }"
                    rows="4"
                  ></textarea>
                  <div v-if="formErrors.bio" class="invalid-feedback">
                    {{ formErrors.bio }}
                  </div>
                  <div class="form-text">
                    最多500个字符，当前已输入 {{ formData.bio.length }} 个字符
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card-footer d-flex justify-content-end gap-2">
            <button type="button" class="btn btn-secondary" @click="cancelEdit">
              取消
            </button>
            <button type="submit" class="btn btn-primary" :disabled="isUploading">
              <span v-if="isUploading">
                <span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                保存中...
              </span>
              <span v-else>
                <i class="fas fa-save me-1"></i> 保存更改
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  `
}; 