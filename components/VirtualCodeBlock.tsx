'use client';

import React, { useMemo } from 'react';
import { List } from 'react-window';

interface VirtualCodeBlockProps {
  content: string;
  maxHeight?: number;
  className?: string;
  lineHeight?: number;
  showLineNumbers?: boolean;
}

const VirtualCodeBlock: React.FC<VirtualCodeBlockProps> = ({
  content,
  maxHeight = 400,
  className = '',
  lineHeight = 20,
  showLineNumbers = true,
}) => {
  // 将内容按行分割
  const lines = useMemo(() => {
    return content.split('\n');
  }, [content]);

  // 如果行数较少，直接渲染不使用虚拟滚动
  const shouldUseVirtualScroll = lines.length > 50;

  // 计算行号的宽度
  const lineNumberWidth = useMemo(() => {
    if (!showLineNumbers) return 0;
    const maxLineNumber = lines.length;
    const digits = maxLineNumber.toString().length;
    return Math.max(digits * 8 + 16, 40); // 每个数字约8px，加上padding
  }, [lines.length, showLineNumbers]);

  // 渲染单行 - react-window v2.x 使用 rowProps
  const RowComponent = ({ index, ...rowProps }: any) => (
    <div
      {...rowProps}
      className="hover:bg-gray-50 dark:hover:bg-gray-800"
      style={{
        ...rowProps.style,
        display: 'flex',
        alignItems: 'flex-start',
      }}
    >
      {showLineNumbers && (
        <span
          className="flex-shrink-0 text-gray-400 dark:text-gray-600 select-none text-right pr-3 border-r border-gray-200 dark:border-gray-700"
          style={{ width: lineNumberWidth }}
        >
          {index + 1}
        </span>
      )}
      <pre
        className="flex-1 px-3 m-0 text-xs font-mono text-gray-700 dark:text-gray-300 whitespace-pre overflow-x-auto"
        style={{ lineHeight: `${lineHeight}px` }}
      >
        {lines[index]}
      </pre>
    </div>
  );

  // 如果不需要虚拟滚动，使用简单渲染
  if (!shouldUseVirtualScroll) {
    return (
      <div className={`bg-gray-100 dark:bg-gray-900 rounded-lg overflow-hidden ${className}`}>
        <div className="overflow-auto" style={{ maxHeight }}>
          {lines.map((line, index) => (
            <div
              key={index}
              className="flex items-start hover:bg-gray-50 dark:hover:bg-gray-800"
              style={{ minHeight: lineHeight }}
            >
              {showLineNumbers && (
                <span
                  className="flex-shrink-0 text-gray-400 dark:text-gray-600 select-none text-right pr-3 border-r border-gray-200 dark:border-gray-700"
                  style={{ width: lineNumberWidth }}
                >
                  {index + 1}
                </span>
              )}
              <pre className="flex-1 px-3 m-0 text-xs font-mono text-gray-700 dark:text-gray-300 whitespace-pre overflow-x-auto">
                {line}
              </pre>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // 使用虚拟滚动 - react-window v2.x API
  return (
    <div className={`bg-gray-100 dark:bg-gray-900 rounded-lg overflow-hidden ${className}`}>
      <List
        defaultHeight={Math.min(maxHeight, lines.length * lineHeight)}
        rowCount={lines.length}
        rowHeight={lineHeight}
        rowComponent={RowComponent}
        rowProps={{ lines, showLineNumbers, lineNumberWidth }}
        className="scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200 dark:scrollbar-thumb-gray-600 dark:scrollbar-track-gray-800"
      />
    </div>
  );
};

export default VirtualCodeBlock;
