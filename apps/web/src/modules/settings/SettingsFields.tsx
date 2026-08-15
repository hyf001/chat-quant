import { Check, Copy, Save, X } from "lucide-react";
import { useState, type ReactNode } from "react";

import { emptyToNull, linesToList } from "./settingsUtils";

export function FormSection({
  title,
  action,
  children,
}: {
  title: string;
  action?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-sm font-semibold text-ink">{title}</h2>
        {action}
      </div>
      <div className="grid gap-3 sm:grid-cols-2">{children}</div>
    </div>
  );
}

export function TextField({
  label,
  value,
  onChange,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: "text" | "password";
}) {
  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <input
        className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal"
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

export function ApiKeyField({
  hasSavedApiKey,
  value,
  onChange,
  onCopy,
}: {
  hasSavedApiKey: boolean;
  value: string | null;
  onChange: (value: string | null) => void;
  onCopy?: () => void;
}) {
  const [isEditing, setIsEditing] = useState(false);
  const displayValue = value ?? (hasSavedApiKey && !isEditing ? "***" : "");
  const isShowingSavedMask = value === null && hasSavedApiKey && !isEditing;

  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">API Key</span>
      <span className="flex h-10 items-center rounded-md border border-line bg-panel focus-within:border-signal">
        <input
          className="min-h-0 min-w-0 flex-1 bg-transparent px-2.5 text-xs text-ink outline-none"
          type={isShowingSavedMask ? "text" : "password"}
          value={displayValue}
          onFocus={() => setIsEditing(true)}
          onBlur={() => {
            if (!value) {
              setIsEditing(false);
            }
          }}
          onChange={(event) => onChange(emptyToNull(event.target.value))}
        />
        {onCopy ? (
          <button
            className="grid h-8 w-8 shrink-0 place-items-center rounded-md text-muted transition-colors hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
            type="button"
            title="复制 API Key"
            aria-label="复制 API Key"
            onClick={onCopy}
          >
            <Copy className="h-3.5 w-3.5" />
          </button>
        ) : null}
      </span>
    </label>
  );
}

export function NumberField({
  label,
  value,
  onChange,
  onCommit,
  disabled = false,
  min = 0,
}: {
  label: string;
  value: number;
  onChange: (value: number) => void;
  onCommit?: () => void;
  disabled?: boolean;
  min?: number;
}) {
  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <span className="flex h-10 items-center rounded-md border border-line bg-panel focus-within:border-signal">
        <input
          className="min-h-0 min-w-0 flex-1 bg-transparent px-2.5 text-xs text-ink outline-none disabled:cursor-not-allowed disabled:text-muted"
          min={min}
          type="number"
          value={value}
          disabled={disabled}
          onChange={(event) => onChange(Number(event.target.value))}
        />
        {onCommit ? (
          <button
            className="grid h-8 w-8 shrink-0 place-items-center rounded-md text-muted transition-colors hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20 disabled:cursor-not-allowed disabled:opacity-50"
            type="button"
            title={`保存${label}`}
            aria-label={`保存${label}`}
            disabled={disabled}
            onClick={onCommit}
          >
            <Save className="h-3.5 w-3.5" />
          </button>
        ) : null}
      </span>
    </label>
  );
}

