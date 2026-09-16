import { useEffect, useState } from "react";
import type { ReactNode } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { cn } from "@/lib/utils";

export type TrainingCreateForm = {
  initialCash: string;
  commission: string;
  slippage: string;
  excludeSt: boolean;
};

type TrainingCreateDialogProps = {
  open: boolean;
  busy: boolean;
  error: string | null;
  defaultForm: TrainingCreateForm;
  onClose: () => void;
  onSubmit: (form: TrainingCreateForm) => void;
};

/** 费率上限 10%：再高就不是"成本"而是"另一个游戏"了，后端也是这个界。 */
const MAX_RATE = 0.1;

export function TrainingCreateDialog({
  open,
  busy,
  error,
  defaultForm,
  onClose,
  onSubmit,
}: TrainingCreateDialogProps) {
  const [form, setForm] = useState<TrainingCreateForm>(defaultForm);

  // 每次打开都回到默认值，避免上一局的输入残留
  useEffect(() => {
    if (open) {
      setForm(defaultForm);
    }
  }, [open, defaultForm]);

  const cash = Number(form.initialCash);
  const cashInvalid = form.initialCash.trim() === "" || !Number.isFinite(cash) || cash <= 0;
  const commissionInvalid = !isValidRate(form.commission);
  const slippageInvalid = !isValidRate(form.slippage);
  const invalid = cashInvalid || commissionInvalid || slippageInvalid;

  return (
    <Dialog open={open} onOpenChange={(next) => (next ? undefined : onClose())}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>新建训练</DialogTitle>
        </DialogHeader>

        <div className="space-y-3">
          <Field label="初始资金">
            <Input
              value={form.initialCash}
              inputMode="decimal"
              autoComplete="off"
              onChange={(event) => setForm({ ...form, initialCash: event.target.value })}
            />
            {cashInvalid ? (
              <Hint tone="error">初始资金需要是大于 0 的数字</Hint>
            ) : null}
          </Field>

          <div className="grid gap-3 sm:grid-cols-2">
            <Field label="手续费（费率）">
              <Input
                value={form.commission}
                inputMode="decimal"
                autoComplete="off"
                onChange={(event) => setForm({ ...form, commission: event.target.value })}
              />
              {commissionInvalid ? (
                <Hint tone="error">填 0 ~ 0.1 之间的费率</Hint>
              ) : null}
            </Field>

            <Field label="滑点（费率）">
              <Input
                value={form.slippage}
                inputMode="decimal"
                autoComplete="off"
                onChange={(event) => setForm({ ...form, slippage: event.target.value })}
              />
              {slippageInvalid ? (
                <Hint tone="error">填 0 ~ 0.1 之间的费率</Hint>
              ) : null}
            </Field>
          </div>

          <div className="flex items-center justify-between gap-3 rounded-md border border-line bg-panel/60 px-3 py-2">
            <Label htmlFor="training-exclude-st">去除 ST 标的</Label>
            <Switch
              id="training-exclude-st"
              checked={form.excludeSt}
              onCheckedChange={(checked) => setForm({ ...form, excludeSt: checked })}
            />
          </div>

          <p className="text-xs text-ink-muted">
            开局随机抽一只标的的末端片段：180 根展示段 + 60~180 根训练段；窗口内含除权除息会重新抽题。
          </p>

          {error ? <Hint tone="error">{error}</Hint> : null}
        </div>

        <DialogFooter>
          <Button variant="outline" type="button" disabled={busy} onClick={onClose}>
            取消
          </Button>
          <Button type="button" disabled={busy || invalid} onClick={() => onSubmit(form)}>
            {busy ? "正在开局…" : "开始训练"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function isValidRate(value: string): boolean {
  if (value.trim() === "") {
    return false;
  }
  const numeric = Number(value);
  return Number.isFinite(numeric) && numeric >= 0 && numeric <= MAX_RATE;
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="grid gap-1.5">
      <Label>{label}</Label>
      {children}
    </div>
  );
}

function Hint({ tone = "muted", children }: { tone?: "muted" | "error"; children: ReactNode }) {
  return (
    <p className={cn("text-xs", tone === "error" ? "text-[#e11d48]" : "text-ink-muted")}>
      {children}
    </p>
  );
}
