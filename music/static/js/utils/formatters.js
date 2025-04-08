/**
 * 格式化工具函数集合
 */

/**
 * 将秒数格式化为分:秒格式
 * @param {Number} time - 秒数
 * @returns {String} 格式化后的时间字符串
 */
export function formatTime(time) {
  if (isNaN(time)) return '0:00';
  
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

/**
 * 将日期对象格式化为YYYY-MM-DD格式
 * @param {Date} date - 日期对象
 * @returns {String} 格式化后的日期字符串
 */
export function formatDate(date) {
  if (!(date instanceof Date)) {
    date = new Date(date);
  }
  
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  
  return `${year}-${month}-${day}`;
}

/**
 * 将日期时间对象格式化为YYYY-MM-DD HH:MM格式
 * @param {Date} date - 日期对象
 * @returns {String} 格式化后的日期时间字符串
 */
export function formatDateTime(date) {
  if (!(date instanceof Date)) {
    date = new Date(date);
  }
  
  const dateStr = formatDate(date);
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  
  return `${dateStr} ${hours}:${minutes}`;
}

/**
 * 将文件大小（字节）格式化为人类可读的格式
 * @param {Number} bytes - 字节数
 * @param {Number} decimals - 小数位数
 * @returns {String} 格式化后的文件大小
 */
export function formatFileSize(bytes, decimals = 2) {
  if (bytes === 0) return '0 B';
  
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
} 