export function SelectField({
  label,
  value,
  options,
  onChange,
  disabled = false,
  placeholder,
}: {
  label: string;
  value: string;
  options: string[] | Array<{ label: string; value: string }>;
  onChange: (value: string) => void;
  disabled?: boolean;
  placeholder?: string;
}) {
  const normalizedOptions = options.map((option) =>
    typeof option === "string" ? { label: option, value: option } : option,
  );

  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <select
        className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal disabled:cursor-not-allowed disabled:bg-soft disabled:text-muted"
        value={disabled && placeholder ? "" : value}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value)}
      >
        {placeholder ? <option value="">{placeholder}</option> : null}
        {normalizedOptions.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

export function ToggleField({
  label,
  checked,
  onChange,
  description,
}: {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  description?: string;
}) {
  return (
    <label className="flex min-h-12 items-center justify-between gap-3 rounded-md border border-line bg-panel px-3 py-2">
      <span className="min-w-0">
        <span className="block text-xs font-semibold text-graphite">{label}</span>
        {description ? (
          <span className="mt-0.5 block text-[11px] leading-4 text-muted">{description}</span>
        ) : null}
      </span>
      <input
        className="peer sr-only"
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
      />
      <span
        className="relative h-6 w-11 shrink-0 rounded-full bg-line transition-colors after:absolute after:left-0.5 after:top-0.5 after:h-5 after:w-5 after:rounded-full after:bg-panel after:shadow-sm after:transition-transform peer-checked:bg-brand peer-checked:after:translate-x-5 peer-focus-visible:ring-2 peer-focus-visible:ring-signal/25"
        aria-hidden="true"
      />
    </label>
  );
}

export function ListField({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string[];
  onChange: (value: string[]) => void;
}) {
  return (
    <label className="grid gap-1.5 sm:col-span-2">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <textarea
        className="min-h-20 rounded-md border border-line bg-panel px-2.5 py-2 text-xs leading-5 text-ink outline-none focus:border-signal"
        value={value.join("\n")}
        onChange={(event) => onChange(linesToList(event.target.value))}
      />
    </label>
  );
}

export function ChipListField({
  label,
  value,
  options,
  onChange,
  disabled = false,
}: {
  label: string;
  value: string[];
  options: string[];
  onChange: (value: string[]) => void;
  disabled?: boolean;
}) {
  const availableOptions = options.filter((option) => !value.includes(option));
  const [selectedOption, setSelectedOption] = useState("");

  const removeItem = (item: string) => {
    if (disabled) {
      return;
    }
    onChange(value.filter((current) => current !== item));
  };

  const addSelectedOption = () => {
    if (disabled || !selectedOption || value.includes(selectedOption)) {
      return;
    }
    onChange([...value, selectedOption]);
    setSelectedOption("");
  };

  return (
    <div className="grid gap-2 sm:col-span-2">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <div className="rounded-md border border-line bg-panel p-2">
        <div className="flex flex-wrap gap-1.5">
          {value.map((item) => (
            <span
              className="inline-flex min-h-7 items-center gap-1 rounded-md border border-line bg-soft px-2 font-mono text-[11px] text-graphite"
              key={item}
            >
              {item}
              <button
                className="grid h-4 w-4 place-items-center rounded text-muted transition-colors hover:bg-riskSoft hover:text-risk focus:outline-none focus:ring-2 focus:ring-risk/20"
                type="button"
                aria-label={`移除 ${item}`}
                title={`移除 ${item}`}
                disabled={disabled}
                onClick={() => removeItem(item)}
              >
                <X className="h-3 w-3" />
              </button>
            </span>
          ))}
          {value.length === 0 ? (
            <span className="px-1 py-1 text-xs text-muted">暂无工具</span>
          ) : null}
        </div>
        <div className="mt-2 flex flex-wrap gap-2 border-t border-line pt-2">
          <select
            className="h-9 min-w-0 flex-1 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal disabled:cursor-not-allowed disabled:bg-soft disabled:text-muted"
            value={selectedOption}
            disabled={disabled || availableOptions.length === 0}
            onChange={(event) => setSelectedOption(event.target.value)}
          >
            <option value="">
              {availableOptions.length === 0 ? "没有可添加工具" : "选择要添加的工具"}
            </option>
            {availableOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          <button
            className="inline-flex h-9 items-center rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite disabled:cursor-not-allowed disabled:opacity-60"
            type="button"
            disabled={disabled || !selectedOption}
            onClick={addSelectedOption}
          >
            添加
          </button>
        </div>
      </div>
    </div>
  );
}

export function StatusMessage({ message }: { message: string }) {
  const isSaved = message.includes("已");

  return (
    <div
      className="rounded-md border border-line bg-panel px-2.5 py-2 text-xs text-muted"
      role="status"
    >
      {isSaved ? (
        <span className="inline-flex items-center gap-1 text-brand">
          <Check className="h-3.5 w-3.5" />
          {message}
        </span>
      ) : (
        message
      )}
    </div>
  );
}
