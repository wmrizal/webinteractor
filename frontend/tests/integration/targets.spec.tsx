import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { TargetsPage } from "../../src/pages/TargetsPage";

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
        <TargetsPage />
      </QueryClientProvider>
    </MemoryRouter>,
  );
}

describe("TargetsPage", () => {
  it("creates a target and renders it in the list", async () => {
    mockApiRequest.mockResolvedValueOnce([]);
    mockApiRequest.mockResolvedValueOnce({
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
      defaultDesiredState: "on",
      createdAt: "2026-07-11T10:00:00Z",
      updatedAt: "2026-07-11T10:00:00Z",
    });
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
        defaultDesiredState: "on",
        createdAt: "2026-07-11T10:00:00Z",
        updatedAt: "2026-07-11T10:00:00Z",
      },
    ]);

    renderPage();

    await screen.findByText("No targets saved yet.");

    await userEvent.type(screen.getByLabelText(/target name/i), "Checkout flag");
    await userEvent.type(screen.getByLabelText(/base url/i), "https://example.test");
    await userEvent.type(screen.getByLabelText(/page path/i), "/flags");
    await userEvent.type(screen.getByLabelText(/auth profile/i), "qa-session");
    await userEvent.type(screen.getByLabelText(/capture key/i), "featureName");
    await userEvent.type(screen.getByLabelText(/capture selector/i), "#feature-name");
    await userEvent.type(screen.getByLabelText(/toggle control selector/i), "#feature-toggle");
    await userEvent.type(screen.getByLabelText(/toggle state selector/i), "#feature-state");
    await userEvent.selectOptions(screen.getByLabelText(/verification method/i), "text-label");
    await userEvent.selectOptions(screen.getByLabelText(/default desired state/i), "on");

    await userEvent.click(screen.getByRole("button", { name: /save target/i }));

    await waitFor(() => {
      expect(mockApiRequest).toHaveBeenCalledWith("/targets", expect.objectContaining({ method: "POST" }));
    });
    expect(await screen.findByText("Checkout flag")).toBeInTheDocument();
    expect(screen.getByText("https://example.test/flags")).toBeInTheDocument();
  });
});
