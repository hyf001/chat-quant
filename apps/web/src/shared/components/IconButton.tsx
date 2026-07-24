import type { ReactNode } from "react";

type IconButtonProps = {
  label: string;
  icon: ReactNode;
  onClick?: () => void;
};

export function IconButton({ label, icon, onClick }: IconButtonProps) {
  return (
    <button
      className="grid size-9 place-items-center rounded-lg border border-line bg-soft text-ink transition hover:border-strong hover:bg-panel"
      aria-label={label}
      onClick={onClick}
      type="button"
    >
      {icon}
    </button>
  );
}
