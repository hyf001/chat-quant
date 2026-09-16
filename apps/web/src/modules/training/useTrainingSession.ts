import { useCallback, useEffect, useRef, useState } from "react";

import {
  TrainingApiError,
  createTrainingSession,
  finishTrainingSession,
  getTrainingSession,
  getTrainingReport,
  revealTrainingBar,
  type TrainingAction,
  type TrainingBar,
  type TrainingConfig,
  type TrainingFill,
  type TrainingMarker,
  type TrainingOrderRejection,
  type TrainingReportResponse,
  type TrainingSessionView,
} from "@/shared/api/training";
import { notify } from "@/shared/notify";

const STORAGE_KEY = "chatq.training.session";

export type TrainingPhase = "idle" | "loading" | "active" | "finished";

export type TrainingSessionState = {
  phase: TrainingPhase;
  session: TrainingSessionView | null;
  bars: TrainingBar[];
  markers: TrainingMarker[];
  fills: TrainingFill[];
  rejected: TrainingOrderRejection[];
  report: TrainingReportResponse | null;
  elapsedSeconds: number;
  busy: boolean;
  error: string | null;
};

const initialState: TrainingSessionState = {
  phase: "idle",
  session: null,
  bars: [],
  markers: [],
  fills: [],
  rejected: [],
  report: null,
  elapsedSeconds: 0,
  busy: false,
  error: null,
};

