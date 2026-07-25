import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiRequest } from "../../services/apiClient";
import type { DesiredState } from "../targets/useTargets";

export type RunStatus = "queued" | "running" | "success" | "failed" | "no-change-needed";

export type CreateRunInput = {
  targetId: string;
  requestedState: DesiredState;
};

export type CapturedItem = {
  key: string;
  selector: string;
  value: string;
  capturedAt: string;
};

export type ToggleResult = {
  stateBefore: "on" | "off" | "unknown";
  stateAfter: "on" | "off" | "unknown";
  actionTaken: "none" | "toggle-once" | "retry-toggle";
  verified: boolean;
};

export type AutomationRun = {
  id: string;
  targetId: string;
  requestedState: DesiredState;
  status: RunStatus;
  startedAt: string;
  finishedAt: string | null;
  durationMs: number | null;
};

export type RunDetails = AutomationRun & {
  capturedItems: CapturedItem[];
  toggleResult: ToggleResult | null;
  failureStep: "navigate" | "authenticate" | "extract" | "toggle" | "verify" | null;
  failureMessage: string | null;
};

const runKeys = {
  details: (runId: string) => ["runs", runId] as const,
  targetRuns: (targetId: string) => ["target-runs", targetId] as const,
};

function isTerminal(status: RunStatus) {
  return status === "success" || status === "failed" || status === "no-change-needed";
}

export function useCreateRunMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateRunInput) =>
      apiRequest<AutomationRun>("/runs", {
        method: "POST",
        body: payload,
      }),
    onSuccess: async (run) => {
      await queryClient.invalidateQueries({ queryKey: runKeys.targetRuns(run.targetId) });
    },
  });
}

export function useRunDetailsQuery(runId: string | null) {
  return useQuery({
    queryKey: runId ? runKeys.details(runId) : ["runs", "idle"],
    enabled: Boolean(runId),
    queryFn: () => apiRequest<RunDetails>(`/runs/${runId}`),
    refetchInterval: (query) => {
      const current = query.state.data;
      if (!current || !runId) {
        return 1200;
      }
      return isTerminal(current.status) ? false : 1200;
    },
  });
}

export function useTargetRunsQuery(targetId: string | null) {
  return useQuery({
    queryKey: targetId ? runKeys.targetRuns(targetId) : ["target-runs", "idle"],
    enabled: Boolean(targetId),
    queryFn: () => apiRequest<AutomationRun[]>(`/targets/${targetId}/runs`),
  });
}
