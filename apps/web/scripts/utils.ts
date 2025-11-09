// 环境地址
export const base_url =  process.env.NODE_ENV === 'production' ? '/sdmp/deep_analysis' : '';


export const assistantOptions = [
  { id: 'analysis', name: '数据分析', icon: '' },
  { id: 'fin-analysis', name: '金融数据分析', icon: '' },
  // { id: 'next-js', name: 'AI网页生成', icon: './claude.png' }
];

// Define assistant brand colors
export const assistantBrandColors: { [key: string]: string } = {
  analysis: '#e50012',
  'fin-analysis': '#e50012',
  'next-js': '#e50012',
};
  // Define models for each assistant statically
export const modelsByAssistant = {
  analysis: [
    { id: 'claude-sonnet-4-5', name: 'Claude Sonnet 4.5' },
    { id: 'claude-opus-4.1', name: 'Claude Opus 4.1' },
    { id: 'claude-sonnet-4', name: 'Claude Sonnet 4' }
  ],
  'fin-analysis': [
    { id: 'claude-sonnet-4-5', name: 'Claude Sonnet 4.5' },
    { id: 'claude-opus-4.1', name: 'Claude Opus 4.1' },
    { id: 'claude-sonnet-4', name: 'Claude Sonnet 4' }
  ],
  'next-js': [
    { id: 'claude-sonnet-4-5', name: 'Claude Sonnet 4.5' },
    { id: 'claude-opus-4.1', name: 'Claude Opus 4.1' },
    { id: 'claude-sonnet-4', name: 'Claude Sonnet 4' }
  ]
};

/**
 * 检测是否为 Windows 环境
 */
export const isWindows = typeof window !== 'undefined'
  ? navigator.userAgent.toLowerCase().includes('windows') || navigator.userAgent.toLowerCase().includes('win')
  : typeof process !== 'undefined' && process.platform === 'win32';

/**
 * 获取当前操作系统的路径分隔符
 */
export const PATH_SEPARATOR = isWindows ? '\\' : '/';

/**
 * 标准化路径分隔符（将路径转换为当前系统的格式）
 * @param path - 文件路径
 * @returns 标准化后的路径
 */
