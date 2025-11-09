/**
 * File Autocomplete Component
 * @ mention style file picker
 */
import React, { useEffect, useRef } from 'react';
import { FaFile, FaFolder, FaFileCode, FaCss3Alt, FaHtml5, FaJs, FaPython } from 'react-icons/fa';
import { SiTypescript, SiJson } from 'react-icons/si';

interface FileItem {
  path: string;
  type: 'file' | 'dir';
  size?: number;
  name: string;
}

interface FileAutocompleteProps {
  files: FileItem[];
  selectedIndex: number;
  onSelect: (file: FileItem) => void;
  position: { bottom?: number; top?: number; left: number };
  isLoading?: boolean;
}

export function FileAutocomplete({
  files,
  selectedIndex,
  onSelect,
  position,
  isLoading = false
}: FileAutocompleteProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  // 滚动到选中项
  useEffect(() => {
    if (containerRef.current && selectedIndex >= 0 && files.length > 0) {
      const selectedElement = containerRef.current.children[selectedIndex] as HTMLElement;
      if (selectedElement) {
        selectedElement.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    }
  }, [selectedIndex, files.length]);

  const getFileIcon = (file: FileItem) => {
    if (file.type === 'dir') {
      return <FaFolder className="text-yellow-500 dark:text-yellow-400" />;
    }

    const ext = file.name.split('.').pop()?.toLowerCase();
    switch (ext) {
      case 'ts':
      case 'tsx':
        return <SiTypescript className="text-blue-600 dark:text-blue-400" />;
      case 'js':
      case 'jsx':
        return <FaJs className="text-yellow-500 dark:text-yellow-400" />;
      case 'py':
        return <FaPython className="text-blue-500 dark:text-blue-400" />;
      case 'css':
      case 'scss':
        return <FaCss3Alt className="text-blue-400 dark:text-blue-300" />;
      case 'html':
        return <FaHtml5 className="text-orange-500 dark:text-orange-400" />;
      case 'json':
        return <SiJson className="text-gray-600 dark:text-gray-400" />;
      default:
        return <FaFileCode className="text-gray-500 dark:text-gray-400" />;
    }
  };

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return '';
    if (bytes < 1024) return `${bytes}B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
  };

  if (files.length === 0 && !isLoading) {
    return (
      <div
        className="absolute z-50 w-96 max-h-64 overflow-auto bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl"
        style={{
          bottom: position.bottom !== undefined ? `${position.bottom}px` : undefined,
          top: position.top !== undefined ? `${position.top}px` : undefined,
          left: `${position.left}px`
        }}
      >
        <div className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400 text-center">
          No files found
        </div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="absolute z-50 w-96 max-h-64 overflow-auto bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl"
      style={{
        bottom: position.bottom !== undefined ? `${position.bottom}px` : undefined,
        top: position.top !== undefined ? `${position.top}px` : undefined,
        left: `${position.left}px`
      }}
    >
      {isLoading ? (
        <div className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400 text-center">
          <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-gray-500"></div>
          <span className="ml-2">Searching files...</span>
        </div>
      ) : (
        <>
          <div className="px-3 py-2 text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
            {files.length} file{files.length !== 1 ? 's' : ''} found
          </div>
          {files.map((file, index) => (
            <div
              key={file.path}
              onClick={() => onSelect(file)}
              className={`px-4 py-2 cursor-pointer flex items-center gap-3 transition-colors ${
                index === selectedIndex
                  ? 'bg-blue-100 dark:bg-blue-900/30'
                  : 'hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <div className="flex-shrink-0 w-5 h-5 flex items-center justify-center">
                {getFileIcon(file)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                  {file.name}
                </div>
                {file.path !== file.name && (
                  <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
                    {file.path}
                  </div>
                )}
              </div>
              {file.type === 'file' && file.size && (
                <div className="text-xs text-gray-400 dark:text-gray-500">
                  {formatFileSize(file.size)}
                </div>
              )}
              {file.type === 'dir' && (
                <div className="text-xs text-gray-400 dark:text-gray-500">
                  folder
                </div>
              )}
            </div>
          ))}
        </>
      )}
    </div>
  );
}
