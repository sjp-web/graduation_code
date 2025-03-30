(function($) {
    $(document).ready(function() {
        // 高亮显示表格行
        $("#result_list tbody tr").hover(
            function() {
                $(this).addClass("row-highlight");
            },
            function() {
                $(this).removeClass("row-highlight");
            }
        );

        // 点击统计卡片显示图表
        $(".stat-card").click(function() {
            var target = $(this).data("target");
            if (target) {
                $(".chart-container").hide();
                $("#" + target).fadeIn();
            }
        });

        // 初始化工具提示
        if (typeof $.fn.tooltip === 'function') {
            $('[data-toggle="tooltip"]').tooltip();
        }

        // 初始化数据表格增强功能
        enhanceDataTable();
    });

    // 增强数据表格功能
    function enhanceDataTable() {
        var $table = $("#result_list");
        if ($table.length === 0) return;

        // 添加表格响应式包装器
        $table.wrap('<div class="table-responsive"></div>');

        // 添加表格类
        $table.addClass("table table-hover");

        // 添加分页器增强
        $(".paginator").addClass("pagination-enhanced");

        // 添加过滤器折叠功能
        $("#changelist-filter h2").click(function() {
            $(this).next().slideToggle();
        });
    }

    // 添加一些动画效果
    $(".chart-container, .top-list").css({
        opacity: 0,
        transform: "translateY(20px)"
    }).animate({
        opacity: 1,
        transform: "translateY(0)"
    }, 500);

})(django.jQuery); 