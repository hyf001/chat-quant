import { toast } from "sonner";

export type ToastTone = "success" | "error" | "info";

export function notify(message: string, tone: ToastTone = "info") {
  if (tone === "success") {
    toast.success(message);
    return;
  }
  if (tone === "error") {
    toast.error(message);
    return;
  }
  toast.message(message);
}
