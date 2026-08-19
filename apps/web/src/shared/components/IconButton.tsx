import type { ReactNode } from "react";

import { Button } from "@/components/ui/button";

type IconButtonProps = {
  label: string;
  icon: ReactNode;
  onClick?: () => void;
};

export function IconButton({ label, icon, onClick }: IconButtonProps) {
  return (
    <Button
      aria-label={label}
      onClick={onClick}
      size="icon"
      title={label}
      type="button"
      variant="outline"
    >
      {icon}
    </Button>
  );
}
