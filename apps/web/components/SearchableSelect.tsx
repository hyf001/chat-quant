'use client';

import React, { useState, useRef, useEffect } from 'react';

interface SearchableSelectProps {
  options: string[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  className?: string;
  width?: string;
}

export default function SearchableSelect({
  options,
  value,
  onChange,
  placeholder = '请选择',
  className = '',
  width = '250px'
}: SearchableSelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const selectRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (selectRef.current && !selectRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setSearchQuery('');
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Filter options based on search query
  const filteredOptions = searchQuery.trim()
    ? options.filter(option =>
        option.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : options;

  const handleToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!isOpen) {
      setIsOpen(true);
      setSearchQuery('');
      // Focus input when opening
      setTimeout(() => {
        inputRef.current?.focus();
      }, 0);
    }
  };

  const handleInputClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!isOpen) {
      setIsOpen(true);
      setSearchQuery('');
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
    if (!isOpen) {
      setIsOpen(true);
    }
  };

  const handleOptionClick = (option: string, e: React.MouseEvent) => {
    e.stopPropagation();
    onChange(option);
    setIsOpen(false);
    setSearchQuery('');
  };

  return (
    <div ref={selectRef} className={`relative ${className}`} style={{ width }}>
      {/* Select Input */}
      <div
        className="h-9 px-3 bg-white dark:bg-gray-800 text-sm border border-gray-300 dark:border-gray-600 rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors flex items-center justify-between"
        onClick={handleToggle}
      >
        <input
          ref={inputRef}
          type="text"
          value={isOpen ? searchQuery : (value || '')}
          onChange={handleInputChange}
          onClick={handleInputClick}
          placeholder={placeholder}
          readOnly={!isOpen}
          className="bg-transparent text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 outline-none flex-1 cursor-pointer"
        />
        <svg
          className={`w-4 h-4 text-gray-500 transition-transform flex-shrink-0 ml-2 ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg max-h-60 overflow-y-auto z-50">
          {filteredOptions.length > 0 ? (
            filteredOptions.map((option, index) => (
              <div
                key={index}
                onClick={(e) => handleOptionClick(option, e)}
                onMouseDown={(e) => e.preventDefault()}
                className={`px-3 py-2 text-sm cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors ${
                  option === value
                    ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 font-medium'
                    : 'text-gray-900 dark:text-gray-100'
                }`}
              >
                {option}
              </div>
            ))
          ) : (
            <div className="px-3 py-2 text-sm text-gray-500 dark:text-gray-400 text-center">
              没有找到匹配项
            </div>
          )}
        </div>
      )}
    </div>
  );
}
