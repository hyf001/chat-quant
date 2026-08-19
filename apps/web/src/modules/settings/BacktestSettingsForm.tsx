import { Loader2, RefreshCw, Save } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

import { Button } from "@/components/ui/button";

import {
  listDatasets,
  queryDatasets,
  type AppSettings,
  type BacktestSettings,
  type Dataset,
} from "../../shared/api";
import { FormSection, SelectField } from "./SettingsFields";

type BacktestSettingsFormProps = {
  draft: AppSettings;
  onChange: (settings: AppSettings) => void;
  onSaveBacktestSettings: (settings: Partial<BacktestSettings>, message: string) => void;
  onToast: (message: string, tone?: "success" | "error" | "info") => void;
};

export function BacktestSettingsForm({
  draft,
  onChange,
  onSaveBacktestSettings,
  onToast,
}: BacktestSettingsFormProps) {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [marketColumns, setMarketColumns] = useState<string[]>([]);
  const [benchmarkColumns, setBenchmarkColumns] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingMarketColumns, setIsLoadingMarketColumns] = useState(false);
  const [isLoadingBenchmarkColumns, setIsLoadingBenchmarkColumns] = useState(false);
  const backtest = draft.backtest;
  const datasetOptions = useMemo(
    () =>
      datasets.map((dataset) => ({
        value: dataset.id,
        label: `${dataset.name_zh || dataset.description || dataset.name} · ${dataset.name}`,
      })),
    [datasets],
  );

  const loadDatasets = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await listDatasets();
      setDatasets(response.datasets);
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "数据集加载失败", "error");
    } finally {
      setIsLoading(false);
    }
  }, [onToast]);

  useEffect(() => {
    void loadDatasets();
  }, [loadDatasets]);

  const loadDatasetColumns = useCallback(async (
    datasetId: string,
    setColumns: (columns: string[]) => void,
    setLoading: (loading: boolean) => void,
  ) => {
    const dataset = datasets.find((item) => item.id === datasetId);
    if (!dataset) {
      setColumns([]);
      return;
    }
    setLoading(true);
    try {
      const response = await queryDatasets({
        sql: `SELECT * FROM ${quoteDuckdbIdentifier(dataset.name)} LIMIT 0`,
        page: 1,
        page_size: 1,
      });
      setColumns(response.columns.map((column) => column.name));
    } catch (caught) {
      setColumns([]);
      onToast(caught instanceof Error ? caught.message : "字段列表加载失败", "error");
    } finally {
      setLoading(false);
    }
  }, [datasets, onToast]);

  useEffect(() => {
    void loadDatasetColumns(
      backtest.market_dataset.dataset_id,
      setMarketColumns,
      setIsLoadingMarketColumns,
    );
  }, [backtest.market_dataset.dataset_id, loadDatasetColumns]);

  useEffect(() => {
    void loadDatasetColumns(
      backtest.benchmark_dataset.dataset_id,
      setBenchmarkColumns,
      setIsLoadingBenchmarkColumns,
    );
  }, [backtest.benchmark_dataset.dataset_id, loadDatasetColumns]);

  useEffect(() => {
    if (isLoadingMarketColumns || marketColumns.length === 0) {
      return;
    }
    const sanitized = sanitizeMarketDatasetFields(backtest.market_dataset, marketColumns);
    if (sanitized !== backtest.market_dataset) {
      updateMarket(sanitized);
    }
  }, [backtest.market_dataset, isLoadingMarketColumns, marketColumns]);

  useEffect(() => {
    if (isLoadingBenchmarkColumns || benchmarkColumns.length === 0) {
      return;
    }
    const sanitized = sanitizeBenchmarkDatasetFields(
      backtest.benchmark_dataset,
      benchmarkColumns,
    );
    if (sanitized !== backtest.benchmark_dataset) {
      updateBenchmark(sanitized);
    }
  }, [backtest.benchmark_dataset, benchmarkColumns, isLoadingBenchmarkColumns]);

  const updateBacktest = (patch: Partial<BacktestSettings>) => {
    onChange({
      ...draft,
      backtest: {
        ...backtest,
        ...patch,
      },
    });
  };
  const updateMarket = (patch: Partial<BacktestSettings["market_dataset"]>) => {
    updateBacktest({
      market_dataset: {
        ...backtest.market_dataset,
        ...patch,
      },
    });
  };
  const updateBenchmark = (patch: Partial<BacktestSettings["benchmark_dataset"]>) => {
    updateBacktest({
      benchmark_dataset: {
        ...backtest.benchmark_dataset,
        ...patch,
      },
    });
  };

  return (
    <div className="grid gap-5">
      <div className="flex flex-wrap items-center justify-between gap-2 rounded-md border border-line bg-soft px-3 py-2">
        <div className="text-xs text-mutedText">Backtrader 回测只从平台数据集读取行情和基准。</div>
        <Button
          size="sm"
          variant="outline"
          type="button"
          disabled={isLoading}
          onClick={() => void loadDatasets()}
        >
          {isLoading ? (
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
          ) : (
            <RefreshCw className="h-3.5 w-3.5" />
          )}
          刷新
        </Button>
      </div>

      <FormSection
        title="行情数据集"
        action={
          <SaveButton
            label="保存行情配置"
            onClick={() =>
              onSaveBacktestSettings(
                { market_dataset: normalizeMarketDataset(backtest.market_dataset) },
                "回测行情数据集已保存",
              )
            }
          />
        }
      >
        <SelectField
          label="数据集"
          value={backtest.market_dataset.dataset_id}
          options={datasetOptions}
          placeholder="选择数据集"
          onChange={(dataset_id) => updateMarket(emptyMarketFieldPatch(dataset_id))}
        />
        <FieldSelect
          label="代码字段"
          value={backtest.market_dataset.symbol_field}
          columns={marketColumns}
          isLoading={isLoadingMarketColumns}
          onChange={(symbol_field) => updateMarket({ symbol_field })}
        />
        <FieldSelect
          label="日期字段"
          value={backtest.market_dataset.datetime_field}
          columns={marketColumns}
          isLoading={isLoadingMarketColumns}
          onChange={(datetime_field) => updateMarket({ datetime_field })}
        />
        <FieldSelect
          label="开盘字段"
          value={backtest.market_dataset.open_field}
          columns={marketColumns}
          isLoading={isLoadingMarketColumns}
          onChange={(open_field) => updateMarket({ open_field })}
        />
        <FieldSelect
          label="最高字段"
          value={backtest.market_dataset.high_field}
          columns={marketColumns}
          isLoading={isLoadingMarketColumns}
          onChange={(high_field) => updateMarket({ high_field })}
        />
        <FieldSelect
          label="最低字段"
          value={backtest.market_dataset.low_field}
          columns={marketColumns}
          isLoading={isLoadingMarketColumns}
          onChange={(low_field) => updateMarket({ low_field })}
        />
        <FieldSelect
          label="收盘字段"
          value={backtest.market_dataset.close_field}
          columns={marketColumns}
          isLoading={isLoadingMarketColumns}
          onChange={(close_field) => updateMarket({ close_field })}
        />
        <FieldSelect
          label="成交量字段"
          value={backtest.market_dataset.volume_field}
          columns={marketColumns}
          isLoading={isLoadingMarketColumns}
          onChange={(volume_field) => updateMarket({ volume_field })}
        />
      </FormSection>

      <FormSection
        title="基准数据集"
        action={
          <SaveButton
            label="保存基准配置"
            onClick={() =>
              onSaveBacktestSettings(
                { benchmark_dataset: normalizeBenchmarkDataset(backtest.benchmark_dataset) },
                "回测基准数据集已保存",
              )
            }
          />
        }
      >
        <SelectField
          label="数据集"
          value={backtest.benchmark_dataset.dataset_id}
          options={datasetOptions}
          placeholder="选择数据集"
          onChange={(dataset_id) => updateBenchmark(emptyBenchmarkFieldPatch(dataset_id))}
        />
        <FieldSelect
          label="代码字段"
          value={backtest.benchmark_dataset.symbol_field}
          columns={benchmarkColumns}
          isLoading={isLoadingBenchmarkColumns}
          onChange={(symbol_field) => updateBenchmark({ symbol_field })}
        />
        <FieldSelect
          label="日期字段"
          value={backtest.benchmark_dataset.datetime_field}
          columns={benchmarkColumns}
          isLoading={isLoadingBenchmarkColumns}
          onChange={(datetime_field) => updateBenchmark({ datetime_field })}
        />
        <FieldSelect
          label="收盘字段"
          value={backtest.benchmark_dataset.close_field}
          columns={benchmarkColumns}
          isLoading={isLoadingBenchmarkColumns}
          onChange={(close_field) => updateBenchmark({ close_field })}
        />
      </FormSection>
    </div>
  );
}

