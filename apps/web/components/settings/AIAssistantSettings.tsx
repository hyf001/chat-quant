/**
 * AI Assistant Settings Component
 * Display current AI CLI and model (read-only)
 */
import React from 'react';
import { useCLI } from '@/hooks/useCLI';

interface AIAssistantSettingsProps {
  projectId: string;
}

export function AIAssistantSettings({ projectId }: AIAssistantSettingsProps) {
  const { cliOptions, preference } = useCLI({ projectId });

  const selectedCLIOption = cliOptions.find(opt => opt.id === preference?.preferred_cli);
  
  // Debug logging
  console.log('🔍 AIAssistantSettings Debug:', {
    projectId,
    preference,
    selectedCLIOption,
    cliOptions
  });
  
  // Get the actual model name from preference data
  const getModelDisplayName = () => {
    if (!preference?.selected_model) return '默认模型';

    // Find the model name from the CLI options
    const currentCLI = selectedCLIOption;
    if (currentCLI?.models) {
      const model = currentCLI.models.find(m => m.id === preference.selected_model);
      console.log('🔍 Model search:', {
        selected_model: preference.selected_model,
        available_models: currentCLI.models,
        found_model: model
      });
      return model?.name || preference.selected_model;
    }

    return preference.selected_model;
  };
  
  const modelDisplayName = getModelDisplayName();

  return (
    <div className="p-6 space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          当前 AI 助手
        </h3>

        <div className="space-y-4">
          {/* Current CLI */}
          <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  CLI Agent
                </h4>
                <div className="flex items-center gap-2">
                  <span className="text-lg font-semibold text-gray-900 dark:text-white">
                    {selectedCLIOption?.name || preference?.preferred_cli || '未配置'}
                  </span>
                 
                </div>
              </div>
            </div>
          </div>

          {/* Current Model */}
          <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              模型
            </h4>
            <span className="text-lg font-semibold text-gray-900 dark:text-white">
              {modelDisplayName}
            </span>
          </div>


        </div>
      </div>
    </div>
  );
}