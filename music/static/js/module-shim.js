/**
 * ES模块导入兼容性脚本
 * 
 * 此脚本用于在不支持ES模块的浏览器中提供基本兼容性
 */

(function() {
  // 检测浏览器是否支持ES模块
  function supportsESModules() {
    try {
      new Function('import("")');
      return true;
    } catch (err) {
      return false;
    }
  }

  // 检测是否支持现代Web API
  function supportsModernWebAPIs() {
    return 'fetch' in window && 
           'Promise' in window && 
           'Symbol' in window &&
           'Map' in window &&
           'Set' in window;
  }

  // 如果不支持ES模块或现代Web API，加载兼容性脚本
  if (!supportsESModules() || !supportsModernWebAPIs()) {
    console.log('浏览器不支持ES模块或现代Web API，加载兼容性脚本');
    
    // 添加ES模块shim脚本
    const shimScript = document.createElement('script');
    shimScript.src = 'https://unpkg.com/es-module-shims@1.6.3/dist/es-module-shims.js';
    shimScript.async = true;
    
    // 将脚本添加到文档中
    document.head.appendChild(shimScript);
    
    // 添加一个标记，表示我们正在使用兼容模式
    window.usingCompatMode = true;
    
    // 触发一个自定义事件，让其他脚本知道我们正在使用兼容模式
    window.addEventListener('load', function() {
      window.dispatchEvent(new CustomEvent('moduleCompatibilityChecked', { 
        detail: { usingCompatMode: true } 
      }));
    });
  } else {
    console.log('浏览器支持ES模块和现代Web API');
    window.usingCompatMode = false;
    
    // 触发一个自定义事件，让其他脚本知道我们不需要使用兼容模式
    window.dispatchEvent(new CustomEvent('moduleCompatibilityChecked', { 
      detail: { usingCompatMode: false } 
    }));
  }
})(); 