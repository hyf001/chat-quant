/**
 * Chat Type Definitions
 */

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  message_type?: 'chat' | 'error' | 'info' | 'tool_use';
  content: string;
  metadata_json?: Record<string, any>;
  parent_message_id?: string;
  session_id?: string;
  conversation_id?: string;
  cli_source?: string;
  request_id?: string; // ★ NEW: 添加 request_id
  created_at: string;
}

export interface ChatSession {
  id: string;
  project_id: string;
  status: 'pending' | 'active' | 'running' | 'completed' | 'failed';
  instruction?: string;
  cli_type?: string;
  started_at: string;
  completed_at?: string;
  error?: string;
}

export interface ImageAttachment {
  name: string;
  url: string;
  base64_data?: string;
  mime_type?: string;
  file_type?: 'image' | 'csv' | 'text' | 'unknown';
  path?: string;
}

// Alias for backward compatibility and clarity
export type FileAttachment = ImageAttachment;

export interface ActRequest {
  instruction: string;
  allow_globs?: string[];
  conversation_id?: string;
  cli_preference?: string;
  fallback_enabled?: boolean;
  images?: ImageAttachment[]; // Can contain images, CSV, and TXT files
  request_id?: string; // ★ NEW: 添加 request_id
}

export interface UserRequest {
  id: string; // request_id
  projectId: string;
  userMessageId: string;
  instruction: string;
  requestType: 'act' | 'chat';
  isCompleted: boolean;
  isSuccessful?: boolean;
  startedAt?: string;
  completedAt?: string;
  cliTypeUsed?: string;
  modelUsed?: string;
  errorMessage?: string;
  resultMetadata?: Record<string, any>;
  createdAt: string;
}

export interface WebSocketEventData {
  type: string;
  data: {
    request_id?: string; // ★ NEW: WebSocket 事件也包含 request_id
    [key: string]: any;
  };
  timestamp?: string;
}

export type ChatMode = 'chat' | 'act';