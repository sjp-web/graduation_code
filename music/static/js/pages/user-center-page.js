// 用户中心页面组件
// 页面级组件，负责协调用户中心页面的功能

import { createApp } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';

// 初始化页面
document.addEventListener('DOMContentLoaded', () => {
    console.log('用户中心页面初始化中...');
    
    // 初始化个人信息编辑功能
    initProfileEdit();
    
    // 初始化收藏管理功能
    initFavoritesManagement();
    
    // 初始化播放历史功能
    initPlayHistory();
    
    // 初始化账户设置功能
    initAccountSettings();
    
    console.log('用户中心页面初始化完成');
});

// 初始化个人信息编辑功能
function initProfileEdit() {
    const profileEditForm = document.getElementById('profile-edit-form');
    if (!profileEditForm) return;
    
    // 上传头像预览
    const avatarInput = document.getElementById('id_avatar');
    const avatarPreview = document.getElementById('avatar-preview');
    
    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    avatarPreview.src = e.target.result;
                    avatarPreview.style.display = 'block';
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
    
    // 表单验证
    profileEditForm.addEventListener('submit', function(e) {
        const nameInput = document.getElementById('id_display_name');
        if (nameInput && nameInput.value.trim() === '') {
            e.preventDefault();
            showFormError(nameInput, '显示名称不能为空');
            return false;
        }
        
        return true;
    });
}

// 初始化收藏管理功能
function initFavoritesManagement() {
    const favoriteButtons = document.querySelectorAll('.favorite-toggle');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const musicId = this.dataset.musicId;
            const isFavorite = this.dataset.isFavorite === 'true';
            
            // 发送请求更新收藏状态
            fetch(`/api/favorites/toggle/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    music_id: musicId,
                    is_favorite: !isFavorite
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 更新UI
                    this.dataset.isFavorite = (!isFavorite).toString();
                    this.querySelector('i').className = !isFavorite ? 
                        'fas fa-heart text-danger' : 'far fa-heart';
                    this.querySelector('span').textContent = !isFavorite ?
                        '取消收藏' : '收藏';
                        
                    // 显示提示信息
                    showToast(!isFavorite ? '已添加到收藏' : '已从收藏中移除');
                }
            })
            .catch(error => {
                console.error('收藏操作失败:', error);
                showToast('操作失败，请稍后重试', 'danger');
            });
        });
    });
}

// 初始化播放历史功能
function initPlayHistory() {
    const clearHistoryBtn = document.getElementById('clear-history-btn');
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', function() {
            if (confirm('确定要清空播放历史吗？此操作不可恢复。')) {
                fetch('/api/history/clear/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // 清空历史记录列表
                        const historyList = document.getElementById('play-history-list');
                        if (historyList) {
                            historyList.innerHTML = '<div class="text-center py-5 text-muted"><i class="fas fa-history fa-3x mb-3"></i><p>暂无播放历史</p></div>';
                        }
                        showToast('播放历史已清空');
                    }
                })
                .catch(error => {
                    console.error('清空历史失败:', error);
                    showToast('操作失败，请稍后重试', 'danger');
                });
            }
        });
    }
}

// 初始化账户设置功能
function initAccountSettings() {
    const passwordChangeForm = document.getElementById('password-change-form');
    if (passwordChangeForm) {
        passwordChangeForm.addEventListener('submit', function(e) {
            const newPassword = document.getElementById('id_new_password1').value;
            const confirmPassword = document.getElementById('id_new_password2').value;
            
            if (newPassword !== confirmPassword) {
                e.preventDefault();
                showFormError(document.getElementById('id_new_password2'), '两次输入的密码不一致');
                return false;
            }
            
            return true;
        });
    }
}

// 显示表单错误
function showFormError(inputElement, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    
    inputElement.classList.add('is-invalid');
    inputElement.parentNode.appendChild(errorDiv);
    
    // 清除之前的错误信息
    inputElement.addEventListener('input', function() {
        this.classList.remove('is-invalid');
        const feedback = this.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    });
}

// 显示提示信息
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        // 创建Toast容器
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
    }
    
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    document.getElementById('toast-container').appendChild(toast);
    
    // 使用Bootstrap的Toast API
    const toastInstance = new bootstrap.Toast(toast, {
        delay: 3000
    });
    toastInstance.show();
    
    // 自动移除DOM元素
    toast.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// 获取Cookie
function getCookie(name) {
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
}

// 导出页面初始化函数，便于外部调用
export function initUserCenterPage() {
    document.dispatchEvent(new Event('DOMContentLoaded'));
} 