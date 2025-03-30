# 导入文件处理工具
from .file_handlers import optimize_upload, get_audio_file_path, get_audio_metadata

# 导入字符串处理工具
from .string_utils import (
    clean_text, 
    format_lyrics,
    generate_slug,
    truncate_text,
    format_file_size
)

# 导入安全工具
from .security import (
    validate_file_type,
    validate_file_size,
    scan_text_content,
    get_client_ip
)

# 导入HTTP工具
from .http_utils import (
    ajax_response,
    render_template_fragment,
    is_ajax,
    ajax_or_template_response,
    paginated_response
)

# 注意：装饰器和统计工具应当从它们自己的模块中导入
# 例如：from music.utils.decorators.auth_decorators import owner_required

# 在此处可以添加其他通用工具类 