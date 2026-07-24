import type { ReactNode } from "react";

type StatusPillProps = {
  icon?: ReactNode;
  label: string;
};

export function StatusPill({ icon, label }: StatusPillProps) {
  return (
    <div className="hidden items-center gap-2 rounded-full border border-line bg-panel px-3 py-1.5 text-xs font-medium text-muted sm:inline-flex">
      {icon}
      {label}
    </div>
  );
}
