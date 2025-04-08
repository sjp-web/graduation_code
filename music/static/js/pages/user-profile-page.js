// 用户个人资料页面组件
// 页面级组件，负责协调用户个人资料页面功能

import { createApp } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';
import UserProfileComponent from '../components/user/UserProfileComponent.js';

// 初始化页面
document.addEventListener('DOMContentLoaded', () => {
    console.log('用户资料页面初始化中...');
    
    // 获取挂载点
    const mountPoint = document.getElementById('user-profile-app');
    if (!mountPoint) {
        console.error('未找到用户资料组件挂载点');
        return;
    }
    
    try {
        // 获取初始用户数据
        const userDataElement = document.getElementById('user-profile-data');
        let userData = {};
        
        if (userDataElement && userDataElement.textContent) {
            try {
                userData = JSON.parse(userDataElement.textContent);
                console.log('成功加载用户数据');
            } catch (error) {
                console.error('解析用户数据失败:', error);
            }
        }
        
        // 获取是否为当前用户
        const isCurrentUser = mountPoint.dataset.isCurrentUser === 'true';
        
        // 创建Vue应用
        const app = createApp({
            components: {
                UserProfileComponent
            },
            data() {
                return {
                    userData,
                    isEditMode: false,
                    isCurrentUser
                };
            },
            methods: {
                // 进入编辑模式
                enterEditMode() {
                    this.isEditMode = true;
                },
                
                // 取消编辑
                cancelEdit() {
                    this.isEditMode = false;
                },
                
                // 处理资料更新
                handleProfileUpdated(updatedData) {
                    this.userData = { ...this.userData, ...updatedData };
                    this.isEditMode = false;
                    
                    // 显示成功消息
                    this.showToast('个人资料更新成功');
                },
                
                // 显示提示消息
                showToast(message, type = 'success') {
                    if (window.bootstrap && window.bootstrap.Toast) {
                        // 创建Toast容器（如果不存在）
                        let toastContainer = document.getElementById('toast-container');
                        if (!toastContainer) {
                            toastContainer = document.createElement('div');
                            toastContainer.id = 'toast-container';
                            toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
                            toastContainer.style.zIndex = '1050';
                            document.body.appendChild(toastContainer);
                        }
                        
                        // 创建Toast元素
                        const toastEl = document.createElement('div');
                        toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
                        toastEl.setAttribute('role', 'alert');
                        toastEl.setAttribute('aria-live', 'assertive');
                        toastEl.setAttribute('aria-atomic', 'true');
                        
                        toastEl.innerHTML = `
                            <div class="d-flex">
                                <div class="toast-body">
                                    ${message}
                                </div>
                                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                        `;
                        
                        toastContainer.appendChild(toastEl);
                        
                        // 显示Toast
                        const toast = new window.bootstrap.Toast(toastEl, {
                            delay: 3000
                        });
                        toast.show();
                        
                        // 自动移除DOM元素
                        toastEl.addEventListener('hidden.bs.toast', function() {
                            this.remove();
                        });
                    }
                }
            },
            template: `
                <div class="user-profile-page">
                    <user-profile-component
                        :initial-user-data="userData"
                        :is-edit-mode="isEditMode"
                        :is-current-user="isCurrentUser"
                        @edit-profile="enterEditMode"
                        @cancel-edit="cancelEdit"
                        @profile-updated="handleProfileUpdated"
                    ></user-profile-component>
                </div>
            `
        });
        
        // 挂载应用
        app.mount(mountPoint);
        console.log('用户资料页面组件挂载成功');
        
    } catch (error) {
        console.error('用户资料页面初始化失败:', error);
    }
});

// 导出页面初始化函数，便于外部调用
export function initUserProfilePage() {
    console.log('手动初始化用户资料页面');
    document.dispatchEvent(new Event('DOMContentLoaded'));
} 