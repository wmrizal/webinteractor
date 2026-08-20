import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { App } from "../../src/App";

function renderApp(initialPath = "/") {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[initialPath]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("LandingPage", () => {
  it("renders the landing page at / with app title and three cards", () => {
    renderApp("/");

    expect(screen.getByRole("heading", { name: /webinteractor/i })).toBeInTheDocument();
    expect(screen.getByText(/automation made simple/i)).toBeInTheDocument();

    ["Targets", "Runs", "Run History"].forEach((label) => {
      expect(screen.getByRole("heading", { name: label })).toBeInTheDocument();
    });
  });

  it("navigates to the relevant pages from each landing card CTA", async () => {
    const user = userEvent.setup();
    renderApp("/");

    await user.click(screen.getByRole("link", { name: /manage targets/i }));
    expect(screen.getByRole("heading", { name: /automation targets/i })).toBeInTheDocument();

    await user.click(screen.getByRole("link", { name: /home/i }));
    await user.click(screen.getByRole("link", { name: /start a run/i }));
    expect(screen.getByRole("heading", { name: /run browser automation/i })).toBeInTheDocument();

    await user.click(screen.getByRole("link", { name: /home/i }));
    await user.click(screen.getByRole("link", { name: /view history/i }));
    expect(screen.getByRole("heading", { name: /run history/i })).toBeInTheDocument();
  });

  it("includes a how-to list with at least two steps on each section card", () => {
    renderApp("/");

    ["Targets", "Runs", "Run History"].forEach((label) => {
      const card = screen.getByRole("heading", { name: label }).closest("article");
      expect(card).not.toBeNull();

      const listItems = within(card as HTMLElement).getAllByRole("listitem");
      expect(listItems.length).toBeGreaterThanOrEqual(2);
    });
  });
});
