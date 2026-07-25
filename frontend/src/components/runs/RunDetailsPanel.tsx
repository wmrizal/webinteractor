import type { AutomationRun, RunDetails } from "../../features/runs/useRunActions";

type Props = {
  run: RunDetails;
};

function statusBadgeClass(status: AutomationRun["status"]) {
  if (status === "success" || status === "no-change-needed") return "form-success";
  if (status === "failed") return "form-error";
  return "";
}

export function RunDetailsPanel({ run }: Props) {
  return (
    <section className="stack">
      <div className="grid two-columns">
        <div>
          <p>
            <strong>Status</strong>
          </p>
          <p className={statusBadgeClass(run.status)}>{run.status}</p>
        </div>
        <div>
          <p>
            <strong>Duration</strong>
          </p>
          <p>{run.durationMs != null ? `${run.durationMs} ms` : "—"}</p>
        </div>
      </div>

      {run.toggleResult ? (
        <div>
          <p>
            <strong>Toggle</strong>
          </p>
          <p>
            {run.toggleResult.stateBefore} → {run.toggleResult.stateAfter}
            {" "}({run.toggleResult.actionTaken}) —{" "}
            {run.toggleResult.verified ? "verified" : "not verified"}
          </p>
        </div>
      ) : null}

      {run.capturedItems.length > 0 ? (
        <div>
          <p>
            <strong>Captured items</strong>
          </p>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {run.capturedItems.map((item) => (
              <li key={`${item.key}-${item.selector}`}>
                <strong>{item.key}</strong>: {item.value}
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {run.failureStep || run.failureMessage ? (
        <div>
          <p>
            <strong>Failure</strong>
          </p>
          {run.failureStep ? <p>Step: {run.failureStep}</p> : null}
          {run.failureMessage ? <p className="form-error">{run.failureMessage}</p> : null}
        </div>
      ) : null}
    </section>
  );
}
