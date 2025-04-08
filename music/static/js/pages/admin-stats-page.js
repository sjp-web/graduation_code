// 管理员统计页面组件
// 页面级组件，负责协调管理员统计页面功能

import { createApp } from 'https://unpkg.com/vue@3.2.31/dist/vue.esm-browser.js';
import AdminStatsComponent from '../components/admin/AdminStatsComponent.js';

// 初始化页面
document.addEventListener('DOMContentLoaded', () => {
    console.log('管理员统计页面初始化中...');
    
    // 获取挂载点
    const mountPoint = document.getElementById('admin-stats-app');
    if (!mountPoint) {
        console.error('未找到管理员统计组件挂载点');
        return;
    }
    
    try {
        // 获取初始统计数据
        const statsElement = document.getElementById('initial-stats-data');
        let initialStats = {};
        
        if (statsElement && statsElement.textContent) {
            try {
                initialStats = JSON.parse(statsElement.textContent);
                console.log('成功加载初始统计数据');
            } catch (error) {
                console.error('解析初始统计数据失败:', error);
            }
        }
        
        // 创建Vue应用
        const app = createApp({
            components: {
                AdminStatsComponent
            },
            data() {
                return {
                    initialStats,
                    chartOptions: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: {
                            duration: 800
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    precision: 0
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                position: 'top',
                            },
                            tooltip: {
                                mode: 'index',
                                intersect: false
                            }
                        }
                    },
                    refreshInterval: 5 // 5分钟自动刷新
                };
            },
            methods: {
                // 当组件更新统计数据时的处理函数
                handleStatsUpdated(data) {
                    console.log('统计数据已更新');
                    // 可以在这里执行其他操作，如更新页面标题等
                },
                
                // 当组件出现错误时的处理函数
                handleStatsError(error) {
                    console.error('统计组件发生错误:', error);
                    // 可以在这里处理错误，如显示全局通知
                }
            },
            template: `
                <div class="admin-stats-page">
                    <div class="row mb-4">
                        <div class="col-12">
                            <div class="d-flex justify-content-between align-items-center">
                                <h2 class="mb-0">
                                    <i class="fas fa-chart-line me-2"></i>站点统计
                                </h2>
                                <div class="admin-actions">
                                    <a href="/admin/" class="btn btn-outline-primary btn-sm me-2">
                                        <i class="fas fa-cog me-1"></i>管理后台
                                    </a>
                                </div>
                            </div>
                            <p class="text-muted mt-2">查看站点用户和音乐统计数据，掌握平台增长趋势</p>
                        </div>
                    </div>
                    
                    <admin-stats-component
                        :initial-stats="initialStats"
                        :chart-options="chartOptions"
                        :refresh-interval="refreshInterval"
                        @stats-updated="handleStatsUpdated"
                        @stats-error="handleStatsError"
                    ></admin-stats-component>
                </div>
            `
        });
        
        // 挂载应用
        app.mount(mountPoint);
        console.log('管理员统计页面组件挂载成功');
        
    } catch (error) {
        console.error('管理员统计页面初始化失败:', error);
        
        // 显示错误信息
        mountPoint.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <h4 class="alert-heading">初始化失败</h4>
                <p>管理员统计页面加载失败，请刷新页面重试。</p>
                <hr>
                <p class="mb-0">错误详情: ${error.message}</p>
            </div>
        `;
    }
});

// 导出页面初始化函数，便于外部调用
export function initAdminStatsPage() {
    console.log('手动初始化管理员统计页面');
    document.dispatchEvent(new Event('DOMContentLoaded'));
} 