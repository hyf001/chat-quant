'use client';

import React, { useMemo } from 'react';
import VirtualCodeBlock from './VirtualCodeBlock';

interface VirtualJsonViewerProps {
  data: any;
  maxHeight?: number;
  className?: string;
  showLineNumbers?: boolean;
}

const VirtualJsonViewer: React.FC<VirtualJsonViewerProps> = ({
  data,
  maxHeight = 400,
  className = '',
  showLineNumbers = true,
}) => {
  // 将JSON格式化为字符串
  const jsonString = useMemo(() => {
    try {
      return JSON.stringify(data, null, 2);
    } catch (error) {
      return `Error formatting JSON: ${error}`;
    }
  }, [data]);

  return (
    <VirtualCodeBlock
      content={jsonString}
      maxHeight={maxHeight}
      className={className}
      showLineNumbers={showLineNumbers}
    />
  );
};

export default VirtualJsonViewer;
