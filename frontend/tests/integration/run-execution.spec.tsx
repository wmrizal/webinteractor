import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { RunPage } from "../../src/pages/RunPage";

const mockApiRequest = vi.fn();

vi.mock("../../src/services/apiClient", () => ({
  apiRequest: (...args: unknown[]) => mockApiRequest(...args),
  ApiClientError: class ApiClientError extends Error {
    status = 400;
    code = "request_failed";
  },
}));

function renderPage() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  return render(
    <MemoryRouter>
      <QueryClientProvider client={queryClient}>
        <RunPage />
      </QueryClientProvider>
    </MemoryRouter>,
  );
}

describe("RunPage", () => {
  it("triggers a run with selected desired state and renders run details", async () => {
    mockApiRequest.mockResolvedValueOnce([
      {
        id: "target-1",
        name: "Checkout flag",
        baseUrl: "https://example.test",
        pagePath: "/flags",
        authProfile: "qa-session",
        extractionRules: [{ key: "featureName", selector: "#feature-name" }],
        toggleRule: {
          controlSelector: "#feature-toggle",
          stateSelector: "#feature-state",
          verificationMethod: "text-label",
        },
        defaultDesiredState: "off",
        createdAt: "2026-07-24T11:00:00Z",
        updatedAt: "2026-07-24T11:00:00Z",
      },
    ]);

    mockApiRequest.mockResolvedValueOnce({
      id: "run-1",
      targetId: "target-1",
      requestedState: "off",
      status: "queued",
      startedAt: "2026-07-24T11:01:00Z",
      finishedAt: null,
      durationMs: null,
    });

    mockApiRequest.mockResolvedValueOnce({
      id: "run-1",
      targetId: "target-1",
      requestedState: "off",
      status: "success",
      startedAt: "2026-07-24T11:01:00Z",
      finishedAt: "2026-07-24T11:01:08Z",
      durationMs: 8000,
      capturedItems: [{ key: "featureName", selector: "#feature-name", value: "Checkout flag", capturedAt: "2026-07-24T11:01:03Z" }],
      toggleResult: {
        stateBefore: "on",
        stateAfter: "off",
        actionTaken: "toggle-once",
        verified: true,
      },
      failureStep: null,
      failureMessage: null,
    });

    renderPage();

    await screen.findByRole("heading", { name: /run browser automation/i });
    await userEvent.selectOptions(screen.getByLabelText(/desired state/i), "off");
    await userEvent.click(screen.getByRole("button", { name: /trigger run/i }));

    await waitFor(() => {
      expect(mockApiRequest).toHaveBeenCalledWith(
        "/runs",
        expect.objectContaining({ method: "POST", body: { targetId: "target-1", requestedState: "off" } }),
      );
    });

    expect(await screen.findByText(/current status: success/i)).toBeInTheDocument();
    expect(screen.getAllByText("Checkout flag").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText((_, el) => el?.tagName === 'P' && /Toggle:/i.test(el?.textContent ?? ''))).toBeInTheDocument();
  });
});
