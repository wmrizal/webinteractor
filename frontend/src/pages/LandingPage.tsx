import { Link } from "react-router-dom";

const sectionCards = [
  {
    title: "Targets",
    description: "Store browser URLs and selectors once, then reuse them in every automation run.",
    route: "/targets",
    cta: "Manage Targets",
    steps: [
      "Fill in Base URL, page path, and CSS selector.",
      "Save the target.",
      "Reuse it in any Run.",
    ],
  },
  {
    title: "Runs",
    description: "Trigger a one-off automation run against a saved target and monitor the outcome.",
    route: "/runs",
    cta: "Start a Run",
    steps: [
      "Pick a saved Target from the dropdown.",
      "Choose the desired state (on/off).",
      "Click Run and monitor the status.",
    ],
  },
  {
    title: "Run History",
    description: "Review recent automation results, captured values, and toggle outcomes across runs.",
    route: "/history",
    cta: "View History",
    steps: [
      "Select a target to see its past runs.",
      "Click a run to inspect toggle results and captured screenshots.",
      "Compare outcomes to keep automation consistent.",
    ],
  },
];

export function LandingPage() {
  return (
    <div className="page-shell landing-shell">
      <header className="hero-card landing-hero">
        <p className="eyebrow">Automation made simple</p>
        <h1>WebInteractor</h1>
        <p>
          Organize browser automation targets, trigger on-demand runs, and inspect the results from
          one central place.
        </p>
      </header>

      <section className="landing-grid" aria-label="Application sections">
        {sectionCards.map((card) => (
          <article key={card.title} className="section-card">
            <div className="section-card-header">
              <span className="section-badge" aria-hidden="true">
                {card.title === "Targets" ? "🎯" : card.title === "Runs" ? "⚙️" : "📊"}
              </span>
              <h2>{card.title}</h2>
            </div>

            <p>{card.description}</p>

            <ol>
              {card.steps.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ol>

            <Link to={card.route} className="primary-button section-link">
              {card.cta}
            </Link>
          </article>
        ))}
      </section>
    </div>
  );
}
