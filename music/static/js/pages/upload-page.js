// 音乐上传页面组件
// 页面级组件，负责协调音乐上传页面功能

import { createApp } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';
import UploadComponent from '../components/upload/UploadComponent.js';

// 初始化页面
document.addEventListener('DOMContentLoaded', () => {
    console.log('音乐上传页面初始化中...');
    
    // 获取挂载点
    const mountPoint = document.getElementById('upload-app');
    if (!mountPoint) {
        console.error('未找到上传组件挂载点');
        return;
    }
    
    try {
        // 获取分类数据
        const categoriesElement = document.getElementById('categories-data');
        let categories = [];
        
        if (categoriesElement && categoriesElement.textContent) {
            try {
                categories = JSON.parse(categoriesElement.textContent);
                console.log('成功加载分类数据:', categories);
            } catch (error) {
                console.error('解析分类数据失败:', error);
            }
        }
        
        // 获取上传配置
        const configElement = document.getElementById('upload-config');
        let uploadConfig = {
            maxFileSize: 20, // 默认最大文件大小 (MB)
            allowedFileTypes: ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/flac'] // 默认允许的文件类型
        };
        
        if (configElement && configElement.textContent) {
            try {
                const config = JSON.parse(configElement.textContent);
                if (config.maxFileSize) uploadConfig.maxFileSize = config.maxFileSize;
                if (config.allowedFileTypes) uploadConfig.allowedFileTypes = config.allowedFileTypes;
                console.log('成功加载上传配置:', uploadConfig);
            } catch (error) {
                console.error('解析上传配置失败:', error);
            }
        }
        
        // 创建Vue应用
        const app = createApp({
            components: {
                UploadComponent
            },
            data() {
                return {
                    categories,
                    maxFileSize: uploadConfig.maxFileSize,
                    allowedFileTypes: uploadConfig.allowedFileTypes
                };
            },
            methods: {
                // 处理上传成功
                handleUploadSuccess(response) {
                    console.log('上传成功:', response);
                    
                    // 显示成功消息（如果需要）
                    this.showToast('音乐上传成功！');
                },
                
                // 处理上传错误
                handleUploadError(error) {
                    console.error('上传失败:', error);
                    
                    // 显示错误消息（如果需要）
                    this.showToast('上传失败: ' + (error.error || '未知错误'), 'danger');
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
                <div class="upload-page">
                    <div class="upload-header mb-4">
                        <h2 class="mb-3">上传音乐</h2>
                        <p class="text-muted">分享您的音乐作品，让更多人发现您的才华。</p>
                    </div>
                    
                    <upload-component
                        :categories="categories"
                        :max-file-size="maxFileSize"
                        :allowed-file-types="allowedFileTypes"
                        @upload-success="handleUploadSuccess"
                        @upload-error="handleUploadError"
                    ></upload-component>
                </div>
            `
        });
        
        // 挂载应用
        app.mount(mountPoint);
        console.log('音乐上传页面组件挂载成功');
        
    } catch (error) {
        console.error('音乐上传页面初始化失败:', error);
    }
});

// 导出页面初始化函数，便于外部调用
export function initUploadPage() {
    console.log('手动初始化音乐上传页面');
    document.dispatchEvent(new Event('DOMContentLoaded'));
} 