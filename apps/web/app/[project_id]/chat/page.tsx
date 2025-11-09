"use client";
import React, { useEffect, useState, useRef, useCallback } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv, MotionH3, MotionP, MotionButton } from '../../../lib/motion';
import { useRouter, useSearchParams } from 'next/navigation';
import dynamic from 'next/dynamic';
// Import highlight.js CSS locally instead of from CDN
import 'highlight.js/styles/atom-one-dark.min.css';
// Import custom styles
import './styles.css';
import { Resizable as ResizableComponent } from 're-resizable';
// Type-safe wrapper to avoid React 19 compatibility issues
const Resizable = ResizableComponent as any;
import { FaCode, FaDesktop, FaMobileAlt, FaPlay, FaStop, FaSync, FaCog, FaRocket, FaFolder, FaFolderOpen, FaFile, FaFileCode, FaCss3Alt, FaHtml5, FaJs, FaReact, FaPython, FaDocker, FaGitAlt, FaMarkdown, FaDatabase, FaPhp, FaJava, FaRust, FaVuejs, FaLock, FaHome, FaChevronUp, FaChevronRight, FaChevronDown, FaArrowLeft, FaArrowRight, FaRedo } from 'react-icons/fa';
import { SiTypescript, SiGo, SiRuby, SiSvelte, SiJson, SiYaml, SiCplusplus } from 'react-icons/si';
import { VscJson } from 'react-icons/vsc';
import ChatLog from '../../../components/ChatLog';
import { ProjectSettings } from '../../../components/settings/ProjectSettings';
import ChatInput from '../../../components/chat/ChatInput';
import { useUserRequests } from '../../../hooks/useUserRequests';
import { useGlobalSettings } from '@/contexts/GlobalSettingsContext';
import { base_url, getFileLanguage, getFileTreeIconConfig, getFileNameFromPath, PATH_SEPARATOR } from '../../../scripts/utils';
import VirtualCodeEditor from '../../../components/VirtualCodeEditor';
import SearchableSelect from '../../../components/SearchableSelect';
/* 不再加载 ProjectSettings（在主页进行全局设置管理） */

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8080';


const symbol_white_icon = `${base_url}/Symbol_white.png`

// Define assistant brand colors
const assistantBrandColors: { [key: string]: string } = {
  claude: '#e50012',
  cursor: '#6B7280',
  qwen: '#A855F7',
  gemini: '#4285F4',
  codex: '#000000'
};



type Entry = { path: string; type: 'file' | 'dir'; size?: number };
type Params = { params: { project_id: string } };
type ProjectStatus = 'initializing' | 'active' | 'failed';
type fileEntry = {
  url: string;
  name: string;
}

// TreeView component for VSCode-style file explorer
interface TreeViewProps {
  entries: Entry[];
  selectedFile: string;
  expandedFolders: Set<string>;
  folderContents: Map<string, Entry[]>;
  loadingFolders: Set<string>;
  onToggleFolder: (path: string) => void;
  onSelectFile: (path: string) => void;
  onLoadFolder: (path: string) => Promise<void>;
  level: number;
  parentPath?: string;
  getFileIcon: (entry: Entry) => React.ReactElement;
}

const TreeView = React.memo(function TreeView({ entries, selectedFile, expandedFolders, folderContents, loadingFolders, onToggleFolder, onSelectFile, onLoadFolder, level, parentPath = '', getFileIcon }: TreeViewProps) {
  // Ensure entries is an array
  if (!entries || !Array.isArray(entries)) {
    return null;
  }

  // Group entries by directory
  const sortedEntries = [...entries].sort((a, b) => {
    // Directories first
    if (a.type === 'dir' && b.type === 'file') return -1;
    if (a.type === 'file' && b.type === 'dir') return 1;
    // Then alphabetical
    return a.path.localeCompare(b.path);
  });

  return (
    <>
      {sortedEntries.map((entry) => {
        // entry.path should already be the full path from API
        const fullPath = entry.path;
        const isExpanded = expandedFolders.has(fullPath);
        const indent = level * 8;

        return (
          <div key={fullPath}>
            <div
              className={`group flex items-center h-[22px] px-2 cursor-pointer ${selectedFile === fullPath
                ? 'bg-blue-100 dark:bg-[#094771]'
                : 'hover:bg-gray-100 dark:hover:bg-[#1a1a1a]'
                }`}
              style={{ paddingLeft: `${8 + indent}px` }}
              onClick={async () => {
                if (entry.type === 'dir') {
                  // Load folder contents if not already loaded
                  if (!folderContents.has(fullPath)) {
                    await onLoadFolder(fullPath);
                  }
                  onToggleFolder(fullPath);
                } else {
                  onSelectFile(fullPath);
                }
              }}
            >
              {/* Chevron for folders */}
              <div className="w-4 flex items-center justify-center mr-0.5">
                {entry.type === 'dir' && (
                  loadingFolders.has(fullPath) ?
                    <span className="w-2.5 h-2.5 text-gray-600 dark:text-[#8b8b8b] flex items-center justify-center animate-spin">⟳</span> :
                    isExpanded ?
                      <span className="w-2.5 h-2.5 text-gray-600 dark:text-[#8b8b8b] flex items-center justify-center"><FaChevronDown size={10} /></span> :
                      <span className="w-2.5 h-2.5 text-gray-600 dark:text-[#8b8b8b] flex items-center justify-center"><FaChevronRight size={10} /></span>
                )}
              </div>

              {/* Icon */}
              <span className="w-4 h-4 flex items-center justify-center mr-1.5">
                {entry.type === 'dir' ? (
                  isExpanded ?
                    <span className="text-amber-600 dark:text-[#c09553] w-4 h-4 flex items-center justify-center"><FaFolderOpen size={16} /></span> :
                    <span className="text-amber-600 dark:text-[#c09553] w-4 h-4 flex items-center justify-center"><FaFolder size={16} /></span>
                ) : (
                  getFileIcon(entry)
                )}
              </span>

              {/* File/Folder name */}
              <span className={`text-[13px] leading-[22px] ${selectedFile === fullPath ? 'text-blue-700 dark:text-white' : 'text-gray-700 dark:text-[#cccccc]'
                }`} style={{ fontFamily: "'Segoe UI', Tahoma, sans-serif", overflow: 'hidden', whiteSpace: 'nowrap', textOverflow: 'ellipsis', flex: '1' }}
                title={getFileNameFromPath(entry.path)}
              >
                {getFileNameFromPath(entry.path)}
              </span>
            </div>

            {/* Render children if expanded */}
            {entry.type === 'dir' && isExpanded && folderContents.has(fullPath) && (
              <TreeView
                entries={folderContents.get(fullPath) || []}
                selectedFile={selectedFile}
                expandedFolders={expandedFolders}
                folderContents={folderContents}
                loadingFolders={loadingFolders}
                onToggleFolder={onToggleFolder}
                onSelectFile={onSelectFile}
                onLoadFolder={onLoadFolder}
                level={level + 1}
                parentPath={fullPath}
                getFileIcon={getFileIcon}
              />
            )}
          </div>
        );
      })}
    </>
  );
});

