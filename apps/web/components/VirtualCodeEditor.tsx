'use client';

import React, { useMemo, useRef, useEffect, useState, useCallback } from 'react';

interface VirtualCodeEditorProps {
  content: string;
  language: string;
  hljs?: any;
  lineHeight?: number;
  overscan?: number;
  filePath?: string; // 文件路径,用于判断是否为 assets 图片
  projectId?: string; // 项目 ID,用于构建图片 URL
}

const VirtualCodeEditor: React.FC<VirtualCodeEditorProps> = ({
  content,
  language,
  hljs,
  lineHeight = 19,
  overscan = 10,
  filePath,
  projectId,
}) => {
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const lineNumbersRef = useRef<HTMLDivElement>(null);
  const [visibleRange, setVisibleRange] = useState({ start: 0, end: 50 });

  // API 基础地址
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8080';

  // 检查是否为 assets 目录下的图片文件
  const isAssetsImage = useMemo(() => {
    if (!filePath || !projectId) return false;

    // 统一路径分隔符为 / 进行判断 (兼容 Windows 的 \ 和 Unix 的 /)
    const normalizedPath = filePath.replace(/\\/g, '/');

    // 检查是否在 assets 目录下
    const isInAssets = normalizedPath.includes('/assets/') || normalizedPath.startsWith('assets/');

    // 检查是否为图片文件
    const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp', 'ico'];
    // 使用正则表达式分割路径,兼容 Windows 和 Unix 路径
    const ext = filePath.split(/[/\\.]/).pop()?.toLowerCase() || '';
    const isImage = imageExtensions.includes(ext);

    return isInAssets && isImage;
  }, [filePath, projectId]);

  // 构建图片 URL
  const imageUrl = useMemo(() => {
    if (!isAssetsImage || !filePath || !projectId) return '';

    // 提取文件名 (兼容 Windows 反斜杠 \ 和 Unix 正斜杠 /)
    const fileName = filePath.split(/[/\\]/).pop() || '';

    // 构建图片 URL (始终使用正斜杠,因为这是 Web URL)
    return `${API_BASE}/api/assets/${projectId}/${fileName}`;
  }, [isAssetsImage, filePath, projectId, API_BASE]);

  // 将内容按行分割
  const lines = useMemo(() => {
    return content.split('\n');
  }, [content]);

  // 判断是否需要虚拟滚动（超过100行才启用）
  const shouldUseVirtualScroll = lines.length > 100;

  // 对整个内容进行语法高亮
  const highlightedHtml = useMemo(() => {
    if (!hljs || !content) return content;
    try {
      return hljs.highlight(content, { language }).value;
    } catch (error) {
      console.error('Syntax highlighting error:', error);
      return content;
    }
  }, [content, language, hljs]);

  // 计算可见区域
  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    if (!shouldUseVirtualScroll) return;

    const container = e.currentTarget;
    const scrollTop = container.scrollTop;
    const containerHeight = container.clientHeight;

    const startIndex = Math.max(0, Math.floor(scrollTop / lineHeight) - overscan);
    const endIndex = Math.min(
      lines.length,
      Math.ceil((scrollTop + containerHeight) / lineHeight) + overscan
    );

    setVisibleRange({ start: startIndex, end: endIndex });

    // 同步行号滚动
    if (lineNumbersRef.current) {
      lineNumbersRef.current.style.transform = `translateY(-${scrollTop}px)`;
    }
  }, [shouldUseVirtualScroll, lines.length, lineHeight, overscan]);

  // 初始化可见范围
  useEffect(() => {
    if (!shouldUseVirtualScroll) return;

    if (scrollContainerRef.current) {
      const containerHeight = scrollContainerRef.current.clientHeight;
      const initialEnd = Math.min(
        lines.length,
        Math.ceil(containerHeight / lineHeight) + overscan
      );
      setVisibleRange({ start: 0, end: initialEnd });
    }
  }, [shouldUseVirtualScroll, lines.length, lineHeight, overscan]);

  // 提取可见行的高亮HTML
  const visibleHighlightedContent = useMemo(() => {
    if (!shouldUseVirtualScroll) {
      return highlightedHtml;
    }

    // 按行分割高亮的HTML（保留HTML标签）
    const linesArray = lines.slice(visibleRange.start, visibleRange.end);
    return linesArray.join('\n');
  }, [shouldUseVirtualScroll, highlightedHtml, lines, visibleRange]);

  // 总高度
  const totalHeight = lines.length * lineHeight;

  // 可见内容的偏移量
  const offsetY = shouldUseVirtualScroll ? visibleRange.start * lineHeight : 0;

  // 如果是 assets 目录下的图片，显示图片预览
  if (isAssetsImage && imageUrl) {
    return (
      <div className="w-full h-full flex flex-col items-center justify-center bg-white dark:bg-[#0d0d0d] p-8 overflow-auto">
        <div className="flex flex-col items-center gap-4 w-full">
          <img
            src={imageUrl}
            alt={filePath?.split(/[/\\]/).pop() || 'Image preview'}
            className="max-w-full h-auto rounded-lg shadow-lg mx-auto"
            style={{ display: 'block' }}
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.style.display = 'none';
              const parent = target.parentElement;
              if (parent) {
                parent.innerHTML = `
                  <div class="flex flex-col items-center gap-4 p-8 text-gray-500 dark:text-gray-400">
                    <svg class="w-24 h-24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <p class="text-sm">无法加载图片</p>
                    <p class="text-xs text-gray-500 dark:text-gray-600">${imageUrl}</p>
                  </div>
                `;
              }
            }}
          />
          <p className="text-sm text-gray-500 dark:text-gray-400 text-center">
            {filePath?.split(/[/\\]/).pop() || '图片预览'}
          </p>
        </div>
      </div>
    );
  }

  // 如果不需要虚拟滚动，使用简单渲染
  if (!shouldUseVirtualScroll) {
    return (
      <div className="w-full h-full flex bg-white dark:bg-[#0d0d0d] relative">
        {/* Line Numbers */}
        <div
          className="absolute left-0 top-0 bottom-0 bg-gray-50 dark:bg-[#0d0d0d] px-3 py-4 select-none flex-shrink-0 overflow-hidden pointer-events-none z-10"
          style={{ width: '60px' }}
        >
          <div
            ref={lineNumbersRef}
            className="text-[13px] font-mono text-gray-500 dark:text-[#858585]"
            style={{ lineHeight: `${lineHeight}px` }}
          >
            {lines.map((_, index) => (
              <div key={index} className="text-right pr-2">
                {index + 1}
              </div>
            ))}
          </div>
        </div>

        {/* Code Content */}
        <div
          ref={scrollContainerRef}
          className="flex-1 overflow-auto custom-scrollbar code-scroll-container"
          style={{ paddingLeft: '60px' }}
          onScroll={(e) => {
            const scrollTop = e.currentTarget.scrollTop;
            if (lineNumbersRef.current) {
              lineNumbersRef.current.style.transform = `translateY(-${scrollTop}px)`;
            }
          }}
        >
          <pre
            className="p-4 text-[13px] font-mono text-gray-800 dark:text-[#d4d4d4] whitespace-pre"
            style={{
              fontFamily: "'Fira Code', 'Consolas', 'Monaco', monospace",
              lineHeight: `${lineHeight}px`,
              margin: 0,
            }}
          >
            <code
              className={`language-${language}`}
              dangerouslySetInnerHTML={{ __html: highlightedHtml }}
            />
          </pre>
        </div>
      </div>
    );
  }

  // 使用虚拟滚动
  return (
    <div className="w-full h-full flex bg-white dark:bg-[#0d0d0d] relative">
      {/* Line Numbers - Fixed Position */}
      <div
        className="absolute left-0 top-0 bottom-0 bg-gray-50 dark:bg-[#0d0d0d] px-3 py-4 select-none flex-shrink-0 overflow-hidden pointer-events-none z-10"
        style={{ width: '60px' }}
      >
        <div
          ref={lineNumbersRef}
          className="text-[13px] font-mono text-gray-500 dark:text-[#858585]"
          style={{ lineHeight: `${lineHeight}px` }}
        >
          {lines.map((_, index) => (
            <div key={index} className="text-right pr-2">
              {index + 1}
            </div>
          ))}
        </div>
      </div>

      {/* Code Content with Virtual Scrolling */}
      <div
        ref={scrollContainerRef}
        className="flex-1 overflow-auto custom-scrollbar code-scroll-container"
        style={{ paddingLeft: '60px' }}
        onScroll={handleScroll}
      >
        <div style={{ height: totalHeight, position: 'relative' }}>
          <div
            style={{
              position: 'absolute',
              top: offsetY,
              left: 0,
              right: 0,
            }}
          >
            <pre
              className="p-4 text-[13px] font-mono text-gray-800 dark:text-[#d4d4d4] whitespace-pre"
              style={{
                fontFamily: "'Fira Code', 'Consolas', 'Monaco', monospace",
                lineHeight: `${lineHeight}px`,
                margin: 0,
              }}
            >
              <code className={`language-${language}`}>
                {visibleHighlightedContent}
              </code>
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VirtualCodeEditor;
