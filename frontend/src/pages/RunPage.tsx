import { useMemo, useState } from "react";
import { ApiClientError } from "../services/apiClient";
import { useTargetsQuery } from "../features/targets/useTargets";
import { useCreateRunMutation, useRunDetailsQuery } from "../features/runs/useRunActions";

export function RunPage() {
  const targetsQuery = useTargetsQuery();
  const createRunMutation = useCreateRunMutation();

  const firstTargetId = targetsQuery.data?.[0]?.id ?? "";
  const [targetId, setTargetId] = useState("");
  const [requestedState, setRequestedState] = useState<"on" | "off">("on");
  const [runId, setRunId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const selectedTargetId = targetId || firstTargetId;
  const runDetailsQuery = useRunDetailsQuery(runId);

  const statusText = useMemo(() => {
    if (!runDetailsQuery.data) {
      return "No run started yet.";
    }
    return `Current status: ${runDetailsQuery.data.status}`;
  }, [runDetailsQuery.data]);

  async function handleTriggerRun() {
    if (!selectedTargetId) {
      setError("Select a target before triggering a run.");
      return;
    }

    try {
      setError(null);
      const run = await createRunMutation.mutateAsync({
        targetId: selectedTargetId,
        requestedState,
      });
      setRunId(run.id);
    } catch (mutationError) {
      setError(mutationError instanceof ApiClientError ? mutationError.message : "Unable to trigger run.");
    }
  }

  return (
    <div className="page-shell stack">
      <section className="hero-card">
        <p className="eyebrow">User Story 2</p>
        <h1>Run browser automation</h1>
        <p>Trigger an on-demand run to capture values and enforce your desired feature state.</p>
      </section>

      <section className="card stack">
        <h2>Run request</h2>
        <label>
          Target
          <select
            aria-label="Run target"
            value={selectedTargetId}
            onChange={(event) => setTargetId(event.target.value)}
          >
            {targetsQuery.data?.map((target) => (
              <option key={target.id} value={target.id}>
                {target.name}
              </option>
            ))}
          </select>
        </label>

        <label>
          Desired state
          <select
            aria-label="Desired state"
            value={requestedState}
            onChange={(event) => setRequestedState(event.target.value as "on" | "off")}
          >
            <option value="on">on</option>
            <option value="off">off</option>
          </select>
        </label>

        <button
          type="button"
          className="primary-button"
          onClick={() => void handleTriggerRun()}
          disabled={createRunMutation.isPending || targetsQuery.isLoading || !selectedTargetId}
        >
          Trigger run
        </button>

        {error ? <p className="form-error">{error}</p> : null}
      </section>

      <section className="card stack">
        <h2>Run status</h2>
        <p>{statusText}</p>

        {runDetailsQuery.data?.toggleResult ? (
          <p>
            Toggle: {runDetailsQuery.data.toggleResult.stateBefore} → {runDetailsQuery.data.toggleResult.stateAfter}
          </p>
        ) : null}

        {runDetailsQuery.data?.capturedItems?.length ? (
          <div className="target-list">
            {runDetailsQuery.data.capturedItems.map((item) => (
              <article key={`${item.key}-${item.selector}`} className="target-list-item">
                <div>
                  <h3>{item.key}</h3>
                  <p>{item.value}</p>
                </div>
              </article>
            ))}
          </div>
        ) : null}

        {runDetailsQuery.data?.failureMessage ? (
          <p className="form-error">{runDetailsQuery.data.failureMessage}</p>
        ) : null}
      </section>
    </div>
  );
}