export function normalizePath(path: string): string {
  if (isWindows) {
    return path.replace(/\//g, '\\');
  }
  return path.replace(/\\/g, '/');
}

/**
 * 从路径中提取文件名
 * @param path - 文件路径
 * @returns 文件名
 */
export function getFileNameFromPath(path: string): string {
  const separator = path.includes('\\') ? '\\' : '/';
  return path.split(separator).pop() || '';
}

/**
 * 文件图标配置类型
 */
export interface FileIconConfig {
  path: string;
  colorClass: string;
}

/**
 * 根据文件扩展名返回对应的图标配置
 * @param fileExt - 文件扩展名 (小写)
 * @returns 包含图标路径和颜色类名的对象
 */
export const getFileIconConfig = (fileExt: string): FileIconConfig => {
  if (fileExt === 'csv') {
    // CSV 文件图标 (表格图标)
    return {
      path: "M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z",
      colorClass: "text-green-600 dark:text-green-400"
    };
  } else if (['xlsx', 'xls'].includes(fileExt)) {
    // Excel 文件图标
    return {
      path: "M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2",
      colorClass: "text-green-700 dark:text-green-500"
    };
  } else if (['pdf'].includes(fileExt)) {
    // PDF 文件图标
    return {
      path: "M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z",
      colorClass: "text-red-600 dark:text-red-400"
    };
  } else if (['doc', 'docx'].includes(fileExt)) {
    // Word 文件图标
    return {
      path: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
      colorClass: "text-blue-600 dark:text-blue-400"
    };
  } else if (['txt', 'md'].includes(fileExt)) {
    // 文本文件图标
    return {
      path: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
      colorClass: "text-gray-600 dark:text-gray-400"
    };
  } else if (['zip', 'rar', '7z', 'tar', 'gz'].includes(fileExt)) {
    // 压缩文件图标
    return {
      path: "M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4",
      colorClass: "text-yellow-600 dark:text-yellow-400"
    };
  } else {
    // 默认文件图标
    return {
      path: "M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z",
      colorClass: "text-gray-500 dark:text-gray-400"
    };
  }
};

/**
 * 根据文件路径获取语言类型
 * @param path - 文件路径
 * @returns 语言类型字符串
 */
export function getFileLanguage(path: string): string {
  // 标准化路径后再提取扩展名
  const normalizedPath = normalizePath(path);
  const ext = normalizedPath.split('.').pop()?.toLowerCase();
  switch (ext) {
    case 'tsx':
    case 'ts':
      return 'typescript';
    case 'jsx':
    case 'js':
    case 'mjs':
      return 'javascript';
    case 'css':
      return 'css';
    case 'scss':
    case 'sass':
      return 'scss';
    case 'html':
    case 'htm':
      return 'html';
    case 'json':
      return 'json';
    case 'md':
    case 'markdown':
      return 'markdown';
    case 'py':
      return 'python';
    case 'sh':
    case 'bash':
      return 'bash';
    case 'yaml':
    case 'yml':
      return 'yaml';
    case 'xml':
      return 'xml';
    case 'sql':
      return 'sql';
    case 'php':
      return 'php';
    case 'java':
      return 'java';
    case 'c':
      return 'c';
    case 'cpp':
    case 'cc':
    case 'cxx':
      return 'cpp';
    case 'rs':
      return 'rust';
    case 'go':
      return 'go';
    case 'rb':
      return 'ruby';
    case 'vue':
      return 'vue';
    case 'svelte':
      return 'svelte';
    case 'dockerfile':
      return 'dockerfile';
    case 'toml':
      return 'toml';
    case 'ini':
      return 'ini';
    case 'conf':
    case 'config':
      return 'nginx';
    default:
      return 'plaintext';
  }
}

/**
 * 文件图标类型枚举
 */
export type FileIconType =
  | 'folder'
  | 'react-tsx'
  | 'typescript'
  | 'react-jsx'
  | 'javascript'
  | 'css'
  | 'scss'
  | 'html'
  | 'json'
  | 'markdown'
  | 'python'
  | 'shell'
  | 'yaml'
  | 'xml'
  | 'sql'
  | 'database'
  | 'php'
  | 'java'
  | 'c'
  | 'cpp'
  | 'rust'
  | 'go'
  | 'ruby'
  | 'vue'
  | 'svelte'
  | 'docker'
  | 'config'
  | 'lock'
  | 'package-json'
  | 'file';

/**
 * 文件树图标配置
 */
export interface FileTreeIconConfig {
  type: FileIconType;
  colorClass: string;
}

/**
 * 获取文件树中的文件图标配置
 * @param path - 文件路径
 * @param isDir - 是否为目录
 * @returns 图标配置对象
 */
export function getFileTreeIconConfig(path: string, isDir: boolean): FileTreeIconConfig {
  if (isDir) {
    return { type: 'folder', colorClass: 'text-blue-500' };
  }

  // 标准化路径并提取扩展名和文件名
  const normalizedPath = normalizePath(path);
  const ext = normalizedPath.split('.').pop()?.toLowerCase();
  const filename = getFileNameFromPath(normalizedPath)?.toLowerCase() || '';

  // Special files
  if (filename === 'package.json') {
    return { type: 'package-json', colorClass: 'text-green-600' };
  }
  if (filename === 'dockerfile') {
    return { type: 'docker', colorClass: 'text-blue-400' };
  }
  if (filename.startsWith('.env')) {
    return { type: 'lock', colorClass: 'text-yellow-500' };
  }
  if (filename === 'readme.md') {
    return { type: 'markdown', colorClass: 'text-gray-600' };
  }
  if (filename.startsWith('config')) {
    return { type: 'config', colorClass: 'text-gray-500' };
  }

  switch (ext) {
    case 'tsx':
      return { type: 'react-tsx', colorClass: 'text-cyan-400' };
    case 'ts':
      return { type: 'typescript', colorClass: 'text-blue-600' };
    case 'jsx':
      return { type: 'react-jsx', colorClass: 'text-cyan-400' };
    case 'js':
    case 'mjs':
      return { type: 'javascript', colorClass: 'text-yellow-400' };
    case 'css':
      return { type: 'css', colorClass: 'text-blue-500' };
    case 'scss':
    case 'sass':
      return { type: 'scss', colorClass: 'text-pink-500' };
    case 'html':
    case 'htm':
      return { type: 'html', colorClass: 'text-orange-500' };
    case 'json':
      return { type: 'json', colorClass: 'text-yellow-600' };
    case 'md':
    case 'markdown':
      return { type: 'markdown', colorClass: 'text-gray-600' };
    case 'py':
      return { type: 'python', colorClass: 'text-blue-400' };
    case 'sh':
    case 'bash':
      return { type: 'shell', colorClass: 'text-green-500' };
    case 'yaml':
    case 'yml':
      return { type: 'yaml', colorClass: 'text-red-500' };
    case 'xml':
      return { type: 'xml', colorClass: 'text-orange-600' };
    case 'sql':
      return { type: 'database', colorClass: 'text-blue-600' };
    case 'php':
      return { type: 'php', colorClass: 'text-indigo-500' };
    case 'java':
      return { type: 'java', colorClass: 'text-red-600' };
    case 'c':
      return { type: 'c', colorClass: 'text-blue-700' };
    case 'cpp':
    case 'cc':
    case 'cxx':
      return { type: 'cpp', colorClass: 'text-blue-600' };
    case 'rs':
      return { type: 'rust', colorClass: 'text-orange-700' };
    case 'go':
      return { type: 'go', colorClass: 'text-cyan-500' };
    case 'rb':
      return { type: 'ruby', colorClass: 'text-red-500' };
    case 'vue':
      return { type: 'vue', colorClass: 'text-green-500' };
    case 'svelte':
      return { type: 'svelte', colorClass: 'text-orange-600' };
    case 'dockerfile':
      return { type: 'docker', colorClass: 'text-blue-400' };
    case 'toml':
    case 'ini':
    case 'conf':
    case 'config':
      return { type: 'config', colorClass: 'text-gray-500' };
    default:
      return { type: 'file', colorClass: 'text-gray-400' };
  }
}
