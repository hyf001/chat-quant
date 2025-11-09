"use client";
import { motion } from 'framer-motion';

interface PermissionBlockModalProps {
  isOpen: boolean;
}

export default function PermissionBlockModal({ isOpen }: PermissionBlockModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-[9999]">
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 p-8 w-full max-w-md">
          {/* Warning Icon */}
          <div className="flex items-center justify-center w-16 h-16 mx-auto mb-6 bg-red-100 dark:bg-red-900/30 rounded-full">
            <svg
              className="w-10 h-10 text-red-600 dark:text-red-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
              />
            </svg>
          </div>

          {/* Title */}
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white text-center mb-4">
            访问受限
          </h3>

          {/* Description */}
          <div className="text-center space-y-3 mb-6">
            <p className="text-gray-700 dark:text-gray-300 text-lg">
              当前用户没有权限访问此系统
            </p>
            <p className="text-gray-600 dark:text-gray-400">
              请联系 <span className="font-semibold text-red-600 dark:text-red-400">CBAS人员</span> 获取访问权限
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
