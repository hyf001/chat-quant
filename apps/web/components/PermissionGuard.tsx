"use client";
import { useEffect, useState } from 'react';
import PermissionBlockModal from './PermissionBlockModal';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8080';
export default function PermissionGuard({ children }: { children: React.ReactNode }) {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);

  useEffect(() => {
    // Mock 权限检查接口
    const checkPermission = async () => {
      try {
        // 模拟 API 调用延迟
        const res = await fetch(`${API_BASE}/api/auth/check`)

        let mockResponse = {
          has_permission: false,
          message: '当前用户没有权限，请联系CBAS人员'
        };
        if (res.ok) {
          const resData = await res.json()
          if (resData?.authorized) {
            mockResponse = {
              has_permission: true,
              message: '访问已授权'
            }
          }
        }
        if(process.env.NODE_ENV === 'development') {
          mockResponse = {
            has_permission: true,
            message: '访问已授权'
          }
        }
        setHasPermission(mockResponse.has_permission);
      } catch (error) {
        console.error('权限检查失败:', error);
        // 出错时默认无权限
        setHasPermission(false);
      }
    };

    checkPermission();
  }, []);

  // 加载中状态
  if (hasPermission === null) {
    return (
      <div className="fixed inset-0 bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">正在验证权限...</p>
        </div>
      </div>
    );
  }

  // 无权限时显示不可关闭的弹窗
  if (!hasPermission) {
    return (
      <>
        {children}
        <PermissionBlockModal isOpen={true} />
      </>
    );
  }

  // 有权限时正常显示
  return <>{children}</>;
}
