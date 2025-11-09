import { useState, useCallback, useEffect, useRef } from 'react';

interface UseUserRequestsOptions {
  projectId: string;
}

interface ActiveRequestsResponse {
  hasActiveRequests: boolean;
  activeCount: number;
}

export function useUserRequests({ projectId }: UseUserRequestsOptions) {
  const [hasActiveRequests, setHasActiveRequests] = useState(false);
  const [activeCount, setActiveCount] = useState(0);
  const [isTabVisible, setIsTabVisible] = useState(true); // 默认值设为 true
  
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const previousActiveState = useRef(false);

  /* 跟踪标签页可见状态 */
  useEffect(() => {
    /* 仅在客户端执行 */
    if (typeof document !== 'undefined') {
      setIsTabVisible(!document.hidden);
      
      const handleVisibilityChange = () => {
        setIsTabVisible(!document.hidden);
      };

      document.addEventListener('visibilitychange', handleVisibilityChange);
      return () => {
        document.removeEventListener('visibilitychange', handleVisibilityChange);
      };
    }
  }, []);

  /* 从数据库查询活跃请求状态 */
  const checkActiveRequests = useCallback(async () => {
    if (!isTabVisible) return; // 标签页不可见时停止轮询

    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8080';
      const response = await fetch(`${apiBase}/api/chat/${projectId}/requests/active`);
      if (response.ok) {
        const data: ActiveRequestsResponse = await response.json();
        setHasActiveRequests(data.hasActiveRequests);
        setActiveCount(data.activeCount);
        
        /* 仅在活跃状态变化时输出日志 */
        if (data.hasActiveRequests !== previousActiveState.current) {
          console.log(`🔄 [UserRequests] Active requests: ${data.hasActiveRequests} (count: ${data.activeCount})`);
          previousActiveState.current = data.hasActiveRequests;
        }
      }
    } catch (error) {
      if (process.env.NODE_ENV === 'development') {
        console.error('[UserRequests] Failed to check active requests:', error);
      }
    }
  }, [projectId, isTabVisible]);

  /* 自适应轮询设置 */
  useEffect(() => {
    /* 标签页不可见时停止轮询 */
    if (!isTabVisible) {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      return;
    }

    /* 根据活跃请求状态决定轮询间隔 */
    const pollInterval = hasActiveRequests ? 500 : 5000; // 0.5秒 vs 5秒
    
    /* 清理现有轮询 */
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }

    /* 立即检查一次 */
    checkActiveRequests();

    /* 启动新的轮询 */
    intervalRef.current = setInterval(checkActiveRequests, pollInterval);

    if (process.env.NODE_ENV === 'development') {
      console.log(`⏱️ [UserRequests] Polling interval: ${pollInterval}ms (active: ${hasActiveRequests})`);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [hasActiveRequests, isTabVisible, checkActiveRequests]);

  /* 组件卸载时清理 */
  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  /* 用于 WebSocket 事件的占位函数（保持现有接口） */
  const createRequest = useCallback((
    requestId: string,
    messageId: string,
    instruction: string,
    type: 'act' | 'chat' = 'act'
  ) => {
    /* 立即通过轮询检查状态 */
    checkActiveRequests();
    console.log(`🔄 [UserRequests] Created request: ${requestId}`);
  }, [checkActiveRequests]);

  const startRequest = useCallback((requestId: string) => {
    /* 立即通过轮询检查状态 */
    checkActiveRequests();
    console.log(`▶️ [UserRequests] Started request: ${requestId}`);
  }, [checkActiveRequests]);

  const completeRequest = useCallback((
    requestId: string, 
    isSuccessful: boolean,
    errorMessage?: string
  ) => {
    /* 立即通过轮询检查状态 */
    setTimeout(checkActiveRequests, 100); // 稍作延迟后检查
    console.log(`✅ [UserRequests] Completed request: ${requestId} (${isSuccessful ? 'success' : 'failed'})`);
  }, [checkActiveRequests]);

  return {
    hasActiveRequests,
    activeCount,
    createRequest,
    startRequest,
    completeRequest,
    /* 兼容旧版接口 */
    requests: [],
    activeRequests: [],
    getRequest: () => undefined,
    clearCompletedRequests: () => {}
  };
}