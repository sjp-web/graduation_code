/**
 * Vue组件注册工具
 * 用于全局注册常用组件和插件
 */

/**
 * 注册全局组件到Vue应用
 * @param {Object} app - Vue应用实例
 * @param {Object} components - 组件集合，键为组件名，值为组件定义
 */
export function registerComponents(app, components) {
  if (!app || typeof app.component !== 'function') {
    console.error('无效的Vue应用实例');
    return;
  }

  if (!components || typeof components !== 'object') {
    console.error('无效的组件集合');
    return;
  }

  // 注册各个组件
  Object.entries(components).forEach(([name, component]) => {
    app.component(name, component);
    console.log(`已注册组件: ${name}`);
  });
}

/**
 * 注册全局指令到Vue应用
 * @param {Object} app - Vue应用实例
 * @param {Object} directives - 指令集合，键为指令名，值为指令定义
 */
export function registerDirectives(app, directives) {
  if (!app || typeof app.directive !== 'function') {
    console.error('无效的Vue应用实例');
    return;
  }

  if (!directives || typeof directives !== 'object') {
    console.error('无效的指令集合');
    return;
  }

  // 注册各个指令
  Object.entries(directives).forEach(([name, directive]) => {
    app.directive(name, directive);
    console.log(`已注册指令: ${name}`);
  });
}

/**
 * 创建预配置的Vue应用实例
 * @param {Object} options - Vue应用选项
 * @param {Object} [globalComponents] - 要注册的全局组件
 * @param {Object} [globalDirectives] - 要注册的全局指令
 * @returns {Object} Vue应用实例
 */
export function createConfiguredApp(options, globalComponents = {}, globalDirectives = {}) {
  // 这里需要从外部导入 createApp
  // 由于模块化的限制，我们在这个函数中不直接导入Vue
  const { createApp } = window.Vue || (typeof Vue !== 'undefined' ? Vue : null);
  
  if (!createApp) {
    console.error('找不到Vue的createApp函数，请确保Vue已正确加载');
    return null;
  }
  
  // 创建Vue应用
  const app = createApp(options);
  
  // 注册全局组件和指令
  if (Object.keys(globalComponents).length > 0) {
    registerComponents(app, globalComponents);
  }
  
  if (Object.keys(globalDirectives).length > 0) {
    registerDirectives(app, globalDirectives);
  }
  
  return app;
} 