function FieldSelect({
  label,
  value,
  columns,
  isLoading,
  onChange,
}: {
  label: string;
  value: string;
  columns: string[];
  isLoading: boolean;
  onChange: (value: string) => void;
}) {
  const options = fieldOptions(columns, value);
  return (
    <SelectField
      label={label}
      value={value}
      options={options}
      disabled={isLoading || columns.length === 0}
      placeholder={isLoading ? "加载字段" : "选择字段"}
      onChange={onChange}
    />
  );
}

function SaveButton({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <Button
      size="sm"
      variant="outline"
      type="button"
      onClick={onClick}
    >
      <Save className="h-3.5 w-3.5" />
      {label}
    </Button>
  );
}

function fieldOptions(
  columns: string[],
  currentValue: string,
): Array<{ label: string; value: string }> {
  const normalized = columns.map((column) => ({ label: column, value: column }));
  const options = normalized;
  if (currentValue && !options.some((option) => option.value === currentValue)) {
    return [{ label: `${currentValue}（当前）`, value: currentValue }, ...options];
  }
  return options;
}

function quoteDuckdbIdentifier(identifier: string): string {
  return `"${identifier.replace(/"/g, '""')}"`;
}

function emptyMarketFieldPatch(
  datasetId: string,
): Partial<BacktestSettings["market_dataset"]> {
  return {
    dataset_id: datasetId,
    symbol_field: "",
    datetime_field: "",
    open_field: "",
    high_field: "",
    low_field: "",
    close_field: "",
    volume_field: "",
  };
}