export function useTrainingSession(projectId: string | null) {
  const [state, setState] = useState<TrainingSessionState>(initialState);
  const busyRef = useRef(false);

  const applySession = useCallback(
    (payload: {
      session: TrainingSessionView;
      bars: TrainingBar[];
      markers: TrainingMarker[];
    }, extra: Partial<TrainingSessionState> = {}) => {
      window.localStorage.setItem(STORAGE_KEY, payload.session.id);
      setState((current) => ({
        ...current,
        phase: payload.session.status === "finished" ? "finished" : "active",
        session: payload.session,
        bars: payload.bars,
        markers: payload.markers,
        elapsedSeconds: payload.session.elapsed_seconds,
        error: null,
        ...extra,
      }));
    },
    [],
  );

  const start = useCallback(
    async (config: Partial<TrainingConfig>): Promise<boolean> => {
      if (!projectId || busyRef.current) {
        return false;
      }
      busyRef.current = true;
      setState((current) => ({ ...current, phase: "loading", busy: true, error: null }));
      try {
        const payload = await createTrainingSession({ project_id: projectId, config });
        setState({ ...initialState, fills: [], rejected: [] });
        applySession(payload);
        return true;
      } catch (error) {
        setState((current) => ({
          ...current,
          phase: "idle",
          busy: false,
          error: errorMessage(error),
        }));
        notify(errorMessage(error), "error");
        return false;
      } finally {
        busyRef.current = false;
        setState((current) => ({ ...current, busy: false }));
      }
    },
    [applySession, projectId],
  );

  /** 已收局的会话：只拉复盘报告，不写本地续做游标。 */
  const openReport = useCallback(async (sessionId: string) => {
    if (busyRef.current) {
      return;
    }
    busyRef.current = true;
    setState((current) => ({ ...current, busy: true }));
    try {
      const report = await getTrainingReport(sessionId);
      window.localStorage.removeItem(STORAGE_KEY);
      setState((current) => ({
        ...current,
        phase: "finished",
        session: report.session,
        report,
        bars: report.report.bars,
        markers: report.report.markers,
        error: null,
      }));
    } catch (error) {
      notify(errorMessage(error), "error");
    } finally {
      busyRef.current = false;
      setState((current) => ({ ...current, busy: false }));
    }
  }, []);

  /** 收局统一落地：换掉 bars/markers 并放开报告（页面据此自动弹出复盘）。 */
  const applyReport = useCallback((report: TrainingReportResponse) => {
    window.localStorage.removeItem(STORAGE_KEY);
    setState((value) => ({
      ...value,
      phase: "finished",
      session: report.session,
      report,
      bars: report.report.bars,
      markers: report.report.markers,
      error: null,
    }));
  }, []);

  /** 从列表进入某一局：active 续做，finished 直接进复盘。 */
  const resume = useCallback(
    async (sessionId: string) => {
      if (busyRef.current) {
        return;
      }
      busyRef.current = true;
      setState((current) => ({ ...current, phase: "loading", busy: true, error: null }));
      try {
        const payload = await getTrainingSession(sessionId);
        if (payload.session.status === "finished") {
          const report = await getTrainingReport(sessionId);
          window.localStorage.removeItem(STORAGE_KEY);
          setState((current) => ({
            ...current,
            phase: "finished",
            session: report.session,
            report,
            bars: report.report.bars,
            markers: report.report.markers,
            error: null,
          }));
          return;
        }
        setState({ ...initialState, phase: "loading", busy: true });
        applySession(payload);
      } catch (error) {
        notify(errorMessage(error), "error");
        setState((current) => ({
          ...current,
          phase: "idle",
          session: null,
          error: errorMessage(error),
        }));
      } finally {
        busyRef.current = false;
        setState((current) => ({ ...current, busy: false }));
      }
    },
    [applySession],
  );

  const reveal = useCallback(
    async (action: TrainingAction, size?: number) => {
      const current = state.session;
      if (!current || current.status === "finished" || busyRef.current) {
        return;
      }
      busyRef.current = true;
      setState((value) => ({ ...value, busy: true }));
      try {
        const payload = await revealTrainingBar(current.id, {
          seq: current.cursor_index,
          action,
          ...(size === undefined ? {} : { size }),
        });
        applySession(
          {
            session: payload.session,
            bars: payload.bar ? [...state.bars, payload.bar] : state.bars,
            markers: payload.markers,
          },
          {
            fills: payload.fills,
            rejected: payload.rejected,
          },
        );
        if (payload.rejected.length > 0) {
          notify(rejectionMessage(payload.rejected), "error");
        }
        if (payload.session.status === "finished") {
          // 训练段走完这一根：服务端已自动收局，顺手把复盘报告拉回来（弹窗自动打开）
          applyReport(await getTrainingReport(payload.session.id));
        }
      } catch (error) {
        handleRevealError(error);
      } finally {
        busyRef.current = false;
        setState((value) => ({ ...value, busy: false }));
      }
    },
    [applyReport, applySession, state.bars, state.session],
  );

  /** 提前结束：最后一根之前收局（走到最后一根会自动收局，不需要点这里）。 */
  const finish = useCallback(async () => {
    const current = state.session;
    if (!current || busyRef.current) {
      return;
    }
    busyRef.current = true;
    setState((value) => ({ ...value, busy: true }));
    try {
      applyReport(await finishTrainingSession(current.id));
    } catch (error) {
      notify(errorMessage(error), "error");
    } finally {
      busyRef.current = false;
      setState((value) => ({ ...value, busy: false }));
    }
  }, [applyReport, state.session]);

  const reset = useCallback(() => {
    window.localStorage.removeItem(STORAGE_KEY);
    setState(initialState);
  }, []);

  const clearError = useCallback(() => {
    setState((current) => (current.error === null ? current : { ...current, error: null }));
  }, []);

  const resync = useCallback(async () => {
    const current = state.session;
    if (!current) {
      return;
    }
    try {
      const payload = await getTrainingSession(current.id);
      applySession(payload);
    } catch (error) {
      notify(errorMessage(error), "error");
    }
  }, [applySession, state.session]);

  const handleRevealError = useCallback(
    (error: unknown) => {
      if (error instanceof TrainingApiError && error.code === "TRAINING_REVEAL_SEQ_CONFLICT") {
        notify("进度与服务端不一致，已重新同步", "error");
        void resync();
        return;
      }
      notify(errorMessage(error), "error");
    },
    [resync],
  );

  // 刷新后续做：按 session_id 恢复（不重播已揭示数据，一次性 setData）
  useEffect(() => {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (!stored || !projectId) {
      return;
    }
    let cancelled = false;
    setState((current) => ({ ...current, phase: "loading", busy: true }));
    getTrainingSession(stored)
      .then((payload) => {
        if (!cancelled) {
          applySession(payload);
        }
      })
      .catch(() => {
        window.localStorage.removeItem(STORAGE_KEY);
        if (!cancelled) {
          setState((current) => ({ ...current, phase: "idle", busy: false }));
        }
      })
      .finally(() => {
        if (!cancelled) {
          setState((current) => ({ ...current, busy: false }));
        }
      });
    return () => {
      cancelled = true;
    };
  }, [applySession, projectId]);

  // 用时由 started_at 现算，刷新 / Electron 下都正确
  useEffect(() => {
    if (state.phase !== "active" || !state.session) {
      return undefined;
    }
    const started = new Date(state.session.started_at).getTime();
    const timer = window.setInterval(() => {
      setState((current) =>
        current.session && current.session.status === "active"
          ? { ...current, elapsedSeconds: Math.max(0, Math.floor((Date.now() - started) / 1000)) }
          : current,
      );
    }, 1000);
    return () => window.clearInterval(timer);
  }, [state.phase, state.session]);

  return { state, start, reveal, finish, reset, resync, resume, openReport, clearError };
}

function errorMessage(error: unknown): string {
  if (error instanceof TrainingApiError) {
    return error.message;
  }
  return error instanceof Error ? error.message : "训练请求失败";
}

/** 拒单提示：资金不足（margin）/ 卖出超过持仓（oversell）。 */
function rejectionMessage(rejected: TrainingOrderRejection[]): string {
  const first = rejected[0];
  const side = first.side === "buy" ? "买入" : "卖出";
  const reason =
    first.reason === "margin"
      ? "可用资金不足"
      : first.reason === "oversell"
        ? "超过当前持仓"
        : "被券商拒单";
  return `${side} ${first.size} 股${reason}，请按面板的可用资金 / 持仓重下`;
}
