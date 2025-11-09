"use client";

import { useState, useRef, useEffect, useCallback } from 'react';
import { SendHorizontal, MessageSquare, Image, Wrench, Square, Loader2 } from 'lucide-react';
import { FileAutocomplete } from './FileAutocomplete';
import {base_url, assistantOptions} from '../../scripts/utils'
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8080';
interface UploadedFile {
  id: string;
  filename: string;
  path: string;
  url: string;
  file_type: 'image' | 'csv' | 'text' | 'unknown';
  original_filename?: string;
}

interface ChatInputProps {
  onSendMessage: (message: string, images?: UploadedFile[]) => void;
  disabled?: boolean;
  placeholder?: string;
  mode?: 'act' | 'chat';
  onModeChange?: (mode: 'act' | 'chat') => void;
  projectId?: string;
  preferredCli?: string;
  selectedModel?: string;
  thinkingMode?: boolean;
  onThinkingModeChange?: (enabled: boolean) => void;
  hasActiveRequests?: boolean;
  onStop?: () => void;
}

export default function ChatInput({
  onSendMessage,
  disabled = false,
  placeholder = "直接提出你的问题，或描述你想要查看的数据...",
  mode = 'act',
  onModeChange,
  projectId,
  preferredCli = 'agent',
  selectedModel = '',
  thinkingMode = false,
  onThinkingModeChange,
  hasActiveRequests = false,
  onStop
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [uploadedImages, setUploadedImages] = useState<UploadedFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [isStoppingRequest, setIsStoppingRequest] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // File autocomplete states
  const [showFileAutocomplete, setShowFileAutocomplete] = useState(false);
  const [fileSearchResults, setFileSearchResults] = useState<any[]>([]);
  const [fileSearchLoading, setFileSearchLoading] = useState(false);
  const [selectedFileIndex, setSelectedFileIndex] = useState(0);
  const [autocompletePosition, setAutocompletePosition] = useState<{ bottom?: number; top?: number; left: number }>({ left: 0 });
  const [atSymbolStart, setAtSymbolStart] = useState<number>(-1);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if ((message.trim() || uploadedImages.length > 0) && !disabled) {
      // If only files without text, use a placeholder message for the AI
      const finalMessage = message.trim() || (uploadedImages.length > 0 ? 'Please analyze the uploaded file(s).' : '');
      // Send message and files separately - unified_manager will add file references
      onSendMessage(finalMessage, uploadedImages);
      setMessage('');
      setUploadedImages([]);
      if (textareaRef.current) {
        textareaRef.current.style.height = '40px';
      }
    }
  };

  const handleStop = async () => {
    if (!onStop || isStoppingRequest) return;

    try {
      setIsStoppingRequest(true);
      await onStop();
    } catch (error) {
      console.error('Failed to stop request:', error);
    } finally {
       setIsStoppingRequest(false);
      // Keep loading state until hasActiveRequests becomes false
      // The parent component will update hasActiveRequests when the request is actually stopped
    }
  };

  // Reset stopping state when hasActiveRequests becomes false
  useEffect(() => {
    if (!hasActiveRequests && isStoppingRequest) {
      setIsStoppingRequest(false);
    }
  }, [hasActiveRequests, isStoppingRequest]);

  // File search function
  const searchFiles = useCallback(async (query: string) => {
    if (!projectId) return;

    setFileSearchLoading(true);
    try {
      const response = await fetch(
        `${API_BASE}/api/projects/${projectId}/files/search?q=${encodeURIComponent(query)}&limit=20`
      );
      if (response.ok) {
        const data = await response.json();
        setFileSearchResults(data.files);
      }
    } catch (error) {
      console.error('File search failed:', error);
    } finally {
      setFileSearchLoading(false);
    }
  }, [projectId]);

  // Handle textarea change with @ detection
  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setMessage(value);

    // Get cursor position
    const cursorPos = e.target.selectionStart;

    // Check for @ symbol before cursor
    const textBeforeCursor = value.substring(0, cursorPos);
    const atMatch = textBeforeCursor.match(/@(\S*)$/);

    if (atMatch) {
      // Found @ symbol
      const query = atMatch[1];
      const atPos = cursorPos - query.length - 1;

      setAtSymbolStart(atPos);
      setShowFileAutocomplete(true);
      setSelectedFileIndex(0);

      // Calculate dropdown position (show above textarea)
      if (textareaRef.current) {
        const rect = textareaRef.current.getBoundingClientRect();
        setAutocompletePosition({
          bottom: window.innerHeight - rect.top + 5,
          left: rect.left
        });
      }

      // Execute search
      searchFiles(query);
    } else {
      // No @ found
      setShowFileAutocomplete(false);
      setAtSymbolStart(-1);
    }
  };

  // Handle file selection
  const handleFileSelect = (file: any) => {
    if (atSymbolStart === -1 || !textareaRef.current) return;

    const currentValue = message;
    const cursorPos = textareaRef.current.selectionStart;

    // Replace @query with @filepath
    const textBeforeCursor = currentValue.substring(0, cursorPos);
    const textAfterCursor = currentValue.substring(cursorPos);
    const beforeAt = textBeforeCursor.substring(0, atSymbolStart);

    const newValue = `${beforeAt}@${file.path} ${textAfterCursor}`;
    setMessage(newValue);

    // Close autocomplete
    setShowFileAutocomplete(false);
    setAtSymbolStart(-1);

    // Set cursor position
    setTimeout(() => {
      if (textareaRef.current) {
        const newCursorPos = beforeAt.length + file.path.length + 2; // +2 for @ and space
        textareaRef.current.selectionStart = newCursorPos;
        textareaRef.current.selectionEnd = newCursorPos;
        textareaRef.current.focus();
      }
    }, 0);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Handle file autocomplete navigation
    if (showFileAutocomplete && fileSearchResults.length > 0) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedFileIndex(prev =>
          prev < fileSearchResults.length - 1 ? prev + 1 : 0
        );
        return;
      }

      if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedFileIndex(prev =>
          prev > 0 ? prev - 1 : fileSearchResults.length - 1
        );
        return;
      }

      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleFileSelect(fileSearchResults[selectedFileIndex]);
        return;
      }

      if (e.key === 'Escape') {
        e.preventDefault();
        setShowFileAutocomplete(false);
        setAtSymbolStart(-1);
        return;
      }
    }

    // Original Enter to send logic
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = '40px';
      const scrollHeight = textarea.scrollHeight;
      textarea.style.height = `${Math.min(scrollHeight, 200)}px`;
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;
    
    await handleFiles(files);
  };

  const removeImage = (id: string) => {
    setUploadedImages(prev => prev.filter(img => img.id !== id));
  };

  // Handle files (for both drag drop and file input)
  const handleFiles = async (files: FileList) => {
    if (!projectId) return;

    setIsUploading(true);

    try {
      for (let i = 0; i < files.length; i++) {
        const file = files[i];

        // Check if file is supported (image, CSV, or TXT)
        const isImage = file.type.startsWith('image/');
        const isCsv = file.type === 'text/csv' || file.type === 'application/csv' || file.name.endsWith('.csv');
        const isTxt = file.type === 'text/plain' || file.name.endsWith('.txt');

        if (!isImage && !isCsv && !isTxt) {
          console.warn(`Skipping unsupported file type: ${file.name} (${file.type})`);
          continue;
        }

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/api/assets/${projectId}/upload`, {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error(`Upload failed for ${file.name}:`, response.status, errorText);
          throw new Error(`Failed to upload ${file.name}: ${response.status} ${errorText}`);
        }

        const result = await response.json();
        // Use API URL instead of blob URL for persistent file access
        const fileUrl = `${API_BASE}/api/assets/${projectId}/${result.filename}`;

        const newFile: UploadedFile = {
          id: crypto.randomUUID(),
          filename: result.filename,
          path: result.absolute_path,
          url: fileUrl,
          file_type: result.file_type || 'unknown',
          original_filename: result.original_filename || file.name
        };

        setUploadedImages(prev => [...prev, newFile]);
      }
    } catch (error) {
      console.error('File upload failed:', error);
      alert('Failed to upload file. Please try again.');
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  // Drag and drop handlers
  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (projectId) {
      setIsDragOver(true);
    }
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    // Only set to false if we're leaving the container completely
    if (!e.currentTarget.contains(e.relatedTarget as Node)) {
      setIsDragOver(false);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (projectId) {
      e.dataTransfer.dropEffect = 'copy';
    } else {
      e.dataTransfer.dropEffect = 'none';
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    if (!projectId) return;

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFiles(files);
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [message]);

  // Handle clipboard paste for files (images and text files)
  useEffect(() => {
    const handlePaste = (e: ClipboardEvent) => {
      if (!projectId) return;

      const items = e.clipboardData?.items;
      if (!items) return;

      const pastedFiles: File[] = [];
      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        // Support images, CSV, and TXT files
        if (item.type.startsWith('image/') ||
            item.type === 'text/csv' ||
            item.type === 'application/csv' ||
            item.type === 'text/plain') {
          const file = item.getAsFile();
          if (file) {
            pastedFiles.push(file);
          }
        }
      }

      if (pastedFiles.length > 0) {
        e.preventDefault();
        const fileList = {
          length: pastedFiles.length,
          item: (index: number) => pastedFiles[index],
          [Symbol.iterator]: function* () {
            for (let i = 0; i < pastedFiles.length; i++) {
              yield pastedFiles[i];
            }
          }
        } as FileList;

        // Convert to FileList-like object
        Object.defineProperty(fileList, 'length', { value: pastedFiles.length });
        pastedFiles.forEach((file, index) => {
          Object.defineProperty(fileList, index, { value: file });
        });

        handleFiles(fileList);
      }
    };

    document.addEventListener('paste', handlePaste);

    return () => {
      document.removeEventListener('paste', handlePaste);
    };
  }, [projectId, preferredCli]);

  return (
    <div className="flex max-h-[calc(100%-37px)] shrink-0 flex-col overflow-visible">
      <div className="relative top-6">
        <div className="[&_[data-nudge]:not(:first-child)]:hidden"></div>
      </div>
      
      {/* File thumbnails */}
      {uploadedImages.length > 0 && (
        <div className="mb-2 flex flex-wrap gap-2 mr-2 md:mr-0">
          {uploadedImages.map((file, index) => (
            <div key={file.id} className="relative group">
              {file.file_type === 'image' ? (
                <img
                  src={file.url}
                  alt={file.filename}
                  className="w-20 h-20 object-cover rounded-lg border border-gray-200 dark:border-gray-600"
                  onError={(e) => {
                    console.error('Failed to load image:', file.url);
                    // Show broken image placeholder
                    e.currentTarget.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iODAiIHZpZXdCb3g9IjAgMCA4MCA4MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjgwIiBoZWlnaHQ9IjgwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0yNSAzNUwyOSAzMUwzNSAzN0w0NSAyN0w1NSA0NVY1NUgyNVYzNVoiIGZpbGw9IiM5Q0EzQUYiLz4KPHN0cm9rZSB3aWR0aD0iMiIgc3Ryb2tlPSIjNkI3Mjg4IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+';
                    e.currentTarget.alt = 'Failed to load image';
                  }}
                />
              ) : (
                <div className="w-20 h-20 flex flex-col items-center justify-center rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-100 dark:bg-gray-700">
                  <div className="text-2xl mb-1">
                    {file.file_type === 'csv' ? '📊' : file.file_type === 'text' ? '📄' : '📎'}
                  </div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">
                    {file.file_type === 'csv' ? 'CSV' : file.file_type === 'text' ? 'TXT' : 'FILE'}
                  </div>
                </div>
              )}
              <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white text-xs px-1 py-0.5 rounded-b-lg truncate" title={file.original_filename || file.filename}>
                {file.file_type === 'image' ? `Image #${index + 1}` : (file.original_filename || file.filename)}
              </div>
              <button
                type="button"
                onClick={() => removeImage(file.id)}
                className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 text-white rounded-full flex items-center justify-center text-xs opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-600"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}
      
      <form 
        onSubmit={handleSubmit}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`group flex flex-col gap-2 rounded-3xl border transition-all duration-150 ease-in-out relative mr-2 md:mr-0 p-3 ${
          isDragOver 
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 shadow-lg' 
            : 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50'
        }`}
      >
        <div data-state="closed" style={{ cursor: 'text' }}>
          <div className="relative flex flex-1 items-center">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={handleTextareaChange}
              onKeyDown={handleKeyDown}
              className="flex w-full ring-offset-background placeholder:text-gray-500 dark:placeholder:text-gray-400 focus-visible:outline-none focus-visible:ring-0 disabled:cursor-not-allowed disabled:opacity-50 resize-none text-[16px] leading-snug md:text-base max-h-[200px] bg-transparent focus:bg-transparent flex-1 m-1 rounded-md p-0 text-gray-900 dark:text-gray-100"
              id="chatinput"
              placeholder={hasActiveRequests ? "AI 正在生成中..." : placeholder}
              disabled={disabled || hasActiveRequests}
              style={{ minHeight: '40px', height: '40px' }}
            />
          </div>
        </div>
        
        {/* Drag overlay */}
        {isDragOver && projectId && (
          <div className="absolute inset-0 bg-blue-50/90 dark:bg-blue-900/30 rounded-3xl flex items-center justify-center z-10 border-2 border-dashed border-blue-500">
            <div className="text-center">
              <div className="text-2xl mb-2">📎</div>
              <div className="text-sm font-medium text-blue-600 dark:text-blue-400">
                Drop files here
              </div>
              <div className="text-xs text-blue-500 dark:text-blue-500 mt-1">
                Supports: Images (JPG, PNG, GIF, WEBP), CSV, TXT
              </div>
            </div>
          </div>
        )}
        
        <div className="flex items-center gap-1">
          <div className="flex items-center gap-2">
            {/* File Upload Button */}
            {projectId && (
              <label
                className="flex items-center justify-center w-8 h-8 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                title="Upload files (images, CSV, TXT)"
              >
                <Image className="h-4 w-4" />
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*,.csv,.txt,text/csv,text/plain"
                  multiple
                  onChange={handleImageUpload}
                  disabled={isUploading || disabled}
                  className="hidden"
                />
              </label>
            )}
            
            {/* Agent and Model Display */}
            {preferredCli && (
              <div className="flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800/50 rounded-full">
                {/* Agent Icon */}
                {/* <img
                  src={base_url + '/claude.png'}
                  alt={preferredCli}
                  className="w-4 h-4"
                /> */}
                <span>
                  {assistantOptions.find(d => d.id === preferredCli)?.name}Agent
                </span>
                {selectedModel && (
                  <>
                    <span className="text-gray-400 dark:text-gray-600">•</span>
                    <span className="text-gray-500 dark:text-gray-500">
                      {selectedModel === 'claude-sonnet-4-5' ? 'Sonnet 4.5' :
                       selectedModel === 'claude-opus-4.1' ? 'Opus 4.1' :
                       selectedModel === 'claude-sonnet-4' ? 'Sonnet 4' :
                       selectedModel === 'gpt-5' ? 'GPT-5' :
                       selectedModel === 'qwen3-coder-plus' ? 'Qwen3 Coder Plus' :
                       selectedModel === 'gemini-2.5-pro' ? 'Gemini 2.5 Pro' :
                       selectedModel === 'gemini-2.5-flash' ? 'Gemini 2.5 Flash' :
                       selectedModel}
                    </span>
                  </>
                )}
              </div>
            )}
          </div>
          
          <div className="ml-auto flex items-center gap-2">
            {/* Mode Toggle Switch */}
            <div className="flex items-center bg-gray-100 dark:bg-gray-800 rounded-full p-0.5">
              <button
                type="button"
                onClick={() => onModeChange?.('act')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200 ${
                  mode === 'act'
                    ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                    : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
                title="Act Mode: AI can modify code and create/delete files"
              >
                <Wrench className="h-3.5 w-3.5" />
                <span>Act</span>
              </button>
              <button
                type="button"
                onClick={() => onModeChange?.('chat')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200 ${
                  mode === 'chat'
                    ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                    : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
                title="Chat Mode: AI provides answers without modifying code"
              >
                <MessageSquare className="h-3.5 w-3.5" />
                <span>Chat</span>
              </button>
            </div>
            

            {/* Send/Stop Button */}
            <button
              id="chatinput-send-message-button"
              type={hasActiveRequests ? "button" : "submit"}
              onClick={hasActiveRequests ? handleStop : undefined}
              className="flex size-8 items-center justify-center rounded-full bg-gray-900 dark:bg-white text-white dark:text-gray-900 transition-all duration-150 ease-out disabled:cursor-not-allowed disabled:opacity-50 hover:scale-110 disabled:hover:scale-100"
              disabled={isStoppingRequest || (!hasActiveRequests && (disabled || (!message.trim() && (!uploadedImages || uploadedImages.length === 0)) || isUploading))}
              title={isStoppingRequest ? "停止中..." : hasActiveRequests ? "停止生成" : "发送消息"}
            >
              {hasActiveRequests ? (
                isStoppingRequest ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Square className="h-4 w-4 fill-current" />
                )
              ) : (
                <SendHorizontal className="h-4 w-4" />
              )}
            </button>
          </div>
        </div>
      </form>

      {/* File Autocomplete */}
      {showFileAutocomplete && projectId && (
        <FileAutocomplete
          files={fileSearchResults}
          selectedIndex={selectedFileIndex}
          onSelect={handleFileSelect}
          position={autocompletePosition}
          isLoading={fileSearchLoading}
        />
      )}

      <div className="z-10 h-2 w-full bg-background"></div>
    </div>
  );
}
