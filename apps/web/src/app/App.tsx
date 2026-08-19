import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";

import { WorkbenchPage } from "../pages/WorkbenchPage";

export function App() {
  return (
    <TooltipProvider delayDuration={250}>
      <WorkbenchPage />
      <Toaster />
    </TooltipProvider>
  );
}
