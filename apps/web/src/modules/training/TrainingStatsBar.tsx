import type { TrainingSessionView } from "./types";

type TrainingStatsBarProps = {
  session: TrainingSessionView;
  elapsedSeconds: number;
};

export function TrainingStatsBar({ session, elapsedSeconds }: TrainingStatsBarProps) {
  const account = session.account;
  const items = [
    { label: "初始资金", value: formatMoney(account.initial_cash) },
    { label: "仓位", value: formatPercent(account.position_pct) },
    { label: "本局收益", value: `${signed(account.total_return)}%`, tone: tone(account.total_return) },
    { label: "开仓收益", value: `${signed(account.open_return)}%`, tone: tone(account.open_return) },
    { label: "用时", value: formatDuration(elapsedSeconds) },
    {
      label: "进度",
      value: `${session.cursor_index} / ${session.training_bars}`,
    },
  ];

  return (
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-6">
      {items.map((item) => (
        <div key={item.label} className="rounded-md border border-line bg-panel/60 px-3 py-2">
          <div className="text-[11px] text-ink-muted">{item.label}</div>
          <div className={`text-sm font-medium ${item.tone ?? "text-ink"}`}>{item.value}</div>
        </div>
      ))}
    </div>
  );
}

export function formatMoney(value: string | number): string {
  const numeric = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(numeric)) {
    return "—";
  }
  return numeric.toLocaleString("zh-CN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function signed(value: string | number): string {
  const numeric = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(numeric)) {
    return "—";
  }
  const text = numeric.toFixed(2);
  return numeric > 0 ? `+${text}` : text;
}

export function formatDuration(seconds: number): string {
  const total = Math.max(0, Math.floor(seconds));
  const minutes = Math.floor(total / 60);
  const rest = total % 60;
  return `${String(minutes).padStart(2, "0")}:${String(rest).padStart(2, "0")}`;
}

export function formatPercent(value: string | number, digits = 2): string {
  const numeric = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(numeric)) {
    return "—";
  }
  return `${numeric.toFixed(digits)}%`;
}

function tone(value: string | number): string {
  const numeric = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(numeric) || numeric === 0) {
    return "text-ink";
  }
  return numeric > 0 ? "text-[#e11d48]" : "text-[#16a34a]";
}
