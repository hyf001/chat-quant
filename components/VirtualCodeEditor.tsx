'use client';

import React, { useMemo, useRef, useEffect, useState, useCallback } from 'react';

interface VirtualCodeEditorProps {
  content: string;
  language: string;
  hljs?: any;
  lineHeight?: number;
  overscan?: number;
}

const VirtualCodeEditor: React.FC<VirtualCodeEditorProps> = ({
  content,
  language,
  hljs,
  lineHeight = 19,
  overscan = 10,
}) => {
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const lineNumbersRef = useRef<HTMLDivElement>(null);
  const [visibleRange, setVisibleRange] = useState({ start: 0, end: 50 });

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
