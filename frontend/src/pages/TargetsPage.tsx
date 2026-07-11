import { useState } from "react";
import { ApiClientError } from "../services/apiClient";
import { TargetForm } from "../components/targets/TargetForm";
import {
  AutomationTarget,
  AutomationTargetInput,
  useCreateTargetMutation,
  useDeleteTargetMutation,
  useTargetsQuery,
  useUpdateTargetMutation,
} from "../features/targets/useTargets";

function formatTargetPath(target: AutomationTarget) {
  return `${target.baseUrl}${target.pagePath}`;
}

export function TargetsPage() {
  const [editingTarget, setEditingTarget] = useState<AutomationTarget | null>(null);
  const [banner, setBanner] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const targetsQuery = useTargetsQuery();
  const createMutation = useCreateTargetMutation();
  const updateMutation = useUpdateTargetMutation();
  const deleteMutation = useDeleteTargetMutation();

  async function handleSubmit(payload: AutomationTargetInput) {
    try {
      setError(null);
      setBanner(null);

      if (editingTarget) {
        await updateMutation.mutateAsync({ id: editingTarget.id, payload });
        setEditingTarget(null);
        setBanner("Target updated.");
        return;
      }

      await createMutation.mutateAsync(payload);
      setBanner("Target saved.");
    } catch (mutationError) {
      setError(
        mutationError instanceof ApiClientError ? mutationError.message : "Unable to save the target.",
      );
    }
  }

  async function handleDelete(targetId: string) {
    try {
      setError(null);
      setBanner(null);
      await deleteMutation.mutateAsync(targetId);
      if (editingTarget?.id === targetId) {
        setEditingTarget(null);
      }
      setBanner("Target deleted.");
    } catch (mutationError) {
      setError(
        mutationError instanceof ApiClientError ? mutationError.message : "Unable to delete the target.",
      );
    }
  }

  const targets = targetsQuery.data ?? [];

  return (
    <div className="page-shell">
      <section className="hero-card">
        <p className="eyebrow">User Story 1</p>
        <h1>Automation targets</h1>
        <p>
          Save the browser path, capture rules, and toggle selectors once, then reuse them for every
          manual automation run.
        </p>
      </section>

      <div className="targets-layout">
        <section className="card">
          <TargetForm
            initialTarget={editingTarget}
            isSubmitting={createMutation.isPending || updateMutation.isPending}
            onCancelEdit={() => setEditingTarget(null)}
            onSubmit={handleSubmit}
          />
          {error ? <p className="form-error">{error}</p> : null}
          {banner ? <p className="form-success">{banner}</p> : null}
        </section>

        <section className="card">
          <div className="card-header">
            <div>
              <h2>Saved targets</h2>
              <p>Review and update the target definitions available for future runs.</p>
            </div>
          </div>

          {targetsQuery.isLoading ? <p>Loading targets...</p> : null}
          {!targetsQuery.isLoading && targets.length === 0 ? <p>No targets saved yet.</p> : null}

          <div className="target-list">
            {targets.map((target) => (
              <article className="target-list-item" key={target.id}>
                <div>
                  <h3>{target.name}</h3>
                  <p>{formatTargetPath(target)}</p>
                  <p>
                    Default state: <strong>{target.defaultDesiredState}</strong>
                  </p>
                </div>
                <div className="target-actions">
                  <button type="button" className="ghost-button" onClick={() => setEditingTarget(target)}>
                    Edit
                  </button>
                  <button
                    type="button"
                    className="danger-button"
                    onClick={() => void handleDelete(target.id)}
                    disabled={deleteMutation.isPending}
                  >
                    Delete
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
