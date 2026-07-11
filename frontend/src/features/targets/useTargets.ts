import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiRequest } from "../../services/apiClient";

export type DesiredState = "on" | "off";
export type VerificationMethod = "dom-attribute" | "text-label" | "aria-checked";

export type CapturedItemRule = {
  key: string;
  selector: string;
};

export type ToggleControlRule = {
  controlSelector: string;
  stateSelector: string;
  verificationMethod: VerificationMethod;
};

export type AutomationTarget = {
  id: string;
  name: string;
  baseUrl: string;
  pagePath: string;
  authProfile: string | null;
  extractionRules: CapturedItemRule[];
  toggleRule: ToggleControlRule;
  defaultDesiredState: DesiredState;
  createdAt: string;
  updatedAt: string;
};

export type AutomationTargetInput = Omit<AutomationTarget, "id" | "createdAt" | "updatedAt">;

const targetKeys = {
  all: ["targets"] as const,
};

export function useTargetsQuery() {
  return useQuery({
    queryKey: targetKeys.all,
    queryFn: () => apiRequest<AutomationTarget[]>("/targets"),
  });
}

export function useCreateTargetMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: AutomationTargetInput) =>
      apiRequest<AutomationTarget>("/targets", {
        method: "POST",
        body: payload,
      }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: targetKeys.all });
    },
  });
}

export function useUpdateTargetMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: AutomationTargetInput }) =>
      apiRequest<AutomationTarget>(`/targets/${id}`, {
        method: "PATCH",
        body: payload,
      }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: targetKeys.all });
    },
  });
}

export function useDeleteTargetMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) =>
      apiRequest<void>(`/targets/${id}`, {
        method: "DELETE",
      }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: targetKeys.all });
    },
  });
}
