"use client";
import React from 'react';
import { X } from 'lucide-react';

interface ToolInputModalProps {
  isOpen: boolean;
  onClose: () => void;
  toolName: string;
  toolInput: Record<string, any>;
}

export default function ToolInputModal({ isOpen, onClose, toolName, toolInput }: ToolInputModalProps) {
  if (!isOpen) return null;

  // 渲染值的辅助函数
  const renderValue = (value: any): React.ReactNode => {
    if (value === null || value === undefined) {
      return <span className="text-gray-400 dark:text-gray-500">null</span>;
    }

    if (typeof value === 'boolean') {
      return <span className="text-blue-600 dark:text-blue-400">{String(value)}</span>;
    }

    if (typeof value === 'number') {
      return <span className="text-green-600 dark:text-green-400">{value}</span>;
    }

    if (typeof value === 'string') {
      // 如果是长文本,使用多行展示
      if (value.length > 100 || value.includes('\n')) {
        return (
          <pre className="text-gray-900 dark:text-gray-100 whitespace-pre-wrap break-words bg-gray-50 dark:bg-gray-800 p-2 rounded text-sm max-h-96 overflow-y-auto">
            {value}
          </pre>
        );
      }
      return <span className="text-gray-900 dark:text-gray-100">{value}</span>;
    }

    if (Array.isArray(value)) {
      if (value.length === 0) {
        return <span className="text-gray-400 dark:text-gray-500">[]</span>;
      }
      return (
        <div className="pl-4 border-l-2 border-gray-300 dark:border-gray-600">
          {value.map((item, idx) => (
            <div key={idx} className="py-1">
              <span className="text-gray-500 dark:text-gray-400 text-sm">[{idx}]</span>: {renderValue(item)}
            </div>
          ))}
        </div>
      );
    }

    if (typeof value === 'object') {
      return (
        <div className="pl-4 border-l-2 border-gray-300 dark:border-gray-600">
          {Object.entries(value).map(([k, v]) => (
            <div key={k} className="py-1">
              <span className="text-purple-600 dark:text-purple-400 font-medium">{k}</span>: {renderValue(v)}
            </div>
          ))}
        </div>
      );
    }

    return <span className="text-gray-900 dark:text-gray-100">{String(value)}</span>;
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50" onClick={onClose}>
      <div
        className="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-3xl w-full max-h-[80vh] overflow-hidden flex flex-col m-4"
        onClick={(e) => e.stopPropagation()}
      >
        {/* 标题栏 */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
            {toolName}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* 内容区域 */}
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {Object.keys(toolInput).length === 0 ? (
            <div className="text-center text-gray-400 dark:text-gray-500 py-8">
              No input parameters
            </div>
          ) : (
            <div className="space-y-3">
              {Object.entries(toolInput).map(([key, value]) => (
                <div key={key} className="border-b border-gray-100 dark:border-gray-800 pb-3 last:border-b-0">
                  <div className="font-medium text-purple-600 dark:text-purple-400 mb-1">
                    {key}
                  </div>
                  <div className="text-sm">
                    {renderValue(value)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 底部按钮 */}
        <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
          >
            关闭
          </button>
        </div>
      </div>
    </div>
  );
}
