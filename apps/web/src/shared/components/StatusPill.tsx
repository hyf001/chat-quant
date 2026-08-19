import type { ReactNode } from "react";

import { Badge } from "@/components/ui/badge";

type StatusPillProps = {
  icon?: ReactNode;
  label: string;
};

export function StatusPill({ icon, label }: StatusPillProps) {
  return (
    <Badge className="hidden gap-2 px-3 py-1.5 font-medium sm:inline-flex" variant="outline">
      {icon}
      {label}
    </Badge>
  );
}
