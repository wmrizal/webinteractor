import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { RunHistoryPage } from "../../src/pages/RunHistoryPage";

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
        <RunHistoryPage />
      </QueryClientProvider>
    </MemoryRouter>,
  );
}

describe("RunHistoryPage", () => {
  it("renders target run history and shows run details on click", async () => {
    mockApiRequest.mockResolvedValueOnce([
      {
        id: "target-1",
        name: "Checkout flag",
        baseUrl: "https://example.test",
        pagePath: "/flags",
        authProfile: null,
        extractionRules: [{ key: "featureName", selector: "#feature-name" }],
        toggleRule: { controlSelector: "#feature-toggle", stateSelector: "#feature-state", verificationMethod: "text-label" },
        defaultDesiredState: "on",
        createdAt: "2026-07-24T11:00:00Z",
        updatedAt: "2026-07-24T11:00:00Z",
      },
    ]);

    mockApiRequest.mockResolvedValueOnce([
      {
        id: "run-1",
        targetId: "target-1",
        requestedState: "on",
        status: "success",
        startedAt: "2026-07-24T11:01:00Z",
        finishedAt: "2026-07-24T11:01:09Z",
        durationMs: 9000,
      },
    ]);

    mockApiRequest.mockResolvedValueOnce({
      id: "run-1",
      targetId: "target-1",
      requestedState: "on",
      status: "success",
      startedAt: "2026-07-24T11:01:00Z",
      finishedAt: "2026-07-24T11:01:09Z",
      durationMs: 9000,
      capturedItems: [{ key: "featureName", selector: "#feature-name", value: "Checkout", capturedAt: "2026-07-24T11:01:03Z" }],
      toggleResult: { stateBefore: "off", stateAfter: "on", actionTaken: "toggle-once", verified: true },
      failureStep: null,
      failureMessage: null,
    });

    renderPage();

    await screen.findByRole("heading", { name: /run history/i });
    await screen.findByText("Checkout flag");

    await userEvent.click(await screen.findByRole('article'));

    await waitFor(() => {
      expect(mockApiRequest).toHaveBeenCalledWith(expect.stringContaining("/runs/run-1"));
    });

    expect(await screen.findAllByText(/Checkout/, undefined, { timeout: 4000 })).not.toHaveLength(0);
    expect(screen.getByText(/off → on/i)).toBeInTheDocument();
  });
});
