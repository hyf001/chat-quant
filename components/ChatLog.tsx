"use client";
import React, { useEffect, useState, useRef, ReactElement } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { useWebSocket } from '../hooks/useWebSocket';
import ThinkingSection from './chat/ThinkingSection';
import ToolInputModal from './ToolInputModal';



const WS_BASE = process.env.NEXT_PUBLIC_WS_BASE || 'ws://localhost:8080';
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8080';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  message_type?: 'chat' | 'tool_result' | 'tool_use' | 'system' | 'error' | 'info';
  content: string;
  metadata_json?: any;
  parent_message_id?: string;
  session_id?: string;
  conversation_id?: string;
  created_at: string;
}

interface LogEntry {
  id: string;
  type: string;
  data: any;
  timestamp: string;
}

interface ActiveSession {
  status: string;
  session_id?: string;
  instruction?: string;
  started_at?: string;
  duration_seconds?: number;
}

interface ChatLogProps {
  projectId: string;
  onSessionStatusChange?: (isRunning: boolean) => void;
  onProjectStatusUpdate?: (status: string, message?: string) => void;
  startRequest?: (requestId: string) => void;
  completeRequest?: (requestId: string, isSuccessful: boolean, errorMessage?: string) => void;
}

export default function ChatLog({ projectId, onSessionStatusChange, onProjectStatusUpdate, startRequest, completeRequest }: ChatLogProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeSession, setActiveSession] = useState<ActiveSession | null>(null);
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);
  const logsEndRef = useRef<HTMLDivElement>(null);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Tool input modal state
  const [modalState, setModalState] = useState<{
    isOpen: boolean;
    toolName: string;
    toolInput: Record<string, any>;
  }>({
    isOpen: false,
    toolName: '',
    toolInput: {}
  });

  // Use the centralized WebSocket hook
  const { isConnected } = useWebSocket({
    projectId,
    onMessage: (message) => {
      // Handle chat messages from WebSocket
      const chatMessage: ChatMessage = {
        id: message.id || `${Date.now()}-${Math.random()}`,
        role: message.role as ChatMessage['role'],
        message_type: message.message_type as ChatMessage['message_type'],
        content: message.content || '',
        metadata_json: message.metadata_json,
        parent_message_id: message.parent_message_id,
        session_id: message.session_id,
        conversation_id: message.conversation_id,
        created_at: message.created_at || new Date().toISOString()
      };
      
      // Clear waiting state when we receive an assistant message
      if (chatMessage.role === 'assistant') {
        setIsWaitingForResponse(false);
      }
      
      setMessages(prev => {
        const exists = prev.some(msg => msg.id === chatMessage.id);
        if (exists) {
          return prev;
        }
        return [...prev, chatMessage];
      });
    },
    onStatus: (status, data) => {
      
      // Handle project status updates
      if (status === 'project_status' && data) {
        onProjectStatusUpdate?.(data.status, data.message);
      }
      
      // Handle session completion
      if (status === 'act_complete' || status === 'chat_complete') {
        setActiveSession(null);
        onSessionStatusChange?.(false);
        setIsWaitingForResponse(false); // Clear waiting state
        
        /* ★ NEW: Request 完成处理 */
        if (data?.request_id && completeRequest) {
          const isSuccessful = data?.status === 'completed';
          completeRequest(data.request_id, isSuccessful, data?.error);
        }
        
        if (pollIntervalRef.current) {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = null;
        }
      }
      
      // Handle session start
      if (status === 'act_start' || status === 'chat_start') {
        setIsWaitingForResponse(true); // Set waiting state when session starts
        
        /* ★ NEW: Request 开始处理 */  
        if (data?.request_id && startRequest) {
          startRequest(data.request_id);
        }
      }
    },
    onConnect: () => {
    },
    onDisconnect: () => {
    },
    onError: (error) => {
      console.error('🔌 [WebSocket] Error:', error);
    }
  });

  const scrollToBottom = () => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Handle tool use message click
  const handleToolUseClick = (message: ChatMessage) => {
    if (message.message_type === 'tool_use' && message.metadata_json) {
      const toolName = message.metadata_json.tool_name || 'Tool';
      const toolInput = message.metadata_json.tool_input || {};

      setModalState({
        isOpen: true,
        toolName,
        toolInput
      });
    }
  };

  // Close modal
  const closeModal = () => {
    setModalState({
      isOpen: false,
      toolName: '',
      toolInput: {}
    });
  };



  useEffect(scrollToBottom, [messages]);

  // Check for active session on component mount
  const checkActiveSession = async () => {
    onSessionStatusChange?.(false);
  };



  // Load chat history
  const loadChatHistory = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${API_BASE}/api/chat/${projectId}/messages`);
      if (response.ok) {
        const chatMessages: ChatMessage[] = await response.json();
        setMessages(chatMessages);
      }
    } catch (error) {
      console.error('Failed to load chat history:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    if (!projectId) return;

    let mounted = true;

    const loadData = async () => {
      if (mounted) {
        await loadChatHistory();
        await checkActiveSession();
      }
    };

    loadData();

    return () => {
      mounted = false;
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    };
  }, [projectId]);



  // Function to shorten file paths
  const shortenPath = (text: string) => {
    if (!text) return text;

    // Pattern to match file paths (starts with / and contains multiple directories)
    const pathPattern = /\/[^\/\s]+(?:\/[^\/\s]+){3,}\/([^\/\s]+\.[^\/\s]+)/g;

    return text.replace(pathPattern, (match, filename) => {
      return `.../${filename}`;
    });
  };

  // Function to clean user messages by removing think hard instruction and chat mode instructions
  const cleanUserMessage = (content: string) => {
    if (!content) return content;

    let cleanedContent = content;

    // Remove think hard instruction
    cleanedContent = cleanedContent.replace(/\.\s*think\s+hard\.\s*$/, '');

    // Remove chat mode instruction
    cleanedContent = cleanedContent.replace(/\n\nDo not modify code, only answer to the user's request\.$/, '');

    return cleanedContent.trim();
  };

  // Function to render content with thinking tags
  const renderContentWithThinking = (content: string): ReactElement => {
    const parts: ReactElement[] = [];
    let lastIndex = 0;
    const regex = /<thinking>([\s\S]*?)<\/thinking>/g;
    let match;

    while ((match = regex.exec(content)) !== null) {
      // Add text before the thinking tag (with markdown)
      if (match.index > lastIndex) {
        const beforeText = content.slice(lastIndex, match.index).trim();
        if (beforeText) {
          parts.push(
            <ReactMarkdown
              key={`text-${lastIndex}`}
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0 break-words">{children}</p>,
                strong: ({ children }) => <strong className="font-medium">{children}</strong>,
                em: ({ children }) => <em className="italic">{children}</em>,
                code: ({ children }) => <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs font-mono">{children}</code>,
                pre: ({ children }) => <pre className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg my-2 overflow-x-auto text-xs break-words">{children}</pre>,
                ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
                li: ({ children }) => <li className="mb-1 break-words">{children}</li>
              }}
            >
              {beforeText}
            </ReactMarkdown>
          );
        }
      }

      // Add the thinking section using the new component
      const thinkingText = match[1].trim();
      if (thinkingText) {
        parts.push(
          <ThinkingSection
            key={`thinking-${match.index}`}
            content={thinkingText}
          />
        );
      }

      lastIndex = regex.lastIndex;
    }

    // Add remaining text after the last thinking tag (with markdown)
    if (lastIndex < content.length) {
      const remainingText = content.slice(lastIndex).trim();
      if (remainingText) {
        parts.push(
          <ReactMarkdown
            key={`text-${lastIndex}`}
            components={{
              p: ({ children }) => {
                // Check for Planning tool message pattern
                const childrenArray = React.Children.toArray(children);
                const hasPlanning = childrenArray.some(child => {
                  if (typeof child === 'string' && child.includes('Planning for next moves...')) {
                    return true;
                  }
                  return false;
                });
                if (hasPlanning) {
                  return <p className="mb-2 last:mb-0 break-words">
                    <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs font-mono">
                      Planning for next moves...
                    </code>
                  </p>;
                }
                return <p className="mb-2 last:mb-0 break-words">{children}</p>;
              },
              strong: ({ children }) => <strong className="font-medium">{children}</strong>,
              em: ({ children }) => <em className="italic">{children}</em>,
              code: ({ children }) => <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs font-mono">{children}</code>,
              pre: ({ children }) => <pre className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg my-2 overflow-x-auto text-xs break-words">{children}</pre>,
              ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
              li: ({ children }) => <li className="mb-1 break-words">{children}</li>
            }}
          >
            {remainingText}
          </ReactMarkdown>
        );
      }
    }

    // If no thinking tags found, return original content with markdown
    if (parts.length === 0) {
      return (
        <ReactMarkdown
          components={{
            p: ({ children }) => {
              // Check if this paragraph contains Planning tool message
              // The message now comes as plain text "Planning for next moves..."
              // ReactMarkdown passes the whole paragraph with child elements
              const childrenArray = React.Children.toArray(children);
              const hasPlanning = childrenArray.some(child => {
                if (typeof child === 'string' && child.includes('Planning for next moves...')) {
                  return true;
                }
                return false;
              });
              if (hasPlanning) {
                return <p className="mb-2 last:mb-0 break-words">
                  <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs font-mono">
                    Planning for next moves...
                  </code>
                </p>;
              }
              return <p className="mb-2 last:mb-0 break-words">{children}</p>;
            },
            strong: ({ children }) => <strong className="font-medium">{children}</strong>,
            em: ({ children }) => <em className="italic">{children}</em>,
            code: ({ children }) => <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs font-mono">{children}</code>,
            pre: ({ children }) => <pre className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg my-2 overflow-x-auto text-xs break-words">{children}</pre>,
            ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
            ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
            li: ({ children }) => <li className="mb-1 break-words">{children}</li>
          }}
        >
          {content}
        </ReactMarkdown>
      );
    }

    return <>{parts}</>;
  };

  // Message filtering function - hide internal tool results and system messages
  const shouldDisplayMessage = (message: ChatMessage) => {
    // Always show messages that have images (even if content is empty)
    if (message.metadata_json?.has_images || message.metadata_json?.attachments?.length > 0) {
      return true;
    }

    // Hide messages with empty or whitespace-only content (but not if they have images)
    if (!message.content || message.content.trim() === '') {
      return false;
    }

    // Hide tool_result messages (internal processing results)
    if (message.message_type === 'tool_result') {
      return false;
    }

    // Hide system initialization messages
    if (message.role === 'system' && message.message_type === 'system') {
      // Check if it's an initialization message
      if (message.content.includes('initialized') || message.content.includes('Agent')) {
        return false;
      }
    }

    // Hide messages explicitly marked as hidden
    if (message.metadata_json && message.metadata_json.hidden_from_ui) {
      return false;
    }

    // Show all other messages (user messages, assistant text responses, tool use summaries)
    return true;
  };


  return (
    <div className="flex flex-col h-full bg-white dark:bg-black">

      {/* 同时显示消息与日志 */}
      <div className="flex-1 overflow-y-auto px-8 py-3 space-y-2 custom-scrollbar dark:chat-scrollbar">
        {isLoading && (
          <div className="flex items-center justify-center h-32 text-gray-400 dark:text-gray-600 text-sm">
            <div className="flex flex-col items-center">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900 dark:border-white mb-2 mx-auto"></div>
              <p>Loading chat history...</p>
            </div>
          </div>
        )}

        {!isLoading && messages.length === 0 && (
          <div className="flex items-center justify-center h-32 text-gray-400 dark:text-gray-600 text-sm">
            <div className="text-center">
              <div className="text-2xl mb-2">💬</div>
              <p>Start a conversation with your agent</p>
            </div>
          </div>
        )}

        <AnimatePresence>
          {/* Render chat messages */}
          {messages.filter(shouldDisplayMessage).map((message, index) => {

            return (
              <div className="mb-4" key={`message-${message.id}-${index}`}>
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                >
                  {message.role === 'user' ? (
                    // User message - boxed on the right
                    <div className="flex justify-end">
                      <div className="max-w-[80%] bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-3">
                        <div className="text-sm text-gray-900 dark:text-white break-words">
                          {(() => {
                            const cleanedMessage = cleanUserMessage(message.content);

                            // Check if message contains image paths
                            const imagePattern = /Image #\d+ path: ([^\n]+)/g;
                            const imagePaths: string[] = [];
                            let match;

                            while ((match = imagePattern.exec(cleanedMessage)) !== null) {
                              imagePaths.push(match[1]);
                            }

                            // Remove image paths from message
                            const messageWithoutPaths = cleanedMessage.replace(/\n*Image #\d+ path: [^\n]+/g, '').trim();

                            return (
                              <>
                                {messageWithoutPaths && (
                                  <div>{shortenPath(messageWithoutPaths)}</div>
                                )}
                                {(() => {
                                  // Use attachments from metadata if available, otherwise fallback to parsed paths
                                  const attachments = message.metadata_json?.attachments || [];
                                  if (attachments.length > 0) {
                                    return (
                                      <div className="mt-2 flex flex-wrap gap-2 max-w-full">
                                        {attachments.map((attachment: any, idx: number) => {
                                          const imageUrl = `${API_BASE}${attachment.url}`;
                                          console.log('🔗 Image URL:', imageUrl, 'for attachment:', attachment);
                                          return (
                                            <div key={idx} className="relative group max-w-full">
                                              <div className="w-full max-w-[300px] h-auto bg-gray-200 dark:bg-gray-700 rounded-lg overflow-hidden border border-gray-300 dark:border-gray-600">
                                                <img
                                                  src={imageUrl}
                                                  alt={`Image ${idx + 1}`}
                                                  className="w-full h-auto max-w-full object-contain"
                                                  onError={(e) => {
                                                    // Fallback to icon if image fails to load
                                                    const target = e.target as HTMLImageElement;
                                                    console.error('❌ Image failed to load:', target.src, 'Error:', e);
                                                    target.style.display = 'none';
                                                    const parent = target.parentElement;
                                                    if (parent) {
                                                      parent.innerHTML = `
                                                    <div class="w-full h-full flex items-center justify-center">
                                                      <svg class="w-16 h-16 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                      </svg>
                                                    </div>
                                                  `;
                                                    }
                                                  }}
                                                />
                                              </div>
                                              <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 rounded-lg transition-opacity flex items-center justify-center">
                                                <span className="text-white text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity bg-black bg-opacity-60 px-2 py-1 rounded">
                                                  #{idx + 1}
                                                </span>
                                              </div>
                                              {/* Tooltip with filename */}
                                              <div className="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                                                {attachment.name}
                                              </div>
                                            </div>
                                          );
                                        })}
                                      </div>
                                    );
                                  } else if (imagePaths.length > 0) {
                                    // Fallback to old method for backward compatibility
                                    return (
                                      <div className="mt-2 flex flex-wrap gap-2 max-w-full">
                                        {imagePaths.map((path, idx) => {
                                          const filename = path.split('/').pop() || 'image';
                                          return (
                                            <div key={idx} className="relative group max-w-full">
                                              <div className="w-full max-w-[300px] h-auto min-h-[200px] bg-gray-200 dark:bg-gray-700 rounded-lg overflow-hidden border border-gray-300 dark:border-gray-600 flex items-center justify-center">
                                                <svg className="w-16 h-16 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                </svg>
                                              </div>
                                              <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 rounded-lg transition-opacity flex items-center justify-center">
                                                <span className="text-white text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity bg-black bg-opacity-60 px-2 py-1 rounded">
                                                  #{idx + 1}
                                                </span>
                                              </div>
                                              {/* Tooltip with filename */}
                                              <div className="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                                                {filename}
                                              </div>
                                            </div>
                                          );
                                        })}
                                      </div>
                                    );
                                  }
                                  return null;
                                })()}
                              </>
                            );
                          })()}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div
                      className={`text-sm text-gray-900 dark:text-white leading-relaxed ${
                        message.message_type === 'tool_use' ? 'cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg p-2 -m-2 transition-colors' : ''
                      }`}
                      onClick={() => message.message_type === 'tool_use' && handleToolUseClick(message)}
                    >
                      {renderContentWithThinking(shortenPath(message.content))}
                    </div>
                  )}
                </motion.div>
              </div>
            );
          })}

        </AnimatePresence>
        
        {/* Loading indicator for waiting response */}
        {isWaitingForResponse && (
          <div className="mb-4 w-full">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <div className="text-xl text-gray-900 dark:text-white leading-relaxed font-bold">
                <span className="animate-pulse">...</span>
              </div>
            </motion.div>
          </div>
        )}
      </div>

      {/* Tool Input Modal */}
      <ToolInputModal
        isOpen={modalState.isOpen}
        onClose={closeModal}
        toolName={modalState.toolName}
        toolInput={modalState.toolInput}
      />
    </div>
  );
}