import { Check, Copy, Save, X } from "lucide-react";
import { useState, type ReactNode } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";

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
    <Label className="grid gap-1.5">
      <span>{label}</span>
      <Input
        className="h-10 text-xs"
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </Label>
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
    <Label className="grid gap-1.5">
      <span>API Key</span>
      <span className="flex h-10 items-center rounded-md border border-input bg-background shadow-sm focus-within:ring-2 focus-within:ring-ring/30">
        <Input
          className="h-8 min-w-0 flex-1 border-0 bg-transparent px-3 text-xs shadow-none focus-visible:ring-0"
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
          <Button
            className="mr-1"
            size="iconSm"
            variant="ghost"
            type="button"
            title="复制 API Key"
            aria-label="复制 API Key"
            onClick={onCopy}
          >
            <Copy className="h-3.5 w-3.5" />
          </Button>
        ) : null}
      </span>
    </Label>
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
    <Label className="grid gap-1.5">
      <span>{label}</span>
      <span className="flex h-10 items-center rounded-md border border-input bg-background shadow-sm focus-within:ring-2 focus-within:ring-ring/30">
        <Input
          className="h-8 min-w-0 flex-1 border-0 bg-transparent px-3 text-xs shadow-none focus-visible:ring-0"
          min={min}
          type="number"
          value={value}
          disabled={disabled}
          onChange={(event) => onChange(Number(event.target.value))}
        />
        {onCommit ? (
          <Button
            className="mr-1"
            size="iconSm"
            variant="ghost"
            type="button"
            title={`保存${label}`}
            aria-label={`保存${label}`}
            disabled={disabled}
            onClick={onCommit}
          >
            <Save className="h-3.5 w-3.5" />
          </Button>
        ) : null}
      </span>
    </Label>
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
    <Label className="grid gap-1.5">
      <span>{label}</span>
      <Select
        value={disabled && placeholder ? "" : value}
        disabled={disabled}
        onValueChange={onChange}
      >
        <SelectTrigger className="h-10 text-xs">
          <SelectValue placeholder={placeholder} />
        </SelectTrigger>
        <SelectContent>
          {placeholder ? (
            <SelectItem value="__placeholder" disabled>
              {placeholder}
            </SelectItem>
          ) : null}
          {normalizedOptions.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </Label>
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
    <Label className="flex min-h-12 items-center justify-between gap-3 rounded-md border bg-card px-3 py-2 shadow-sm">
      <span className="min-w-0">
        <span className="block">{label}</span>
        {description ? (
          <span className="mt-0.5 block text-[11px] leading-4 text-muted-foreground">
            {description}
          </span>
        ) : null}
      </span>
      <Switch
        checked={checked}
        onCheckedChange={onChange}
      />
    </Label>
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
    <Label className="grid gap-1.5 sm:col-span-2">
      <span>{label}</span>
      <Textarea
        className="text-xs leading-5"
        value={value.join("\n")}
        onChange={(event) => onChange(linesToList(event.target.value))}
      />
    </Label>
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
      <Label>{label}</Label>
      <div className="rounded-md border bg-card p-2 shadow-sm">
        <div className="flex flex-wrap gap-1.5">
          {value.map((item) => (
            <Badge
              className="min-h-7 gap-1 font-mono text-[11px]"
              variant="secondary"
              key={item}
            >
              {item}
              <Button
                className="h-4 w-4"
                size="iconSm"
                variant="ghost"
                type="button"
                aria-label={`移除 ${item}`}
                title={`移除 ${item}`}
                disabled={disabled}
                onClick={() => removeItem(item)}
              >
                <X className="h-3 w-3" />
              </Button>
            </Badge>
          ))}
          {value.length === 0 ? (
            <span className="px-1 py-1 text-xs text-muted-foreground">暂无工具</span>
          ) : null}
        </div>
        <div className="mt-2 flex flex-wrap gap-2 border-t border-line pt-2">
          <Select
            value={selectedOption}
            disabled={disabled || availableOptions.length === 0}
            onValueChange={setSelectedOption}
          >
            <SelectTrigger className="min-w-52 flex-1 text-xs">
              <SelectValue
                placeholder={availableOptions.length === 0 ? "没有可添加工具" : "选择要添加的工具"}
              />
            </SelectTrigger>
            <SelectContent>
              {availableOptions.map((option) => (
                <SelectItem key={option} value={option}>
                  {option}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button
            size="sm"
            type="button"
            disabled={disabled || !selectedOption}
            onClick={addSelectedOption}
          >
            添加
          </Button>
        </div>
      </div>
    </div>
  );
}

export function StatusMessage({ message }: { message: string }) {
  const isSaved = message.includes("已");

  return (
    <div
      className="rounded-md border bg-card px-2.5 py-2 text-xs text-muted-foreground shadow-sm"
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
