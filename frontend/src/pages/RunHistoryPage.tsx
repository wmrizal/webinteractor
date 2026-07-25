import { useState } from "react";
import { useTargetsQuery, type AutomationTarget } from "../features/targets/useTargets";
import { useTargetRunsQuery, useRunDetailsQuery } from "../features/runs/useRunActions";
import { RunDetailsPanel } from "../components/runs/RunDetailsPanel";

function RunDate({ iso }: { iso: string }) {
  return <time dateTime={iso}>{new Date(iso).toLocaleString()}</time>;
}

function TargetRunHistory({ target }: { target: AutomationTarget }) {
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const runsQuery = useTargetRunsQuery(target.id);
  const detailsQuery = useRunDetailsQuery(selectedRunId);

  return (
    <section className="card stack">
      <h2>{target.name}</h2>

      {runsQuery.isLoading ? <p>Loading runs...</p> : null}
      {!runsQuery.isLoading && !runsQuery.data?.length ? <p>No runs recorded yet.</p> : null}

      <div className="target-list">
        {runsQuery.data?.map((run) => (
          <article
            key={run.id}
            className="target-list-item"
            style={{ cursor: "pointer", flexDirection: "column", alignItems: "flex-start" }}
            onClick={() => setSelectedRunId((prev) => (prev === run.id ? null : run.id))}
          >
            <div className="target-actions" style={{ width: "100%" }}>
              <div>
                <strong>{run.requestedState}</strong>
                {" — "}
                <span>{run.status}</span>
              </div>
              <RunDate iso={run.startedAt} />
            </div>

            {selectedRunId === run.id && detailsQuery.data ? (
              <RunDetailsPanel run={detailsQuery.data} />
            ) : null}
          </article>
        ))}
      </div>
    </section>
  );
}

export function RunHistoryPage() {
  const targetsQuery = useTargetsQuery();
  const targets = targetsQuery.data ?? [];

  return (
    <div className="page-shell stack">
      <section className="hero-card">
        <p className="eyebrow">User Story 3</p>
        <h1>Run history</h1>
        <p>Review outcomes and step-level diagnostics for all past automation runs.</p>
      </section>

      {targetsQuery.isLoading ? <p>Loading targets...</p> : null}
      {!targetsQuery.isLoading && targets.length === 0 ? (
        <p>No targets available.</p>
      ) : null}

      {targets.map((target) => (
        <TargetRunHistory key={target.id} target={target} />
      ))}
    </div>
  );
}
