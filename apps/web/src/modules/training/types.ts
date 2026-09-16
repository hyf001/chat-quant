export type {
  TrainingAccount,
  TrainingAction,
  TrainingBar,
  TrainingConfig,
  TrainingFill,
  TrainingMarker,
  TrainingMetrics,
  TrainingOrderRejection,
  TrainingReport,
  TrainingReportResponse,
  TrainingReveal,
  TrainingRevealedBar,
  TrainingSession,
  TrainingSessionList,
  TrainingSessionSummary,
  TrainingSessionView,
} from "@/shared/api/training";

/** 仓位档位用 key 表示，具体比例由 size 给到后端（1/3、1/5 是无限小数）。 */
export type TrainingPositionRatio = "all" | "half" | "third" | "quarter" | "fifth";

export type TrainingPositionOption = {
  value: TrainingPositionRatio;
  label: string;
  size: number;
};

export const POSITION_RATIOS: TrainingPositionOption[] = [
  { value: "all", label: "全仓", size: 1 },
  { value: "half", label: "1/2", size: 0.5 },
  { value: "third", label: "1/3", size: 1 / 3 },
  { value: "quarter", label: "1/4", size: 0.25 },
  { value: "fifth", label: "1/5", size: 0.2 },
];

export function ratioSize(ratio: TrainingPositionRatio): number {
  return POSITION_RATIOS.find((item) => item.value === ratio)?.size ?? 1;
}
