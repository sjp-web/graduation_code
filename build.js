// 简单的构建脚本
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 确保目录存在
const ensureDir = (dir) => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
};

// 构建Vue组件
const buildVueComponents = () => {
  try {
    console.log('开始构建Vue组件...');
    execSync('npx vite build', { stdio: 'inherit' });
    console.log('Vue组件构建成功！');
  } catch (error) {
    console.error('Vue组件构建失败:', error);
    process.exit(1);
  }
};

// 确保有默认封面图片
const ensureDefaultCover = () => {
  const svgPath = path.join(__dirname, 'staticfiles', 'images', 'default-cover.svg');
  const pngPath = path.join(__dirname, 'staticfiles', 'images', 'default-cover.png');
  
  if (!fs.existsSync(svgPath) && !fs.existsSync(pngPath)) {
    console.warn('警告: 未找到默认封面图片。请确保创建 default-cover.svg 或 default-cover.png');
  }
};

// 主函数
const main = () => {
  // 确保目录结构
  ensureDir(path.join(__dirname, 'staticfiles', 'dist'));
  ensureDir(path.join(__dirname, 'staticfiles', 'images'));
  
  // 检查默认封面
  ensureDefaultCover();
  
  // 构建组件
  buildVueComponents();
  
  console.log('所有任务完成！');
};

// 执行主函数
main(); 