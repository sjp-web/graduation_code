/**
 * 音乐平台主要JavaScript文件
 */

// DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    initializeTooltips();
    
    // 初始化下拉菜单
    initializeDropdowns();
    
    // 处理表单提交时的加载状态
    handleFormSubmissions();
});

/**
 * 初始化Bootstrap工具提示
 */
function initializeTooltips() {
    // 检查是否存在工具提示元素
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        // 初始化所有工具提示
        [...tooltipTriggerList].map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * 初始化Bootstrap下拉菜单
 */
function initializeDropdowns() {
    // 检查是否存在下拉菜单元素
    const dropdownTriggerList = document.querySelectorAll('[data-bs-toggle="dropdown"]');
    if (dropdownTriggerList.length > 0) {
        // 初始化所有下拉菜单
        [...dropdownTriggerList].map(dropdownTriggerEl => {
            return new bootstrap.Dropdown(dropdownTriggerEl);
        });
    }
}

/**
 * 处理表单提交时的加载状态
 */
function handleFormSubmissions() {
    // 查找所有表单
    const forms = document.querySelectorAll('form:not(.no-loader)');
    
    // 为每个表单添加提交事件监听器
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // 查找提交按钮
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                // 保存原始内容
                const originalContent = submitButton.innerHTML;
                
                // 更新为加载状态
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 处理中...';
                
                // 在5分钟后恢复按钮状态（防止永久禁用）
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalContent;
                }, 300000);
            }
        });
    });
} 