// 管理员统计组件
// 负责展示站点统计数据和图表

export default {
    name: 'AdminStatsComponent',
    props: {
        // 初始统计数据
        initialStats: {
            type: Object,
            required: true
        },
        // 图表配置
        chartOptions: {
            type: Object,
            default: () => ({
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000
                },
                scales: {
                    y: {
                        beginAtZero: true
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
            })
        },
        // 刷新间隔（分钟）
        refreshInterval: {
            type: Number,
            default: 5
        }
    },
    data() {
        return {
            stats: { ...this.initialStats },
            loading: false,
            error: null,
            lastUpdated: new Date(),
            charts: {}, // 存储图表实例
            timeRanges: [
                { value: 'today', label: '今天' },
                { value: 'week', label: '本周' },
                { value: 'month', label: '本月' },
                { value: 'year', label: '今年' }
            ],
            selectedTimeRange: 'week',
            refreshIntervalId: null
        };
    },
    computed: {
        formattedLastUpdated() {
            return this.lastUpdated.toLocaleString('zh-CN');
        },
        totalUsers() {
            return this.stats.userStats?.totalUsers || 0;
        },
        totalSongs() {
            return this.stats.musicStats?.totalSongs || 0;
        },
        totalPlays() {
            return this.stats.musicStats?.totalPlays || 0;
        },
        totalDownloads() {
            return this.stats.musicStats?.totalDownloads || 0;
        },
        newUsersToday() {
            return this.stats.userStats?.newUsersToday || 0;
        },
        activeUsersToday() {
            return this.stats.userStats?.activeUsersToday || 0;
        }
    },
    watch: {
        selectedTimeRange() {
            this.fetchStatsByTimeRange();
        }
    },
    mounted() {
        // 初始化图表
        this.initCharts();
        
        // 设置定时刷新
        if (this.refreshInterval > 0) {
            const milliseconds = this.refreshInterval * 60 * 1000;
            this.refreshIntervalId = setInterval(() => {
                this.fetchStats();
            }, milliseconds);
        }
    },
    beforeUnmount() {
        // 清除定时器
        if (this.refreshIntervalId) {
            clearInterval(this.refreshIntervalId);
        }
        
        // 销毁图表
        Object.values(this.charts).forEach(chart => {
            if (chart) {
                chart.destroy();
            }
        });
    },
    methods: {
        // 初始化图表
        async initCharts() {
            // 在DOM更新后初始化图表
            await this.$nextTick();
            
            try {
                // 确保Chart.js已加载
                if (window.Chart) {
                    this.createUserChart();
                    this.createMusicChart();
                    this.createActivityChart();
                } else {
                    console.error('Chart.js未加载，无法创建图表');
                }
            } catch (error) {
                console.error('初始化图表失败:', error);
                this.error = '图表初始化失败';
            }
        },
        
        // 创建用户统计图表
        createUserChart() {
            const ctx = document.getElementById('user-chart');
            if (!ctx) return;
            
            const data = this.stats.userStats?.userGrowth || [];
            
            this.charts.userChart = new window.Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.map(item => item.date),
                    datasets: [{
                        label: '新注册用户',
                        data: data.map(item => item.newUsers),
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: this.chartOptions
            });
        },
        
        // 创建音乐统计图表
        createMusicChart() {
            const ctx = document.getElementById('music-chart');
            if (!ctx) return;
            
            const data = this.stats.musicStats?.musicActivity || [];
            
            this.charts.musicChart = new window.Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(item => item.date),
                    datasets: [
                        {
                            label: '播放次数',
                            data: data.map(item => item.plays),
                            backgroundColor: 'rgba(54, 162, 235, 0.6)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        },
                        {
                            label: '下载次数',
                            data: data.map(item => item.downloads),
                            backgroundColor: 'rgba(255, 159, 64, 0.6)',
                            borderColor: 'rgba(255, 159, 64, 1)',
                            borderWidth: 1
                        }
                    ]
                },
                options: this.chartOptions
            });
        },
        
        // 创建活动统计图表
        createActivityChart() {
            const ctx = document.getElementById('activity-chart');
            if (!ctx) return;
            
            const data = this.stats.userStats?.activeUsers || [];
            
            this.charts.activityChart = new window.Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.map(item => item.hour),
                    datasets: [{
                        label: '活跃用户',
                        data: data.map(item => item.count),
                        borderColor: 'rgba(153, 102, 255, 1)',
                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.1
                    }]
                },
                options: {
                    ...this.chartOptions,
                    scales: {
                        ...this.chartOptions.scales,
                        x: {
                            title: {
                                display: true,
                                text: '时间 (小时)'
                            }
                        }
                    }
                }
            });
        },
        
        // 更新图表数据
        updateCharts() {
            if (this.charts.userChart && this.stats.userStats?.userGrowth) {
                const data = this.stats.userStats.userGrowth;
                this.charts.userChart.data.labels = data.map(item => item.date);
                this.charts.userChart.data.datasets[0].data = data.map(item => item.newUsers);
                this.charts.userChart.update();
            }
            
            if (this.charts.musicChart && this.stats.musicStats?.musicActivity) {
                const data = this.stats.musicStats.musicActivity;
                this.charts.musicChart.data.labels = data.map(item => item.date);
                this.charts.musicChart.data.datasets[0].data = data.map(item => item.plays);
                this.charts.musicChart.data.datasets[1].data = data.map(item => item.downloads);
                this.charts.musicChart.update();
            }
            
            if (this.charts.activityChart && this.stats.userStats?.activeUsers) {
                const data = this.stats.userStats.activeUsers;
                this.charts.activityChart.data.labels = data.map(item => item.hour);
                this.charts.activityChart.data.datasets[0].data = data.map(item => item.count);
                this.charts.activityChart.update();
            }
        },
        
        // 获取最新统计数据
        async fetchStats() {
            this.loading = true;
            this.error = null;
            
            try {
                const response = await fetch('/admin/api/stats/');
                
                if (!response.ok) {
                    throw new Error(`获取统计数据失败: ${response.status} ${response.statusText}`);
                }
                
                const data = await response.json();
                this.stats = data;
                this.lastUpdated = new Date();
                
                // 更新图表
                this.updateCharts();
                
                this.$emit('stats-updated', data);
                
            } catch (error) {
                console.error('获取统计数据失败:', error);
                this.error = `获取统计数据失败: ${error.message}`;
                this.$emit('stats-error', error);
            } finally {
                this.loading = false;
            }
        },
        
        // 根据时间范围获取统计数据
        async fetchStatsByTimeRange() {
            this.loading = true;
            this.error = null;
            
            try {
                const response = await fetch(`/admin/api/stats/?time_range=${this.selectedTimeRange}`);
                
                if (!response.ok) {
                    throw new Error(`获取统计数据失败: ${response.status} ${response.statusText}`);
                }
                
                const data = await response.json();
                this.stats = data;
                this.lastUpdated = new Date();
                
                // 更新图表
                this.updateCharts();
                
                this.$emit('stats-updated', data);
                
            } catch (error) {
                console.error('获取统计数据失败:', error);
                this.error = `获取统计数据失败: ${error.message}`;
                this.$emit('stats-error', error);
            } finally {
                this.loading = false;
            }
        },
        
        // 手动刷新统计数据
        handleRefresh() {
            this.fetchStats();
        }
    },
    template: `
        <div class="admin-stats-component">
            <!-- 顶部控制栏 -->
            <div class="stats-controls d-flex justify-content-between align-items-center mb-4">
                <div class="time-range-selector">
                    <div class="btn-group" role="group">
                        <template v-for="range in timeRanges">
                            <button type="button" 
                                    :class="['btn', selectedTimeRange === range.value ? 'btn-primary' : 'btn-outline-primary']"
                                    @click="selectedTimeRange = range.value">
                                {{ range.label }}
                            </button>
                        </template>
                    </div>
                </div>
                
                <div class="last-updated d-flex align-items-center">
                    <small class="text-muted me-2">
                        最后更新: {{ formattedLastUpdated }}
                    </small>
                    <button class="btn btn-sm btn-outline-secondary" 
                            @click="handleRefresh" 
                            :disabled="loading">
                        <i class="fas" :class="loading ? 'fa-spinner fa-spin' : 'fa-sync-alt'"></i>
                    </button>
                </div>
            </div>
            
            <!-- 错误提示 -->
            <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
            </div>
            
            <!-- 统计卡片 -->
            <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4 mb-4">
                <!-- 用户数量卡片 -->
                <div class="col">
                    <div class="card h-100 border-0 shadow-sm">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <div class="icon-container bg-primary bg-opacity-10 text-primary p-3 rounded-circle me-3">
                                    <i class="fas fa-users"></i>
                                </div>
                                <h6 class="card-title mb-0">总用户数</h6>
                            </div>
                            <h2 class="fw-bold mb-0">{{ totalUsers }}</h2>
                            <div class="text-success small mt-2" v-if="newUsersToday > 0">
                                <i class="fas fa-arrow-up me-1"></i>
                                今日新增 {{ newUsersToday }} 用户
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 歌曲数量卡片 -->
                <div class="col">
                    <div class="card h-100 border-0 shadow-sm">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <div class="icon-container bg-info bg-opacity-10 text-info p-3 rounded-circle me-3">
                                    <i class="fas fa-music"></i>
                                </div>
                                <h6 class="card-title mb-0">总歌曲数</h6>
                            </div>
                            <h2 class="fw-bold mb-0">{{ totalSongs }}</h2>
                            <div class="text-muted small mt-2">
                                平均每用户 {{ (totalSongs / Math.max(totalUsers, 1)).toFixed(1) }} 首
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 播放次数卡片 -->
                <div class="col">
                    <div class="card h-100 border-0 shadow-sm">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <div class="icon-container bg-success bg-opacity-10 text-success p-3 rounded-circle me-3">
                                    <i class="fas fa-play-circle"></i>
                                </div>
                                <h6 class="card-title mb-0">总播放次数</h6>
                            </div>
                            <h2 class="fw-bold mb-0">{{ totalPlays }}</h2>
                            <div class="text-muted small mt-2">
                                平均每首歌 {{ (totalPlays / Math.max(totalSongs, 1)).toFixed(1) }} 次
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 下载次数卡片 -->
                <div class="col">
                    <div class="card h-100 border-0 shadow-sm">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <div class="icon-container bg-warning bg-opacity-10 text-warning p-3 rounded-circle me-3">
                                    <i class="fas fa-download"></i>
                                </div>
                                <h6 class="card-title mb-0">总下载次数</h6>
                            </div>
                            <h2 class="fw-bold mb-0">{{ totalDownloads }}</h2>
                            <div class="text-muted small mt-2">
                                转化率 {{ ((totalDownloads / Math.max(totalPlays, 1)) * 100).toFixed(1) }}%
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 图表区域 -->
            <div class="row g-4">
                <!-- 用户增长图表 -->
                <div class="col-md-6">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header bg-transparent border-0">
                            <h5 class="card-title mb-0">用户增长趋势</h5>
                        </div>
                        <div class="card-body">
                            <div class="chart-container" style="position: relative; height: 300px;">
                                <canvas id="user-chart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 音乐活动图表 -->
                <div class="col-md-6">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header bg-transparent border-0">
                            <h5 class="card-title mb-0">音乐活动统计</h5>
                        </div>
                        <div class="card-body">
                            <div class="chart-container" style="position: relative; height: 300px;">
                                <canvas id="music-chart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 活动统计图表 -->
                <div class="col-12">
                    <div class="card border-0 shadow-sm">
                        <div class="card-header bg-transparent border-0">
                            <h5 class="card-title mb-0">24小时活跃用户分布</h5>
                        </div>
                        <div class="card-body">
                            <div class="chart-container" style="position: relative; height: 300px;">
                                <canvas id="activity-chart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 统计详情 -->
            <div class="stats-details mt-4" v-if="stats.topItems">
                <div class="row g-4">
                    <!-- 热门歌曲 -->
                    <div class="col-md-6">
                        <div class="card border-0 shadow-sm h-100">
                            <div class="card-header bg-transparent border-0">
                                <h5 class="card-title mb-0">热门歌曲 Top 5</h5>
                            </div>
                            <div class="card-body p-0">
                                <div class="list-group list-group-flush">
                                    <div v-for="(song, index) in stats.topItems.songs" 
                                        :key="song.id" 
                                        class="list-group-item list-group-item-action d-flex align-items-center">
                                        <div class="rank me-3 fw-bold text-muted">{{ index + 1 }}</div>
                                        <div class="song-info flex-grow-1">
                                            <h6 class="mb-0">{{ song.title }}</h6>
                                            <small class="text-muted">{{ song.artist }}</small>
                                        </div>
                                        <div class="stats d-flex">
                                            <div class="me-3 text-primary">
                                                <i class="fas fa-play me-1"></i>
                                                {{ song.plays }}
                                            </div>
                                            <div class="text-success">
                                                <i class="fas fa-download me-1"></i>
                                                {{ song.downloads }}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 活跃用户 -->
                    <div class="col-md-6">
                        <div class="card border-0 shadow-sm h-100">
                            <div class="card-header bg-transparent border-0">
                                <h5 class="card-title mb-0">活跃用户 Top 5</h5>
                            </div>
                            <div class="card-body p-0">
                                <div class="list-group list-group-flush">
                                    <div v-for="(user, index) in stats.topItems.users" 
                                        :key="user.id" 
                                        class="list-group-item list-group-item-action d-flex align-items-center">
                                        <div class="rank me-3 fw-bold text-muted">{{ index + 1 }}</div>
                                        <div class="user-avatar me-3">
                                            <img :src="user.avatar || '/static/img/default-avatar.png'" 
                                                alt="User Avatar" 
                                                class="rounded-circle" 
                                                width="40" 
                                                height="40">
                                        </div>
                                        <div class="user-info flex-grow-1">
                                            <h6 class="mb-0">{{ user.username }}</h6>
                                            <small class="text-muted">注册于 {{ user.joinDate }}</small>
                                        </div>
                                        <div class="stats d-flex">
                                            <div class="me-3">
                                                <i class="fas fa-music me-1"></i>
                                                {{ user.songCount }}
                                            </div>
                                            <div>
                                                <i class="fas fa-headphones me-1"></i>
                                                {{ user.playCount }}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `
}; 