# 从各个视图模块导入视图函数

# 用户相关视图
from .user_views import (
    register, 
    login_view, 
    profile_view, 
    create_profile,
    custom_logout
)

# 音乐相关视图
from .music_views import (
    music_list, 
    upload_music, 
    music_detail, 
    download_music
)

# 搜索相关视图
from .search_views import (
    music_search, 
    search_suggestions
)

# 统计相关视图
from .stats_views import (
    statistics_view
)

# 管理员相关视图
from .admin_views import (
    admin_dashboard
)
