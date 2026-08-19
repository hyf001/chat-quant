import {
  AlertCircle,
  CheckCircle2,
  Inbox,
  Loader2,
} from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

type StateNoticeProps = {
  title: string;
  description?: string;
  className?: string;
};

export function EmptyState({ title, description, className }: StateNoticeProps) {
  return (
    <Alert className={className} variant="muted">
      <Inbox className="h-4 w-4" />
      <AlertTitle>{title}</AlertTitle>
      {description ? <AlertDescription>{description}</AlertDescription> : null}
    </Alert>
  );
}

export function LoadingState({
  title = "加载中",
  className,
  rows = 3,
}: {
  title?: string;
  className?: string;
  rows?: 1 | 2 | 3;
}) {
  return (
    <div className={cn("rounded-md border bg-card p-4", className)} role="status">
      <div className="mb-3 flex items-center gap-2 text-xs font-medium text-muted-foreground">
        <Loader2 className="h-4 w-4 animate-spin" />
        {title}
      </div>
      <div className="grid gap-2">
        <Skeleton className="h-3 w-full" />
        {rows >= 2 ? <Skeleton className="h-3 w-5/6" /> : null}
        {rows >= 3 ? <Skeleton className="h-3 w-2/3" /> : null}
      </div>
    </div>
  );
}

export function InlineAlert({
  title,
  description,
  tone = "error",
  className,
}: StateNoticeProps & {
  tone?: "error" | "success";
}) {
  const isError = tone === "error";
  return (
    <Alert className={className} variant={isError ? "destructive" : "success"}>
      {isError ? <AlertCircle className="h-4 w-4" /> : <CheckCircle2 className="h-4 w-4" />}
      <AlertTitle>{title}</AlertTitle>
      {description ? <AlertDescription>{description}</AlertDescription> : null}
    </Alert>
  );
}