export default function ChatPage({ params }: Params) {
  const projectId = params.project_id;
  const router = useRouter();
  const searchParams = useSearchParams();

  // ★ NEW: 管理 UserRequests 状态
  const {
    hasActiveRequests,
    createRequest,
    startRequest,
    completeRequest
  } = useUserRequests({ projectId });

  const [projectName, setProjectName] = useState<string>('');
  const [projectDescription, setProjectDescription] = useState<string>('');
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [tree, setTree] = useState<Entry[]>([]);
  const [content, setContent] = useState<string>('');
  const [selectedFile, setSelectedFile] = useState<string>('');
  const [currentPath, setCurrentPath] = useState<string>('.');
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set(['']));
  const [folderContents, setFolderContents] = useState<Map<string, Entry[]>>(new Map());
  const [loadingFolders, setLoadingFolders] = useState<Set<string>>(new Set());
  const [prompt, setPrompt] = useState('');
  const [mode, setMode] = useState<'act' | 'chat'>('act');
  const [isRunning, setIsRunning] = useState(false);
  const [showPreview, setShowPreview] = useState(true);
  const [deviceMode, setDeviceMode] = useState<'desktop' | 'mobile'>('desktop');
  const [showGlobalSettings, setShowGlobalSettings] = useState(false);
  const [uploadedImages, setUploadedImages] = useState<{ name: string, url: string, base64: string }[]>([]);
  const [isInitializing, setIsInitializing] = useState(true);
  // Initialize states with default values, will be loaded from localStorage in useEffect
  const [hasInitialPrompt, setHasInitialPrompt] = useState<boolean>(false);
  const [agentWorkComplete, setAgentWorkComplete] = useState<boolean>(false);
  const [projectStatus, setProjectStatus] = useState<ProjectStatus>('initializing');
  const [initializationMessage, setInitializationMessage] = useState('Starting project initialization...');
  const [initialPromptSent, setInitialPromptSent] = useState(false);
  const initialPromptSentRef = useRef(false);
  const [showPublishPanel, setShowPublishPanel] = useState(false);
  const [publishLoading, setPublishLoading] = useState(false);
  const [githubConnected, setGithubConnected] = useState<boolean | null>(null);
  const [vercelConnected, setVercelConnected] = useState<boolean | null>(null);
  const [publishedUrl, setPublishedUrl] = useState<string | null>(null);
  const [deploymentId, setDeploymentId] = useState<string | null>(null);
  const [deploymentStatus, setDeploymentStatus] = useState<'idle' | 'deploying' | 'ready' | 'error'>('idle');
  const deployPollRef = useRef<NodeJS.Timeout | null>(null);
  const [isStartingPreview, setIsStartingPreview] = useState(false);
  const [previewInitializationMessage, setPreviewInitializationMessage] = useState('正在启动开发服务器...');
  const [preferredCli, setPreferredCli] = useState<string>('claude');
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [usingGlobalDefaults, setUsingGlobalDefaults] = useState<boolean>(true);
  const [thinkingMode, setThinkingMode] = useState<boolean>(false);
  const [currentRoute, setCurrentRoute] = useState<string>('');
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [isFileUpdating, setIsFileUpdating] = useState(false);

  const [sessionId, setSessionId] = useState<string>('');
  // 记录中断状态
  const [recordInterruptState, setRecordInterruptState] = useState<boolean>(false);
  // 获取dashboard目录下的文件
  const [dashboardDirData, setDashboardDirData] = useState<Entry[]>([])

  useEffect(() => {
    setSessionId(searchParams?.get('session_id') || '')
  }, [])

  // Guarded trigger that can be called from multiple places safely
  const triggerInitialPromptIfNeeded = useCallback(() => {
    const initialPromptFromUrl = searchParams?.get('initial_prompt');
    if (!initialPromptFromUrl) return;
    if (initialPromptSentRef.current) return;
    // Synchronously guard to prevent double ACT calls
    initialPromptSentRef.current = true;
    setInitialPromptSent(true);

    // Store the selected model and assistant in sessionStorage when returning
    const cliFromUrl = searchParams?.get('cli');
    const modelFromUrl = searchParams?.get('model');
    if (cliFromUrl) {
      sessionStorage.setItem('selectedAssistant', cliFromUrl);
    }
    if (modelFromUrl) {
      sessionStorage.setItem('selectedModel', modelFromUrl);
    }

    // Don't show the initial prompt in the input field
    // setPrompt(initialPromptFromUrl);
    setTimeout(() => {
      sendInitialPrompt(initialPromptFromUrl);
    }, 300);
  }, [searchParams]);

  const loadDeployStatus = useCallback(async () => {
    try {
      // Use the same API as ServiceSettings to check actual project service connections
      const response = await fetch(`${API_BASE}/api/projects/${projectId}/services`);
      if (response.ok) {
        const connections = await response.json();
        const githubConnection = connections.find((conn: any) => conn.provider === 'github');
        const vercelConnection = connections.find((conn: any) => conn.provider === 'vercel');

        // Check actual project connections (not just token existence)
        setGithubConnected(!!githubConnection);
        setVercelConnected(!!vercelConnection);

        // Set published URL only if actually deployed
        if (vercelConnection && vercelConnection.service_data) {
          const sd = vercelConnection.service_data;
          // Only use actual deployment URLs, not predicted ones
          const rawUrl = sd.last_deployment_url || null;
          const url = rawUrl ? (String(rawUrl).startsWith('http') ? String(rawUrl) : `https://${rawUrl}`) : null;
          setPublishedUrl(url || null);
          if (url) {
            setDeploymentStatus('ready');
          } else {
            setDeploymentStatus('idle');
          }
        } else {
          setPublishedUrl(null);
          setDeploymentStatus('idle');
        }
      } else {
        setGithubConnected(false);
        setVercelConnected(false);
        setPublishedUrl(null);
        setDeploymentStatus('idle');
      }

    } catch (e) {
      console.warn('Failed to load deploy status', e);
      setGithubConnected(false);
      setVercelConnected(false);
      setPublishedUrl(null);
      setDeploymentStatus('idle');
    }
  }, [projectId]);

  const checkCurrentDeployment = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/api/projects/${projectId}/vercel/deployment/current`);
      if (response.ok) {
        const data = await response.json();
        if (data.has_deployment) {
          // 有正在进行的部署时设置状态并开始轮询
          setDeploymentId(data.deployment_id);
          setDeploymentStatus('deploying');
          setPublishLoading(false); // 解除 publishLoading，由 deploymentStatus 控制 UI
          setShowPublishPanel(true); // 打开面板显示进度
          startDeploymentPolling(data.deployment_id);
        }
      }
    } catch (e) {
      console.warn('Failed to check current deployment', e);
    }
  }, [projectId]);

  const startDeploymentPolling = useCallback((depId: string) => {
    if (deployPollRef.current) clearInterval(deployPollRef.current);
    setDeploymentStatus('deploying');
    setDeploymentId(depId);

    deployPollRef.current = setInterval(async () => {
      try {
        const r = await fetch(`${API_BASE}/api/projects/${projectId}/vercel/deployment/current`);
        if (!r.ok) return;
        const data = await r.json();

        // 无进行中的部署则停止轮询（已完成）
        if (!data.has_deployment) {
          // 设置最终部署 URL
          if (data.last_deployment_url) {
            const url = String(data.last_deployment_url).startsWith('http') ? data.last_deployment_url : `https://${data.last_deployment_url}`;
            setPublishedUrl(url);
            setDeploymentStatus('ready');
          } else {
            setDeploymentStatus('idle');
          }

          // 结束发布加载状态（重要：即使没有部署也解除 loading）
          setPublishLoading(false);

          if (deployPollRef.current) {
            clearInterval(deployPollRef.current);
            deployPollRef.current = null;
          }
          return;
        }

        // 存在进行中的部署时
        const status = data.status;

        // Log only status changes
        if (status && status !== 'QUEUED') {
          console.log('🔍 Deployment status:', status);
        }

        // Check if deployment is ready or failed
        const isReady = status === 'READY';
        const isBuilding = status === 'BUILDING' || status === 'QUEUED';
        const isError = status === 'ERROR';

        if (isError) {
          setDeploymentStatus('error');

          // End publish loading state
          setPublishLoading(false);

          // Close publish panel after error (with delay to show error message)
          setTimeout(() => {
            setShowPublishPanel(false);
          }, 3000); // Show error for 3 seconds before closing

          if (deployPollRef.current) {
            clearInterval(deployPollRef.current);
            deployPollRef.current = null;
          }
          return;
        }

        if (isReady && data.deployment_url) {
          const url = String(data.deployment_url).startsWith('http') ? data.deployment_url : `https://${data.deployment_url}`;
          setPublishedUrl(url);
          setDeploymentStatus('ready');

          // End publish loading state
          setPublishLoading(false);

          // Keep panel open to show the published URL

          if (deployPollRef.current) {
            clearInterval(deployPollRef.current);
            deployPollRef.current = null;
          }
        } else if (isBuilding) {
          setDeploymentStatus('deploying');
        }
      } catch (error) {
        console.error('🔍 Polling error:', error);
      }
    }, 1000); /* 改为 1 秒间隔 */
  }, [projectId]);

  async function start(url:string = '') {
    if (recordInterruptState) {
      stop()
      return
    }

    try {
      setIsStartingPreview(true);
      setPreviewInitializationMessage('正在启动开发服务器...');

      let newUrl = url

      console.log(newUrl, 'url')
      if(!newUrl) {
        const r = await fetch(`${API_BASE}/api/projects/${projectId}/preview/start`, { method: 'POST' });
        if (!r.ok) {
          setPreviewInitializationMessage('启动预览失败');
          setTimeout(() => setIsStartingPreview(false), 2000);
          return;
        }
        const data = await r.json();
        newUrl = data.url
      }

      setPreviewInitializationMessage('预览已就绪！');
      setTimeout(() => {
        setPreviewUrl(newUrl);
        setIsStartingPreview(false);
        setCurrentRoute(''); // Reset to root route when starting
      }, 1000);
    } catch (error) {
      console.error('Error starting preview:', error);
      setPreviewInitializationMessage('发生错误');
      setTimeout(() => setIsStartingPreview(false), 2000);
    }
  }

  async function stop() {
    try {
      await fetch(`${API_BASE}/api/projects/${projectId}/preview/stop`, { method: 'POST' });
      setPreviewUrl(null);
      // 停止状态清空
      setRecordInterruptState(false);
      setCurrentRoute('');
    } catch (error) {
      console.error('Error stopping preview:', error);
    }
  }


  // Navigate to specific route in iframe
  const navigateToRoute = (route: string) => {
    const baseUrl = `${API_BASE}/api/static/${projectId}/dashboard/`;
    // Ensure route starts with /
    const normalizedRoute = route.startsWith('/') ? route : `${route}`;
    const newUrl = `${baseUrl}${normalizedRoute}`;
    // iframeRef.current.src = newUrl;
    setPreviewUrl(newUrl)
  };

  // Get available routes from dashboardDirData
  const getAvailableRoutes = () => {
    if (!dashboardDirData || dashboardDirData.length === 0) {
      return [];
    }
    // Extract paths from dashboardDirData
    const routes = dashboardDirData.map(entry => {
      return getFileNameFromPath(entry.path);
    });
    return routes;
  };

  async function chatInputStop() {
    try {
      // TODO: 后端接口对接 - 调用停止聊天会话的 API
      const res = await fetch(`${API_BASE}/api/chat/${projectId}/interrupt`, {
        headers: { 'Content-Type': 'application/json' },
        method: 'POST',
        body: JSON.stringify({ session_id: sessionId })
      });
      // 记录中断成功状态
      if (res.ok) {
        setRecordInterruptState(true)
      } else {
        throw new Error(`claude 未连接 请稍后再试`);
      }

    } catch (error) {
      console.error('❌ claude 未连接 请稍后再试', error);
      alert('claude 未连接 请稍后再试')
      throw error; // 向上抛出错误，让 ChatInput 组件处理
    }
  }



  // Track ongoing tree request to prevent duplicates
  const treeRequestRef = useRef<Promise<void> | null>(null);

  async function loadTree(dir = '.') {
    // If already loading, wait for that request
    if (treeRequestRef.current) {
      return treeRequestRef.current;
    }

    // Create new request
    const requestPromise = (async () => {
      try {
        const r = await fetch(`${API_BASE}/api/repo/${projectId}/tree?dir=${encodeURIComponent(dir)}`);
        const data = await r.json();

        // Ensure data is an array
        if (Array.isArray(data)) {
          setTree(data);

          // Load contents for all directories in the root
          const newFolderContents = new Map();

          // Process each directory
          for (const entry of data) {
            if (entry.type === 'dir') {
              try {
                const subContents = await loadSubdirectory(entry.path);
                newFolderContents.set(entry.path, subContents);
              } catch (err) {
                console.error(`Failed to load contents for ${entry.path}:`, err);
              }
            }
          }

          setFolderContents(newFolderContents);
        } else {
          console.error('Tree data is not an array:', data);
          setTree([]);
        }

        setCurrentPath(dir);
      } catch (error) {
        console.error('Failed to load tree:', error);
        setTree([]);
      } finally {
        // Clear the request reference after completion
        treeRequestRef.current = null;
      }
    })();

    // Track this request
    treeRequestRef.current = requestPromise;
    return requestPromise;
  }

  // Load subdirectory contents
  async function loadSubdirectory(dir: string): Promise<Entry[]> {
    try {

      const r = await fetch(`${API_BASE}/api/repo/${projectId}/tree?dir=${encodeURIComponent(dir)}`);
      const data = await r.json();
      if (dir === 'dashboard') {
        setDashboardDirData(data?.map((d: Entry) => ({ ...d, path: getFileNameFromPath(d.path) })))
      }
      return data;
    } catch (error) {
      console.error('Failed to load subdirectory:', error);
      return [];
    }
  }

  // Track ongoing folder requests to prevent duplicates
  const folderRequestsRef = useRef<Map<string, Promise<void>>>(new Map());

  // Load folder contents
  const handleLoadFolder = useCallback(async (path: string) => {
    // If already loading this folder, wait for that request
    const existingRequest = folderRequestsRef.current.get(path);
    if (existingRequest) {
      return existingRequest;
    }

    // Create new request
    const requestPromise = (async () => {
      // Add to loading state
      setLoadingFolders(prev => new Set(prev).add(path));

      try {
        const contents = await loadSubdirectory(path);
        setFolderContents(prev => {
          const newMap = new Map(prev);
          newMap.set(path, contents);

          // Also load nested directories
          for (const entry of contents) {
            if (entry.type === 'dir') {
              const fullPath = `${path}/${entry.path}`;
              // Don't load if already loaded
              if (!newMap.has(fullPath)) {
                loadSubdirectory(fullPath).then(subContents => {
                  setFolderContents(prev2 => new Map(prev2).set(fullPath, subContents));
                });
              }
            }
          }

          return newMap;
        });
      } finally {
        // Remove from loading state
        setLoadingFolders(prev => {
          const newSet = new Set(prev);
          newSet.delete(path);
          return newSet;
        });
        // Remove from tracking after complete
        folderRequestsRef.current.delete(path);
      }
    })();

    // Track this request
    folderRequestsRef.current.set(path, requestPromise);
    return requestPromise;
  }, []);

  // Toggle folder expansion
  const toggleFolder = useCallback((path: string) => {
    setExpandedFolders(prev => {
      const newSet = new Set(prev);
      if (newSet.has(path)) {
        newSet.delete(path);
      } else {
        newSet.add(path);
      }
      return newSet;
    });
  }, []);


  // Track ongoing file requests to prevent duplicates
  const fileRequestsRef = useRef<Map<string, Promise<void>>>(new Map());

  const openFile = useCallback(async (path: string) => {
    // If already loading this file, wait for that request
    const existingRequest = fileRequestsRef.current.get(path);
    if (existingRequest) {
      return existingRequest;
    }

    // Create new request
    const requestPromise = (async () => {
      try {
        const r = await fetch(`${API_BASE}/api/repo/${projectId}/file?path=${encodeURIComponent(path)}`);
        if (!r.ok) {
          setContent('// Failed to load file content');
          setSelectedFile(path);
          return;
        }

        const data = await r.json();
        setContent(data.content || '');
        setSelectedFile(path);
      } catch (error) {
        console.error('Error opening file:', error);
        setContent('// Error loading file');
        setSelectedFile(path);
      } finally {
        // Remove from tracking after complete
        fileRequestsRef.current.delete(path);
      }

    })();

    // Track this request
    fileRequestsRef.current.set(path, requestPromise);
    return requestPromise;
  }, [projectId]);

  // Track ongoing reload request to prevent duplicates
  const reloadRequestRef = useRef<Promise<void> | null>(null);



  // Lazy load highlight.js only when needed
  const [hljs, setHljs] = useState<any>(null);
  useEffect(() => {
    if (selectedFile && !hljs) {
      import('highlight.js/lib/common').then(mod => {
        setHljs(mod.default);
      });
    }
  }, [selectedFile, hljs]);

  // Get file extension for syntax highlighting
  // Get file icon based on type
  const getFileIcon = useCallback((entry: Entry): React.ReactElement => {
    const iconConfig = getFileTreeIconConfig(entry.path, entry.type === 'dir');

    // Map icon types to React icon components
    const iconMap: Record<string, React.ReactElement> = {
      'folder': <FaFolder size={16} />,
      'react-tsx': <FaReact size={16} />,
      'typescript': <SiTypescript size={16} />,
      'react-jsx': <FaReact size={16} />,
      'javascript': <FaJs size={16} />,
      'css': <FaCss3Alt size={16} />,
      'scss': <FaCss3Alt size={16} />,
      'html': <FaHtml5 size={16} />,
      'json': <VscJson size={16} />,
      'markdown': <FaMarkdown size={16} />,
      'python': <FaPython size={16} />,
      'shell': <FaFileCode size={16} />,
      'yaml': <SiYaml size={16} />,
      'xml': <FaFileCode size={16} />,
      'database': <FaDatabase size={16} />,
      'php': <FaPhp size={16} />,
      'java': <FaJava size={16} />,
      'c': <FaFileCode size={16} />,
      'cpp': <SiCplusplus size={16} />,
      'rust': <FaRust size={16} />,
      'go': <SiGo size={16} />,
      'ruby': <SiRuby size={16} />,
      'vue': <FaVuejs size={16} />,
      'svelte': <SiSvelte size={16} />,
      'docker': <FaDocker size={16} />,
      'config': <FaCog size={16} />,
      'lock': <FaLock size={16} />,
      'package-json': <VscJson size={16} />,
      'file': <FaFile size={16} />,
    };

    const icon = iconMap[iconConfig.type] || <FaFile size={16} />;

    return <span className={iconConfig.colorClass}>{icon}</span>;
  }, []);

  async function loadSettings(projectSettings?: { cli?: string; model?: string }) {
    try {

      // Use project settings if available, otherwise check state
      const hasCliSet = projectSettings?.cli || preferredCli;
      const hasModelSet = projectSettings?.model || selectedModel;

      // Only load global settings if project doesn't have CLI/model settings
      if (!hasCliSet || !hasModelSet) {
        const globalResponse = await fetch(`${API_BASE}/api/settings/global`);
        if (globalResponse.ok) {
          const globalSettings = await globalResponse.json();
          const defaultCli = globalSettings.default_cli || 'agent';

          // Only set if not already set by project
          if (!hasCliSet) {
            setPreferredCli(defaultCli);
          }

          // Set the model for the CLI if not already set
          if (!hasModelSet) {
            const cliSettings = globalSettings.cli_settings?.[hasCliSet || defaultCli];
            if (cliSettings?.model) {
              setSelectedModel(cliSettings.model);
            } else {
              // Set default model based on CLI
              const currentCli = hasCliSet || defaultCli;
              if (currentCli === 'agent') {
                setSelectedModel('claude-sonnet-4-5');
              } else if (currentCli === 'cursor') {
                setSelectedModel('gpt-5');
              } else if (currentCli === 'codex') {
                setSelectedModel('gpt-5');
              } else if (currentCli === 'qwen') {
                setSelectedModel('qwen3-coder-plus');
              } else if (currentCli === 'gemini') {
                setSelectedModel('gemini-2.5-pro');
              }
            }
          }
        } else {
          // Fallback to project settings
          const response = await fetch(`${API_BASE}/api/settings`);
          if (response.ok) {
            const settings = await response.json();
            if (!hasCliSet) setPreferredCli(settings.preferred_cli || 'agent');
            if (!hasModelSet) setSelectedModel(settings.preferred_cli === 'agent' ? 'claude-sonnet-4-5' : 'gpt-5');
          }
        }
      }
    } catch (error) {
      console.error('Failed to load settings:', error);
      // Only set fallback if not already set
      const hasCliSet = projectSettings?.cli || preferredCli;
      const hasModelSet = projectSettings?.model || selectedModel;
      if (!hasCliSet) setPreferredCli('agent');
      if (!hasModelSet) setSelectedModel('claude-sonnet-4-5');
    }
  }

  async function loadProjectInfo() {
    try {
      const r = await fetch(`${API_BASE}/api/projects/${projectId}`);
      if (r.ok) {
        const project = await r.json();

        setProjectName(project.name || `Project ${projectId.slice(0, 8)}`);

        // Set CLI and model from project settings if available
        if (project.preferred_cli) {
          setPreferredCli(project.preferred_cli);
        }
        if (project.selected_model) {
          setSelectedModel(project.selected_model);
        }
        // Determine if we should follow global defaults (no project-specific prefs)
        const followGlobal = !project.preferred_cli && !project.selected_model;
        setUsingGlobalDefaults(followGlobal);
        setProjectDescription(project.description || '');

        // Check if project has initial prompt
        if (project.initial_prompt) {
          setHasInitialPrompt(true);
          localStorage.setItem(`project_${projectId}_hasInitialPrompt`, 'true');
          // Don't start preview automatically if there's an initial prompt
        } else {
          setHasInitialPrompt(false);
          localStorage.setItem(`project_${projectId}_hasInitialPrompt`, 'false');
        }

        // Check initial project status and handle initial prompt
        const initialPromptFromUrl = searchParams?.get('initial_prompt');

        if (project.status === 'initializing') {
          setProjectStatus('initializing');
          setIsInitializing(true);
          /* 处于 initializing 状态时，等待 WebSocket 变为 active */
        } else {
          setProjectStatus('active');
          setIsInitializing(false);

          /* 项目已为 active 时立即开始安装依赖 */
          startDependencyInstallation();

          // Initial prompt: trigger once with shared guard (handles active-on-load case)
          triggerInitialPromptIfNeeded();
        }

        // Always load the file tree after getting project info
        await loadTree('.')

        // Return project settings for use in loadSettings
        return {
          cli: project.preferred_cli,
          model: project.selected_model
        };
      } else {
        // If API fails, use a fallback name
        setProjectName(`Project ${projectId.slice(0, 8)}`);
        setProjectDescription('');
        setHasInitialPrompt(false);
        localStorage.setItem(`project_${projectId}_hasInitialPrompt`, 'false');
        setProjectStatus('active');
        setIsInitializing(false);
        setUsingGlobalDefaults(true);
        return {}; // Return empty object if no project found
      }
    } catch (error) {
      console.error('Failed to load project info:', error);
      // If network error, use a fallback name
      setProjectName(`Project ${projectId.slice(0, 8)}`);
      setProjectDescription('');
      setHasInitialPrompt(false);
      localStorage.setItem(`project_${projectId}_hasInitialPrompt`, 'false');
      setProjectStatus('active');
      setIsInitializing(false);
      setUsingGlobalDefaults(true);
      return {}; // Return empty object on error
    }
  }

  async function runAct(messageOverride?: string, externalImages?: any[]) {
    let finalMessage = messageOverride || prompt;
    const imagesToUse = externalImages || uploadedImages;

    // Allow if there's text OR images
    if (!finalMessage.trim() && (!imagesToUse || imagesToUse.length === 0)) {
      alert('请输入工作内容或上传图像。');
      return;
    }

    // If only images without text, provide a default instruction
    if (!finalMessage.trim() && imagesToUse && imagesToUse.length > 0) {
      finalMessage = "Please analyze the uploaded image(s).";
    }

    /* 在 Chat 模式下追加附加指令 */
    if (mode === 'chat') {
      finalMessage = finalMessage + "\n\nDo not modify code, only answer to the user's request.";
    }

    setIsRunning(true);

    // ★ NEW: 生成 request_id
    const requestId = crypto.randomUUID();

    try {

      const processedImages = imagesToUse.map((img, index) => {

        // Check if this is from ChatInput (has 'path' property) or old format (has 'base64')
        if (img.path) {
          return {
            path: img.path,
            name: img.filename || img.name || 'image'
          };
        } else if (img.base64) {
          return {
            name: img.name,
            base64_data: img.base64.split(',')[1], // Remove data:image/...;base64, prefix
            mime_type: img.base64.split(';')[0].split(':')[1] // Extract mime type
          };
        }

        return img; // Return as-is if already in correct format
      });


      const requestBody = {
        instruction: finalMessage,
        images: processedImages,
        is_initial_prompt: false, // Mark as continuation message
        cli_preference: preferredCli, // Add CLI preference
        selected_model: selectedModel, // Add selected model
        request_id: requestId, // ★ NEW: 添加 request_id
        session_id: sessionId || null
      };


      // Use different endpoint based on mode
      const endpoint = mode === 'act' ? 'act' : 'chat';
      const r = await fetch(`${API_BASE}/api/chat/${projectId}/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });


      if (!r.ok) {
        const errorText = await r.text();
        console.error('❌ API Error:', errorText);
        alert(`错误: ${errorText}`);
        return;
      }

      const result = await r.json();
      setSessionId(result.session_id || '')
      // ★ NEW: 创建 UserRequest
      createRequest(requestId, result.session_id, finalMessage, mode);

      /* 完成后刷新数据 */
      await loadTree('.');

      /* 重置提示与已上传图片 */
      setPrompt('');
      // Clean up old format images if any
      if (uploadedImages && uploadedImages.length > 0) {
        uploadedImages.forEach(img => {
          if (img.url) URL.revokeObjectURL(img.url);
        });
        setUploadedImages([]);
      }

    } catch (error) {
      console.error('Act 执行错误:', error);
      alert(`执行中发生错误：${error}`);
    } finally {
      setIsRunning(false);
    }
  }


  // Handle project status updates via callback from ChatLog
  const handleProjectStatusUpdate = (status: string, message?: string) => {
    const previousStatus = projectStatus;

    /* 状态相同则忽略（避免重复） */
    if (previousStatus === status) {
      return;
    }

    setProjectStatus(status as ProjectStatus);
    if (message) {
      setInitializationMessage(message);
    }

    // If project becomes active, stop showing loading UI
    if (status === 'active') {
      setIsInitializing(false);

      /* 仅在 initializing → active 转换时处理 */
      if (previousStatus === 'initializing') {

        /* 开始安装依赖 */
        startDependencyInstallation();
      }

      // Initial prompt: trigger once with shared guard (handles active-via-WS case)
      triggerInitialPromptIfNeeded();
    } else if (status === 'failed') {
      setIsInitializing(false);
    }
  };

  // Function to start dependency installation in background
  const startDependencyInstallation = async () => {
    try {

      const response = await fetch(`${API_BASE}/api/projects/${projectId}/install-dependencies`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      if (response.ok) {
        const result = await response.json();
      } else {
        const errorText = await response.text();
        console.warn('⚠️ Failed to start dependency installation:', errorText);
      }
    } catch (error) {
      console.error('❌ Error starting dependency installation:', error);
    }
  };

  // Function to send initial prompt automatically
  const sendInitialPrompt = async (initialPrompt: string) => {
    /* 已发送则不再重新发送 */
    if (initialPromptSent) {
      return;
    }

    // Reset task complete state for new initial prompt
    setAgentWorkComplete(false);
    localStorage.setItem(`project_${projectId}_taskComplete`, 'false');

    // ★ NEW: request_id 생성
    const requestId = crypto.randomUUID();

    // No need to add project structure info here - backend will add it for the AI agent
    debugger
    try {
      setIsRunning(true);
      setInitialPromptSent(true); /* 在开始发送时立即设置 */
      const requestBody = {
        instruction: initialPrompt,
        images: [], // No images for initial prompt
        is_initial_prompt: true, // Mark as initial prompt
        request_id: requestId, // ★ NEW: 添加 request_id
        session_id: sessionId || null
      };

      const r = await fetch(`${API_BASE}/api/chat/${projectId}/act`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });

      if (!r.ok) {
        const errorText = await r.text();
        console.error('❌ API Error:', errorText);
        setInitialPromptSent(false); /* 失败后可再次尝试 */
        return;
      }

      const result = await r.json();
      setSessionId(result.session_id || '')
      // ★ NEW: 创建 UserRequest（显示原始 prompt，不增强）
      createRequest(requestId, result.session_id, initialPrompt, 'act');

      // Clear the prompt input after sending
      setPrompt('');

      // Clean up URL by removing the initial_prompt parameter
      const newUrl = new URL(window.location.href);
      newUrl.searchParams.delete('initial_prompt');
      window.history.replaceState({}, '', newUrl.toString());

    } catch (error) {
      console.error('Error sending initial prompt:', error);
      setInitialPromptSent(false); // 失败后可再次尝试
    } finally {
      setIsRunning(false);
    }
  };

  // Load states from localStorage when projectId changes
  useEffect(() => {
    if (typeof window !== 'undefined' && projectId) {
      const storedHasInitialPrompt = localStorage.getItem(`project_${projectId}_hasInitialPrompt`);
      const storedTaskComplete = localStorage.getItem(`project_${projectId}_taskComplete`);

      if (storedHasInitialPrompt !== null) {
        setHasInitialPrompt(storedHasInitialPrompt === 'true');
      }
      if (storedTaskComplete !== null) {
        setAgentWorkComplete(storedTaskComplete === 'true');
      }
    }
  }, [projectId]);

  /* ★ NEW: 根据活跃请求状态自动控制 preview 服务器 */
  const previousActiveState = useRef(false);

  useEffect(() => {
    /* 任务开始时 - 停止 preview 服务器 */
    if (hasActiveRequests && previewUrl) {
      stop();
    }

    /* 任务完成时 - 自动启动 preview 服务器 */
    if (previousActiveState.current && !hasActiveRequests && !previewUrl) {
      start();
    }

    previousActiveState.current = hasActiveRequests;
  }, [hasActiveRequests, previewUrl]);




  useEffect(() => {
    let mounted = true;
    let timer: NodeJS.Timeout | null = null;

    const initializeChat = async () => {
      if (!mounted) return;
      const projectSettings = await loadProjectInfo();
      await loadSettings(projectSettings);
    };

    initializeChat();
    loadDeployStatus().then(() => {
      /* 加载部署状态后检查进行中的部署 */
      checkCurrentDeployment();
    });

    // Listen for service updates from Settings
    const handleServicesUpdate = () => {
      loadDeployStatus();
    };

    // Cleanup function to stop preview server when page is unloaded
    const handleBeforeUnload = () => {
      // Send a request to stop the preview server
      navigator.sendBeacon(`${API_BASE}/api/projects/${projectId}/preview/stop`);
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    window.addEventListener('services-updated', handleServicesUpdate);

    return () => {
      mounted = false;
      if (timer) clearTimeout(timer);

      // Clean up event listeners
      window.removeEventListener('beforeunload', handleBeforeUnload);
      window.removeEventListener('services-updated', handleServicesUpdate);

      // Stop preview server when component unmounts
      if (previewUrl) {
        fetch(`${API_BASE}/api/projects/${projectId}/preview/stop`, { method: 'POST' })
          .catch(() => { });
      }
    };
  }, [projectId, previewUrl, loadDeployStatus, checkCurrentDeployment]);

  // React to global settings changes when using global defaults
  const { settings: globalSettings } = useGlobalSettings();
  useEffect(() => {
    if (!usingGlobalDefaults) return;
    if (!globalSettings) return;

    const cli = globalSettings.default_cli || 'agent';
    setPreferredCli(cli);

    const modelFromGlobal = globalSettings.cli_settings?.[cli]?.model;
    if (modelFromGlobal) {
      setSelectedModel(modelFromGlobal);
    } else {
      // Fallback per CLI
      if (cli === 'claude') setSelectedModel('claude-sonnet-4-5');
      else if (cli === 'cursor') setSelectedModel('gpt-5');
      else if (cli === 'codex') setSelectedModel('gpt-5');
      else setSelectedModel('');
    }
  }, [globalSettings, usingGlobalDefaults]);


  const logClickFile = (fileInfo: fileEntry) => {
    setShowPreview(false);
     setExpandedFolders(prev => {
      const newSet = new Set(prev);
      newSet.add('assets');
      return newSet;
    });
    openFile(`assets${PATH_SEPARATOR}${fileInfo.name}`)
  }

  // Show loading UI if project is initializing

  return (
    <>
      {/* Full screen loading overlay during initialization */}
      {isInitializing && (
        <div className="fixed inset-0 bg-white dark:bg-black flex items-center justify-center z-[9999]">
          {/* Gradient background */}
          <div className="absolute inset-0">
            <div className="absolute inset-0 bg-white dark:bg-black" />
            <div
              className="absolute inset-0 dark:block hidden transition-all duration-1000 ease-in-out"
              style={{
                background: `radial-gradient(circle at 50% 50%,
                  ${assistantBrandColors[preferredCli] || assistantBrandColors.claude}66 0%,
                  ${assistantBrandColors[preferredCli] || assistantBrandColors.claude}4D 25%,
                  ${assistantBrandColors[preferredCli] || assistantBrandColors.claude}33 50%,
                  transparent 70%)`
              }}
            />
            {/* Light mode gradient - subtle */}
            <div
              className="absolute inset-0 block dark:hidden transition-all duration-1000 ease-in-out"
              style={{
                background: `radial-gradient(circle at 50% 50%,
                  ${assistantBrandColors[preferredCli] || assistantBrandColors.claude}40 0%,
                  ${assistantBrandColors[preferredCli] || assistantBrandColors.claude}26 25%,
                  transparent 50%)`
              }}
            />
          </div>

          {/* Content */}
          <div className="relative z-10 text-center">
            {/* Loading spinner */}
            <div className="w-40 h-40 mx-auto mb-6 relative">
              <div
                className="w-full h-full"
                style={{
                  backgroundColor: assistantBrandColors[preferredCli] || assistantBrandColors.claude,
                  mask: `url(${symbol_white_icon}) no-repeat center/contain`,
                  WebkitMask: `url(${symbol_white_icon}) no-repeat center/contain`,
                  opacity: 0.9
                }}
              />

              {/* Loading spinner in center */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div
                  className="w-14 h-14 border-4 border-t-transparent rounded-full animate-spin"
                  style={{
                    borderColor: assistantBrandColors[preferredCli] || assistantBrandColors.claude,
                    borderTopColor: 'transparent'
                  }}
                />
              </div>
            </div>

            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
              加载项目信息...
            </h3>

            <div className="flex items-center justify-center gap-1 text-gray-600 dark:text-gray-400">
              <span>正在获取项目详情</span>
              <MotionDiv
                className="flex gap-1 ml-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <MotionDiv
                  animate={{ opacity: [0, 1, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity, delay: 0 }}
                  className="w-1 h-1 bg-gray-600 dark:bg-gray-400 rounded-full"
                />
                <MotionDiv
                  animate={{ opacity: [0, 1, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity, delay: 0.3 }}
                  className="w-1 h-1 bg-gray-600 dark:bg-gray-400 rounded-full"
                />
                <MotionDiv
                  animate={{ opacity: [0, 1, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity, delay: 0.6 }}
                  className="w-1 h-1 bg-gray-600 dark:bg-gray-400 rounded-full"
                />
              </MotionDiv>
            </div>
          </div>
        </div>
      )}

      <div className="h-screen bg-white dark:bg-black flex relative overflow-hidden">
        <div className="h-full w-full flex">
          {/* 左侧：聊天窗 - 可调整宽度 */}
          <Resizable
            defaultSize={{
              width: '35%',
              height: '100%'
            }}
            minWidth="20%"
            maxWidth="60%"
            enable={{
              top: false,
              right: true,
              bottom: false,
              left: false,
              topRight: false,
              bottomRight: false,
              bottomLeft: false,
              topLeft: false
            }}
            handleStyles={{
              right: {
                width: '8px',
                right: '-4px',
                cursor: 'ew-resize',
              }
            }}
            handleClasses={{
              right: 'chatResizeHandle'
            }}
            className="h-full border-r border-gray-200 dark:border-gray-800 flex flex-col"
          >
            {/* 聊天头部 */}
            <div className="bg-white dark:bg-black border-b border-gray-200 dark:border-gray-800 p-4 h-[73px] flex items-center">
              <div className="flex items-center gap-3">
                <button
                  onClick={() => router.push('/')}
                  className="flex items-center justify-center w-8 h-8 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-colors"
                  title="Back to home"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </button>
                <div>
                  <h1 className="text-lg font-semibold text-gray-900 dark:text-white">{projectName || 'Loading...'}</h1>
                  {projectDescription && (
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {projectDescription}
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* 聊天日志区域 */}
            <div className="flex-1 min-h-0">
              <ChatLog
                projectId={projectId}
                onSessionStatusChange={(isRunningValue) => {
                  console.log('🔍 [DEBUG] Session status change:', isRunningValue);
                  setIsRunning(isRunningValue);
                  // 追踪 Agent 任务完成状态并自动启动 preview
                  if (!isRunningValue && hasInitialPrompt && !agentWorkComplete && !previewUrl) {
                    setAgentWorkComplete(true);
                    // Save to localStorage
                    localStorage.setItem(`project_${projectId}_taskComplete`, 'true');
                    // 初始任务完成后自动启动 preview 服务器
                    start();
                  }
                }}
                onProjectStatusUpdate={handleProjectStatusUpdate}
                startRequest={startRequest}
                completeRequest={completeRequest}
                logClickFile={logClickFile}
              />
            </div>

            {/* 简易输入区域 */}
            <div className="p-4 rounded-bl-2xl">
              <ChatInput
                onSendMessage={(message, images) => {
                  runAct(message, images);
                }}
                disabled={isRunning}
                placeholder={"直接提出你的问题，或描述你想要查看的数据..."}
                mode={mode}
                onModeChange={setMode}
                projectId={projectId}
                preferredCli={preferredCli}
                selectedModel={selectedModel}
                thinkingMode={thinkingMode}
                onThinkingModeChange={setThinkingMode}
                hasActiveRequests={hasActiveRequests}
                onStop={chatInputStop}
              />
            </div>
          </Resizable>

          {/* 右侧：预览/代码区域 */}
          <div className="h-full flex-1 flex flex-col bg-black">
            {/* 内容区域 */}
            <div className="flex-1 min-h-0 flex flex-col">
              {/* Controls Bar */}
              <div className="bg-white dark:bg-black border-b border-gray-200 dark:border-gray-800 px-4 h-[73px] flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {/* 切换开关 */}
                  <div className="flex items-center bg-gray-100 dark:bg-gray-900 rounded-lg p-1">
                    <button
                      className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${showPreview
                        ? 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
                        }`}
                      onClick={() => setShowPreview(true)}
                    >
                      <span className="w-4 h-4 flex items-center justify-center"><FaDesktop size={16} /></span>
                    </button>
                    <button
                      className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${!showPreview
                        ? 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
                        }`}
                      onClick={() => setShowPreview(false)}
                    >
                      <span className="w-4 h-4 flex items-center justify-center"><FaCode size={16} /></span>
                    </button>
                  </div>

                  {/* Center Controls */}
                  {dashboardDirData?.length > 0 && showPreview && (
                    <div className="flex items-center gap-3">
                      {/* Route Navigation - Searchable Select */}
                      <SearchableSelect
                        options={getAvailableRoutes()}
                        value={currentRoute}
                        onChange={(route) => {
                          setCurrentRoute(route);
                          navigateToRoute(route);
                        }}
                        placeholder="选择页面"
                        width="250px"
                      />

                      {/* Action Buttons Group */}
                      <div className="flex items-center gap-1.5">
                        <button
                          className="h-9 w-9 flex items-center justify-center bg-gray-100 dark:bg-gray-900 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-200 dark:hover:bg-gray-800 rounded-lg transition-colors"
                          onClick={() => {
                            const iframe = document.querySelector('iframe');
                            if (iframe) {
                              iframe.src = iframe.src;
                            }
                          }}
                          title="Refresh preview"
                        >
                          <FaRedo size={14} />
                        </button>

                        {/* Device Mode Toggle */}
                        <div className="h-9 flex items-center gap-1 bg-gray-100 dark:bg-gray-900 rounded-lg px-1 border border-gray-200 dark:border-gray-700">
                          <button
                            aria-label="Desktop preview"
                            className={`h-7 w-7 flex items-center justify-center rounded transition-colors ${deviceMode === 'desktop'
                              ? 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30'
                              : 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300'
                              }`}
                            onClick={() => setDeviceMode('desktop')}
                          >
                            <FaDesktop size={14} />
                          </button>
                          <button
                            aria-label="Mobile preview"
                            className={`h-7 w-7 flex items-center justify-center rounded transition-colors ${deviceMode === 'mobile'
                              ? 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30'
                              : 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300'
                              }`}
                            onClick={() => setDeviceMode('mobile')}
                          >
                            <FaMobileAlt size={14} />
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {/* Settings Button */}
                  <button
                    onClick={() => setShowGlobalSettings(true)}
                    className="h-9 w-9 flex items-center justify-center bg-gray-100 dark:bg-gray-900 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-200 dark:hover:bg-gray-800 rounded-lg transition-colors"
                    title="Settings"
                  >
                    <FaCog size={16} />
                  </button>

                  {/* Stop Button */}
                  {showPreview && previewUrl && (
                    <button
                      className="h-9 px-3 bg-red-500 hover:bg-red-600 text-white rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
                      onClick={stop}
                    >
                      <FaStop size={12} />
                      停止
                    </button>
                  )}

                  <button
                    onClick={() => {
                      setShowPreview(true);
                      start(`${API_BASE}/api/eval/dashboard?project_id=${projectId}`)
                    }}
                    className="h-9 px-4 flex items-center gap-2 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white rounded-lg text-sm font-medium transition-all shadow-sm hover:shadow-md"
                    title="评估面板"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    评估
                  </button>

                  {/* Publish/Update - Temporarily Disabled */}
                  {showPreview && previewUrl && (
                    <div className="relative group">
                      <button
                        disabled
                        className="h-9 flex items-center gap-2 px-3 bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 rounded-lg text-sm font-medium cursor-not-allowed border border-gray-300 dark:border-gray-600 opacity-60"
                        title="发布功能暂时不可用"
                      >
                        <FaRocket size={14} />
                        发布
                      </button>

                      {false && showPublishPanel && (
                        <div className="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-900 rounded-xl shadow-xl border border-gray-200 dark:border-gray-700 z-50 p-5">
                          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Publish Project</h3>

                          {/* Deployment Status Display */}
                          {deploymentStatus === 'deploying' && (
                            <div className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                              <div className="flex items-center gap-2 mb-2">
                                <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                                <p className="text-sm font-medium text-blue-700 dark:text-blue-400">Deployment in progress...</p>
                              </div>
                              <p className="text-xs text-blue-600 dark:text-blue-300">Building and deploying your project. This may take a few minutes.</p>
                            </div>
                          )}

                          {deploymentStatus === 'ready' && publishedUrl && (
                            <div className="mb-4 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                              <p className="text-sm font-medium text-green-700 dark:text-green-400 mb-2">Currently published at:</p>
                              <a
                                href={publishedUrl || undefined}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-sm text-green-600 dark:text-green-300 font-mono hover:underline break-all"
                              >
                                {publishedUrl}
                              </a>
                            </div>
                          )}

                          {deploymentStatus === 'error' && (
                            <div className="mb-4 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
                              <p className="text-sm font-medium text-red-700 dark:text-red-400 mb-2">Deployment failed</p>
                              <p className="text-xs text-red-600 dark:text-red-300">There was an error during deployment. Please try again.</p>
                            </div>
                          )}

                          <div className="space-y-4">
                            {!githubConnected || !vercelConnected ? (
                              <div className="p-4 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-800">
                                <p className="text-sm font-medium text-gray-900 dark:text-white mb-3">To publish, connect the following services:</p>
                                <div className="space-y-2">
                                  {!githubConnected && (
                                    <div className="flex items-center gap-2 text-amber-700 dark:text-amber-400">
                                      <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                                      </svg>
                                      <span className="text-sm">GitHub repository not connected</span>
                                    </div>
                                  )}
                                  {!vercelConnected && (
                                    <div className="flex items-center gap-2 text-amber-700 dark:text-amber-400">
                                      <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                                      </svg>
                                      <span className="text-sm">Vercel project not connected</span>
                                    </div>
                                  )}
                                </div>
                                <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">
                                  Go to
                                  <button
                                    onClick={() => {
                                      setShowPublishPanel(false);
                                      setShowGlobalSettings(true);
                                    }}
                                    className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 dark:hover:text-indigo-300 underline font-medium mx-1"
                                  >
                                    Settings → Service Integrations
                                  </button>
                                  to connect.
                                </p>
                              </div>
                            ) : null}

                            <button
                              disabled={publishLoading || deploymentStatus === 'deploying' || !githubConnected || !vercelConnected}
                              onClick={async () => {
                                setPublishLoading(true);
                                try {
                                  // Push to GitHub
                                  console.log('🚀 Pushing to GitHub...');
                                  const pushRes = await fetch(`${API_BASE}/api/projects/${projectId}/github/push`, { method: 'POST' });
                                  if (!pushRes.ok) {
                                    const errorText = await pushRes.text();
                                    console.error('🚀 GitHub push failed:', errorText);
                                    throw new Error(errorText);
                                  }

                                  // Deploy to Vercel
                                  console.log('🚀 Deploying to Vercel...');
                                  const deployUrl = `${API_BASE}/api/projects/${projectId}/vercel/deploy`;

                                  const vercelRes = await fetch(deployUrl, {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ branch: 'main' })
                                  });
                                  if (!vercelRes.ok) {
                                    const responseText = await vercelRes.text();
                                    console.error('🚀 Vercel deploy failed:', responseText);
                                  }
                                  if (vercelRes.ok) {
                                    const data = await vercelRes.json();
                                    console.log('🚀 Deployment started, polling for status...');

                                    // Set deploying status BEFORE ending publishLoading to prevent gap
                                    setDeploymentStatus('deploying');

                                    if (data.deployment_id) {
                                      startDeploymentPolling(data.deployment_id);
                                    }

                                    // Only set URL if deployment is already ready
                                    if (data.ready && data.deployment_url) {
                                      const url = data.deployment_url.startsWith('http') ? data.deployment_url : `https://${data.deployment_url}`;
                                      setPublishedUrl(url);
                                      setDeploymentStatus('ready');
                                    }
                                  } else {
                                    const errorText = await vercelRes.text();
                                    console.error('🚀 Vercel deploy failed:', vercelRes.status, errorText);
                                    // if Vercel not connected, just close
                                    setDeploymentStatus('idle');
                                    setPublishLoading(false); // 即使 Vercel 部署失败也停止加载
                                  }
                                  // Keep panel open to show deployment progress
                                } catch (e) {
                                  console.error('🚀 Publish failed:', e);
                                  alert('Publish failed. Check Settings and tokens.');
                                  setDeploymentStatus('idle');
                                  setPublishLoading(false); // 发生错误时停止加载
                                  // Close panel after error
                                  setTimeout(() => {
                                    setShowPublishPanel(false);
                                  }, 1000);
                                } finally {
                                  loadDeployStatus();
                                }
                              }}
                              className={`w-full px-4 py-3 rounded-lg font-medium text-white transition-colors ${publishLoading || deploymentStatus === 'deploying' || !githubConnected || !vercelConnected
                                ? 'bg-gray-400 dark:bg-gray-600 cursor-not-allowed'
                                : 'bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600'
                                }`}
                            >
                              {publishLoading
                                ? 'Publishing...'
                                : deploymentStatus === 'deploying'
                                  ? 'Deploying...'
                                  : !githubConnected || !vercelConnected
                                    ? 'Connect Services First'
                                    : deploymentStatus === 'ready' && publishedUrl ? 'Update' : 'Publish'
                              }
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>

              {/* Content Area */}
              <div className="flex-1 relative bg-black overflow-hidden">
                <AnimatePresence mode="wait">
                  {showPreview ? (
                    <MotionDiv
                      key="preview"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      style={{ height: '100%' }}
                    >
                      {previewUrl ? (
                        <div className="relative w-full h-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                          <div
                            className={`bg-white dark:bg-gray-900 ${deviceMode === 'mobile'
                              ? 'w-[375px] h-[667px] rounded-[25px] border-8 border-gray-800 shadow-2xl'
                              : 'w-full h-full'
                              } overflow-hidden`}
                          >
                            <iframe
                              ref={iframeRef}
                              className="w-full h-full border-none bg-white dark:bg-gray-800"
                              src={previewUrl}
                              onError={() => {
                                // Show error overlay
                                const overlay = document.getElementById('iframe-error-overlay');
                                if (overlay) overlay.style.display = 'flex';
                              }}
                              onLoad={() => {
                                // Hide error overlay when loaded successfully
                                const overlay = document.getElementById('iframe-error-overlay');
                                if (overlay) overlay.style.display = 'none';
                              }}
                            />

                            {/* Error overlay */}
                            <div
                              id="iframe-error-overlay"
                              className="absolute inset-0 bg-gray-50 dark:bg-gray-900 flex items-center justify-center z-10"
                              style={{ display: 'none' }}
                            >
                              <div className="text-center max-w-md mx-auto p-6">
                                <div className="text-4xl mb-4">🔄</div>
                                <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
                                  Connection Issue
                                </h3>
                                <p className="text-gray-600 dark:text-gray-400 mb-4">
                                  The preview couldn't load properly. Try clicking the refresh button to reload the page.
                                </p>
                                <button
                                  className="flex items-center gap-2 mx-auto px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
                                  onClick={() => {
                                    const iframe = document.querySelector('iframe');
                                    if (iframe) {
                                      iframe.src = iframe.src;
                                    }
                                    const overlay = document.getElementById('iframe-error-overlay');
                                    if (overlay) overlay.style.display = 'none';
                                  }}
                                >
                                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M1 4v6h6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                  </svg>
                                  Refresh Now
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      ) : (
                        <div className="h-full w-full flex items-center justify-center bg-gray-50 dark:bg-black relative">
                          {/* Gradient background similar to main page */}
                          <div className="absolute inset-0">
                            <div className="absolute inset-0 bg-white dark:bg-black" />
                            <div
                              className="absolute inset-0 dark:block hidden transition-all duration-1000 ease-in-out"
                              style={{
                                background: `radial-gradient(circle at 50% 100%, 
                            ${assistantBrandColors[preferredCli] || assistantBrandColors.claude}66 0%, 
                            ${assistantBrandColors[preferredCli] || assistantBrandColors.claude}4D 25%, 
                            ${assistantBrandColors[preferredCli] || assistantBrandColors.claude}33 50%, 
                            transparent 70%)`
                              }}
                            />
                            {/* Light mode gradient - subtle */}
                            <div
                              className="absolute inset-0 block dark:hidden transition-all duration-1000 ease-in-out"
                              style={{
                                background: `radial-gradient(circle at 50% 100%, 
                            ${assistantBrandColors[preferredCli] || assistantBrandColors.claude}40 0%, 
                            ${assistantBrandColors[preferredCli] || assistantBrandColors.claude}26 25%, 
                            transparent 50%)`
                              }}
                            />
                          </div>

                          {/* Content with z-index to be above gradient */}
                          <div className="relative z-10 w-full h-full flex items-center justify-center">
                            {isStartingPreview ? (
                              <MotionDiv
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="text-center"
                              >
                                {/* Claudable Symbol with loading spinner */}
                                <div className="w-40 h-40 mx-auto mb-6 relative">
                                  <div
                                    className="w-full h-full"
                                    style={{
                                      backgroundColor: assistantBrandColors[preferredCli] || assistantBrandColors.claude,
                                      mask: `url(${symbol_white_icon}) no-repeat center/contain`,
                                      WebkitMask: `url(${symbol_white_icon}) no-repeat center/contain`,
                                      opacity: 0.9
                                    }}
                                  />

                                  {/* Loading spinner in center */}
                                  <div className="absolute inset-0 flex items-center justify-center">
                                    <div
                                      className="w-14 h-14 border-4 border-t-transparent rounded-full animate-spin"
                                      style={{
                                        borderColor: assistantBrandColors[preferredCli] || assistantBrandColors.claude,
                                        borderTopColor: 'transparent'
                                      }}
                                    />
                                  </div>
                                </div>

                                {/* Content */}
                                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                                  正在启动预览服务器
                                </h3>

                                <div className="flex items-center justify-center gap-1 text-gray-600 dark:text-gray-400">
                                  <span>{previewInitializationMessage}</span>
                                  <MotionDiv
                                    className="flex gap-1 ml-2"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                  >
                                    <MotionDiv
                                      animate={{ opacity: [0, 1, 0] }}
                                      transition={{ duration: 1.5, repeat: Infinity, delay: 0 }}
                                      className="w-1 h-1 bg-gray-600 dark:bg-gray-400 rounded-full"
                                    />
                                    <MotionDiv
                                      animate={{ opacity: [0, 1, 0] }}
                                      transition={{ duration: 1.5, repeat: Infinity, delay: 0.3 }}
                                      className="w-1 h-1 bg-gray-600 dark:bg-gray-400 rounded-full"
                                    />
                                    <MotionDiv
                                      animate={{ opacity: [0, 1, 0] }}
                                      transition={{ duration: 1.5, repeat: Infinity, delay: 0.6 }}
                                      className="w-1 h-1 bg-gray-600 dark:bg-gray-400 rounded-full"
                                    />
                                  </MotionDiv>
                                </div>
                              </MotionDiv>
                            ) : (
                              <div className="text-center">
                                <MotionDiv
                                  initial={{ opacity: 0, y: 20 }}
                                  animate={{ opacity: 1, y: 0 }}
                                  transition={{ duration: 0.6, ease: "easeOut" }}
                                >
                                  {/* Claudable Symbol */}
                                  {hasActiveRequests ? (
                                    <>
                                      <div className="w-40 h-40 mx-auto mb-6 relative">
                                        <MotionDiv
                                          animate={{ rotate: 360 }}
                                          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                                          style={{ transformOrigin: "center center" }}
                                          className="w-full h-full"
                                        >
                                          <div
                                            className="w-full h-full"
                                            style={{
                                              backgroundColor: assistantBrandColors[preferredCli] || assistantBrandColors.claude,
                                              mask: `url(${symbol_white_icon}) no-repeat center/contain`,
                                              WebkitMask: `url(${symbol_white_icon}) no-repeat center/contain`,
                                              opacity: 0.9
                                            }}
                                          />
                                        </MotionDiv>
                                      </div>

                                      <h3 className="text-2xl font-bold mb-3 relative overflow-hidden inline-block">
                                        <span
                                          className="relative"
                                          style={{
                                            background: `linear-gradient(90deg, 
                                          #6b7280 0%, 
                                          #6b7280 30%, 
                                          #ffffff 50%, 
                                          #6b7280 70%, 
                                          #6b7280 100%)`,
                                            backgroundSize: '200% 100%',
                                            WebkitBackgroundClip: 'text',
                                            backgroundClip: 'text',
                                            WebkitTextFillColor: 'transparent',
                                            animation: 'shimmerText 5s linear infinite'
                                          }}
                                        >
                                          Building...
                                        </span>
                                      </h3>
                                    </>
                                  ) : (
                                    <>
                                      <div
                                        onClick={!isRunning && !isStartingPreview ? () => start() : undefined}
                                        className={`w-40 h-40 mx-auto mb-6 relative ${!isRunning && !isStartingPreview ? 'cursor-pointer group' : ''}`}
                                      >
                                        {/* Claudable Symbol with rotating animation when starting */}
                                        <MotionDiv
                                          className="w-full h-full"
                                          animate={isStartingPreview ? { rotate: 360 } : {}}
                                          transition={{ duration: 6, repeat: isStartingPreview ? Infinity : 0, ease: "linear" }}
                                        >
                                          <div
                                            className="w-full h-full"
                                            style={{
                                              backgroundColor: assistantBrandColors[preferredCli] || assistantBrandColors.claude,
                                              mask: `url(${symbol_white_icon}) no-repeat center/contain`,
                                              WebkitMask: `url(${symbol_white_icon}) no-repeat center/contain`,
                                              opacity: 0.9
                                            }}
                                          />
                                        </MotionDiv>

                                        {/* Icon in Center - Play or Loading */}
                                        <div className="absolute inset-0 flex items-center justify-center">
                                          {isStartingPreview ? (
                                            <div
                                              className="w-14 h-14 border-4 border-t-transparent rounded-full animate-spin"
                                              style={{
                                                borderColor: assistantBrandColors[preferredCli] || assistantBrandColors.claude,
                                                borderTopColor: 'transparent'
                                              }}
                                            />
                                          ) : (
                                            <MotionDiv
                                              className="flex items-center justify-center"
                                              whileHover={{ scale: 1.2 }}
                                              whileTap={{ scale: 0.9 }}
                                            >
                                              <FaPlay
                                                size={32}
                                              />
                                            </MotionDiv>
                                          )}
                                        </div>
                                      </div>

                                      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                                        预览项目
                                      </h3>

                                      <p className="text-gray-600 dark:text-gray-400 max-w-lg mx-auto">
                                        启动您的开发项目查看
                                      </p>
                                    </>
                                  )}
                                </MotionDiv>
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </MotionDiv>
                  ) : (
                    <MotionDiv
                      key="code"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="h-full flex bg-white dark:bg-gray-950"
                    >
                      {/* Left Sidebar - File Explorer (VS Code style) - 可调整宽度 */}
                      <Resizable
                        defaultSize={{
                          width: 256,
                          height: '100%'
                        }}
                        minWidth={200}
                        maxWidth={500}
                        enable={{
                          top: false,
                          right: true,
                          bottom: false,
                          left: false,
                          topRight: false,
                          bottomRight: false,
                          bottomLeft: false,
                          topLeft: false
                        }}
                        handleStyles={{
                          right: {
                            width: '8px',
                            right: '-4px',
                            cursor: 'ew-resize',
                          }
                        }}
                        handleClasses={{
                          right: 'fileTreeResizeHandle'
                        }}
                     
                        className="h-full border-r border-gray-200 dark:border-gray-800 flex flex-col"
                      >
                        {/* File Tree */}
                        <div className="flex-1 overflow-y-auto bg-gray-50 dark:bg-[#0a0a0a] custom-scrollbar">
                          {!tree || tree.length === 0 ? (
                            <div className="px-3 py-8 text-center text-[11px] text-gray-600 dark:text-[#6a6a6a] select-none">
                              No files found
                            </div>
                          ) : (
                            <TreeView
                              entries={tree || []}
                              selectedFile={selectedFile}
                              expandedFolders={expandedFolders}
                              folderContents={folderContents}
                              loadingFolders={loadingFolders}
                              onToggleFolder={toggleFolder}
                              onSelectFile={openFile}
                              onLoadFolder={handleLoadFolder}
                              level={0}
                              parentPath=""
                              getFileIcon={getFileIcon}
                            />
                          )}
                        </div>
                      </Resizable>

                      {/* Right Editor Area */}
                      <div className="flex-1 flex flex-col bg-white dark:bg-[#0d0d0d] min-w-0">
                        {selectedFile ? (
                          <>
                            {/* File Tab */}
                            <div className="flex-shrink-0 bg-gray-100 dark:bg-[#1a1a1a]">
                              <div className="flex items-center">
                                <div className="flex items-center gap-2 bg-white dark:bg-[#0d0d0d] px-3 py-1.5 border-t-2 border-t-blue-500 dark:border-t-[#007acc]">
                                  <span className="w-4 h-4 flex items-center justify-center">
                                    {getFileIcon(tree.find(e => e.path === selectedFile) || { path: selectedFile, type: 'file' })}
                                  </span>
                                  <span className="text-[13px] text-gray-700 dark:text-[#cccccc]" style={{ fontFamily: "'Segoe UI', Tahoma, sans-serif" }}>
                                    {getFileNameFromPath(selectedFile)}
                                  </span>
                                  {isFileUpdating && (
                                    <span className="text-[11px] text-green-600 dark:text-green-400 ml-auto mr-2">
                                      Updated
                                    </span>
                                  )}
                                  <button
                                    className="text-gray-700 dark:text-[#cccccc] hover:bg-gray-200 dark:hover:bg-[#383838] ml-2 px-1 rounded"
                                    onClick={() => {
                                      setSelectedFile('');
                                      setContent('');
                                    }}
                                  >
                                    ×
                                  </button>
                                </div>
                              </div>
                            </div>

                            {/* Code Editor with Virtual Scrolling */}
                            <div className="flex-1 overflow-hidden">
                              <VirtualCodeEditor
                                content={content || ''}
                                language={getFileLanguage(selectedFile)}
                                hljs={hljs}
                                lineHeight={19}
                                overscan={20}
                                filePath={selectedFile}
                                projectId={projectId}
                              />
                            </div>
                          </>
                        ) : (
                          /* Welcome Screen */
                          <div className="flex-1 flex items-center justify-center bg-white dark:bg-[#0d0d0d]">
                            <div className="text-center">
                              <span className="w-16 h-16 mb-4 opacity-10 text-gray-400 dark:text-[#3c3c3c] mx-auto flex items-center justify-center"><FaCode size={64} /></span>
                              <h3 className="text-lg font-medium text-gray-700 dark:text-[#cccccc] mb-2">
                                欢迎使用
                              </h3>
                              <p className="text-sm text-gray-500 dark:text-[#858585]">
                                从资源管理器中选择一个文件以开始查看
                              </p>
                            </div>
                          </div>
                        )}
                      </div>
                    </MotionDiv>
                  )}
                </AnimatePresence>
              </div>
            </div>
          </div>
        </div>
      </div>


      {/* Publish Modal */}
      {showPublishPanel && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/50" onClick={() => setShowPublishPanel(false)} />
          <div className="relative w-full max-w-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl shadow-2xl overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between bg-gray-50/60 dark:bg-white/5">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white bg-black border border-black/10 dark:border-white/10">
                  <FaRocket size={14} />
                </div>
                <div>
                  <h3 className="text-base font-semibold text-gray-900 dark:text-white">发布项目</h3>
                  <p className="text-xs text-gray-600 dark:text-gray-400">使用 Vercel 部署，关联到您的 GitHub 仓库</p>
                </div>
              </div>
              <button onClick={() => setShowPublishPanel(false)} className="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /></svg>
              </button>
            </div>

            <div className="p-6 space-y-4">
              {deploymentStatus === 'deploying' && (
                <div className="p-4 rounded-xl border border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20">
                  <div className="flex items-center gap-2 mb-1">
                    <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                    <p className="text-sm font-medium text-blue-700 dark:text-blue-400">部署进行中…</p>
                  </div>
                  <p className="text-xs text-blue-700/80 dark:text-blue-300/80">正在构建和部署您的项目。这可能需要几分钟时间。</p>
                </div>
              )}

              {deploymentStatus === 'ready' && publishedUrl && (
                <div className="p-4 rounded-xl border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20">
                  <p className="text-sm font-medium text-emerald-700 dark:text-emerald-400 mb-2">发布成功</p>
                  <div className="flex items-center gap-2">
                    <a href={publishedUrl} target="_blank" rel="noopener noreferrer" className="text-sm font-mono text-emerald-700 dark:text-emerald-300 underline break-all flex-1">
                      {publishedUrl}
                    </a>
                    <button
                      onClick={() => navigator.clipboard?.writeText(publishedUrl)}
                      className="px-2 py-1 text-xs rounded-lg border border-emerald-300/80 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100 dark:hover:bg-emerald-900/30"
                    >
                      复制
                    </button>
                  </div>
                </div>
              )}

              {deploymentStatus === 'error' && (
                <div className="p-4 rounded-xl border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20">
                  <p className="text-sm font-medium text-red-700 dark:text-red-400">部署失败，请重试。</p>
                </div>
              )}

              {!githubConnected || !vercelConnected ? (
                <div className="p-4 rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20">
                  <p className="text-sm font-medium text-gray-900 dark:text-white mb-2">请连接以下服务：</p>
                  <div className="space-y-1 text-amber-700 dark:text-amber-400 text-sm">
                    {!githubConnected && (<div className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-amber-500" />GitHub 仓库未连接</div>)}
                    {!vercelConnected && (<div className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-amber-500" />Vercel 项目未连接</div>)}
                  </div>
                  <button
                    className="mt-3 w-full px-4 py-2 rounded-xl border border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-white/5"
                    onClick={() => { setShowPublishPanel(false); setShowGlobalSettings(true); }}
                  >
                    打开设置 → 服务
                  </button>
                </div>
              ) : null}

              <button
                disabled={publishLoading || deploymentStatus === 'deploying' || !githubConnected || !vercelConnected}
                onClick={async () => {
                  try {
                    setPublishLoading(true);
                    setDeploymentStatus('deploying');
                    // 1) Push to GitHub to ensure branch/commit exists
                    try {
                      const pushRes = await fetch(`${API_BASE}/api/projects/${projectId}/github/push`, { method: 'POST' });
                      if (!pushRes.ok) {
                        const err = await pushRes.text();
                        console.error('🚀 GitHub push failed:', err);
                        throw new Error(err);
                      }
                    } catch (e) {
                      console.error('🚀 GitHub push step failed', e);
                      throw e;
                    }
                    // Small grace period to let GitHub update default branch
                    await new Promise(r => setTimeout(r, 800));
                    // 2) Deploy to Vercel (branch auto-resolved on server)
                    const deployUrl = `${API_BASE}/api/projects/${projectId}/vercel/deploy`;
                    const vercelRes = await fetch(deployUrl, {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ branch: 'main' })
                    });
                    if (vercelRes.ok) {
                      const data = await vercelRes.json();
                      setDeploymentStatus('deploying');
                      if (data.deployment_id) startDeploymentPolling(data.deployment_id);
                      if (data.ready && data.deployment_url) {
                        const url = data.deployment_url.startsWith('http') ? data.deployment_url : `https://${data.deployment_url}`;
                        setPublishedUrl(url);
                        setDeploymentStatus('ready');
                      }
                    } else {
                      const errorText = await vercelRes.text();
                      console.error('🚀 Vercel deploy failed:', vercelRes.status, errorText);
                      setDeploymentStatus('idle');
                      setPublishLoading(false);
                    }
                  } catch (e) {
                    console.error('🚀 Publish failed:', e);
                    alert('Publish failed. Check Settings and tokens.');
                    setDeploymentStatus('idle');
                    setPublishLoading(false);
                    setTimeout(() => setShowPublishPanel(false), 1000);
                  } finally {
                    loadDeployStatus();
                  }
                }}
                className={`w-full px-4 py-3 rounded-xl font-medium text-white transition ${publishLoading || deploymentStatus === 'deploying' || !githubConnected || !vercelConnected
                  ? 'bg-gray-400 dark:bg-gray-600 cursor-not-allowed'
                  : 'bg-black hover:bg-gray-900'
                  }`}
              >
                {publishLoading ? '发布中…' : deploymentStatus === 'deploying' ? '部署中…' : (!githubConnected || !vercelConnected) ? '请先连接服务' : (deploymentStatus === 'ready' && publishedUrl ? '更新' : '发布')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Project Settings Modal */}
      <ProjectSettings
        isOpen={showGlobalSettings}
        onClose={() => setShowGlobalSettings(false)}
        projectId={projectId}
        projectName={projectName}
        initialTab="general"
      />
    </>
  );
}
