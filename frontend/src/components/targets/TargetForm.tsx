import { FormEvent, useEffect, useState } from "react";
import {
  AutomationTarget,
  AutomationTargetInput,
  CapturedItemRule,
  DesiredState,
  VerificationMethod,
} from "../../features/targets/useTargets";

const emptyRule = (): CapturedItemRule => ({ key: "", selector: "" });

type TargetFormValues = {
  name: string;
  baseUrl: string;
  pagePath: string;
  authProfile: string;
  defaultDesiredState: DesiredState;
  extractionRules: CapturedItemRule[];
  controlSelector: string;
  stateSelector: string;
  verificationMethod: VerificationMethod;
};

const defaultValues: TargetFormValues = {
  name: "",
  baseUrl: "https://",
  pagePath: "/",
  authProfile: "",
  defaultDesiredState: "off",
  extractionRules: [emptyRule()],
  controlSelector: "",
  stateSelector: "",
  verificationMethod: "text-label",
};

function toFormValues(target?: AutomationTarget | null): TargetFormValues {
  if (!target) {
    return defaultValues;
  }

  return {
    name: target.name,
    baseUrl: target.baseUrl,
    pagePath: target.pagePath,
    authProfile: target.authProfile ?? "",
    defaultDesiredState: target.defaultDesiredState,
    extractionRules: target.extractionRules.length > 0 ? target.extractionRules : [emptyRule()],
    controlSelector: target.toggleRule.controlSelector,
    stateSelector: target.toggleRule.stateSelector,
    verificationMethod: target.toggleRule.verificationMethod,
  };
}

function toPayload(values: TargetFormValues): AutomationTargetInput {
  return {
    name: values.name.trim(),
    baseUrl: values.baseUrl.trim(),
    pagePath: values.pagePath.trim(),
    authProfile: values.authProfile.trim() || null,
    extractionRules: values.extractionRules
      .map((rule) => ({ key: rule.key.trim(), selector: rule.selector.trim() }))
      .filter((rule) => rule.key && rule.selector),
    toggleRule: {
      controlSelector: values.controlSelector.trim(),
      stateSelector: values.stateSelector.trim(),
      verificationMethod: values.verificationMethod,
    },
    defaultDesiredState: values.defaultDesiredState,
  };
}

type Props = {
  initialTarget?: AutomationTarget | null;
  isSubmitting?: boolean;
  onCancelEdit?: () => void;
  onSubmit: (payload: AutomationTargetInput) => Promise<void> | void;
};

export function TargetForm({ initialTarget, isSubmitting = false, onCancelEdit, onSubmit }: Props) {
  const [values, setValues] = useState<TargetFormValues>(defaultValues);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setValues(toFormValues(initialTarget));
    setError(null);
  }, [initialTarget]);

  function updateRule(index: number, field: keyof CapturedItemRule, value: string) {
    setValues((current) => ({
      ...current,
      extractionRules: current.extractionRules.map((rule, ruleIndex) =>
        ruleIndex === index ? { ...rule, [field]: value } : rule,
      ),
    }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const payload = toPayload(values);

    if (payload.extractionRules.length === 0) {
      setError("Add at least one capture rule before saving.");
      return;
    }

    if (!payload.baseUrl.startsWith("https://")) {
      setError("Base URL must use HTTPS.");
      return;
    }

    setError(null);
    await onSubmit(payload);

    if (!initialTarget) {
      setValues(defaultValues);
    }
  }

  return (
    <form className="target-form" onSubmit={handleSubmit}>
      <div className="card-header">
        <div>
          <h2>{initialTarget ? "Edit target" : "New automation target"}</h2>
          <p>Save the page location, capture selectors, and toggle rule needed for each run.</p>
        </div>
        {initialTarget && onCancelEdit ? (
          <button type="button" className="ghost-button" onClick={onCancelEdit}>
            Cancel edit
          </button>
        ) : null}
      </div>

      <label>
        Target name
        <input
          value={values.name}
          onChange={(event) => setValues((current) => ({ ...current, name: event.target.value }))}
          required
        />
      </label>

      <label>
        Base URL
        <input
          value={values.baseUrl}
          onChange={(event) => setValues((current) => ({ ...current, baseUrl: event.target.value }))}
          required
        />
      </label>

      <div className="grid two-columns">
        <label>
          Page path
          <input
            value={values.pagePath}
            onChange={(event) => setValues((current) => ({ ...current, pagePath: event.target.value }))}
            required
          />
        </label>

        <label>
          Auth profile
          <input
            value={values.authProfile}
            onChange={(event) => setValues((current) => ({ ...current, authProfile: event.target.value }))}
          />
        </label>
      </div>

      <label>
        Default desired state
        <select
          value={values.defaultDesiredState}
          onChange={(event) =>
            setValues((current) => ({ ...current, defaultDesiredState: event.target.value as DesiredState }))
          }
        >
          <option value="on">On</option>
          <option value="off">Off</option>
        </select>
      </label>

      <div className="stack">
        <div className="section-header">
          <h3>Capture rules</h3>
          <button
            type="button"
            className="ghost-button"
            onClick={() =>
              setValues((current) => ({
                ...current,
                extractionRules: [...current.extractionRules, emptyRule()],
              }))
            }
          >
            Add rule
          </button>
        </div>

        {values.extractionRules.map((rule, index) => (
          <div className="grid two-columns" key={`${index}-${rule.key}-${rule.selector}`}>
            <label>
              Capture key
              <input value={rule.key} onChange={(event) => updateRule(index, "key", event.target.value)} required />
            </label>
            <label>
              Capture selector
              <input
                value={rule.selector}
                onChange={(event) => updateRule(index, "selector", event.target.value)}
                required
              />
            </label>
          </div>
        ))}
      </div>

      <div className="stack">
        <h3>Toggle rule</h3>
        <div className="grid two-columns">
          <label>
            Toggle control selector
            <input
              value={values.controlSelector}
              onChange={(event) => setValues((current) => ({ ...current, controlSelector: event.target.value }))}
              required
            />
          </label>
          <label>
            Toggle state selector
            <input
              value={values.stateSelector}
              onChange={(event) => setValues((current) => ({ ...current, stateSelector: event.target.value }))}
              required
            />
          </label>
        </div>

        <label>
          Verification method
          <select
            value={values.verificationMethod}
            onChange={(event) =>
              setValues((current) => ({
                ...current,
                verificationMethod: event.target.value as VerificationMethod,
              }))
            }
          >
            <option value="text-label">Text label</option>
            <option value="dom-attribute">DOM attribute</option>
            <option value="aria-checked">ARIA checked</option>
          </select>
        </label>
      </div>

      {error ? <p className="form-error">{error}</p> : null}

      <button type="submit" className="primary-button" disabled={isSubmitting}>
        {isSubmitting ? "Saving..." : "Save target"}
      </button>
    </form>
  );
}