function emptyBenchmarkFieldPatch(
  datasetId: string,
): Partial<BacktestSettings["benchmark_dataset"]> {
  return {
    dataset_id: datasetId,
    symbol_field: "",
    datetime_field: "",
    close_field: "",
  };
}

function sanitizeMarketDatasetFields(
  settings: BacktestSettings["market_dataset"],
  columns: string[],
): BacktestSettings["market_dataset"] {
  const next = {
    ...settings,
    symbol_field: keepColumn(settings.symbol_field, columns),
    datetime_field: keepColumn(settings.datetime_field, columns),
    open_field: keepColumn(settings.open_field, columns),
    high_field: keepColumn(settings.high_field, columns),
    low_field: keepColumn(settings.low_field, columns),
    close_field: keepColumn(settings.close_field, columns),
    volume_field: keepColumn(settings.volume_field, columns),
  };
  return shallowEqual(next, settings) ? settings : next;
}

function sanitizeBenchmarkDatasetFields(
  settings: BacktestSettings["benchmark_dataset"],
  columns: string[],
): BacktestSettings["benchmark_dataset"] {
  const next = {
    ...settings,
    symbol_field: keepColumn(settings.symbol_field, columns),
    datetime_field: keepColumn(settings.datetime_field, columns),
    close_field: keepColumn(settings.close_field, columns),
  };
  return shallowEqual(next, settings) ? settings : next;
}

function keepColumn(value: string, columns: string[]): string {
  return columns.includes(value) ? value : "";
}

function shallowEqual<T extends Record<string, unknown>>(left: T, right: T): boolean {
  return Object.keys(left).every((key) => left[key] === right[key]);
}

function normalizeMarketDataset(
  settings: BacktestSettings["market_dataset"],
): BacktestSettings["market_dataset"] {
  return {
    ...settings,
    dataset_id: settings.dataset_id.trim(),
    symbol_field: settings.symbol_field.trim(),
    datetime_field: settings.datetime_field.trim(),
    open_field: settings.open_field.trim(),
    high_field: settings.high_field.trim(),
    low_field: settings.low_field.trim(),
    close_field: settings.close_field.trim(),
    volume_field: settings.volume_field.trim(),
  };
}

function normalizeBenchmarkDataset(
  settings: BacktestSettings["benchmark_dataset"],
): BacktestSettings["benchmark_dataset"] {
  return {
    ...settings,
    dataset_id: settings.dataset_id.trim(),
    symbol_field: settings.symbol_field.trim(),
    datetime_field: settings.datetime_field.trim(),
    close_field: settings.close_field.trim(),
  };
}
