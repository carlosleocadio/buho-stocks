/* eslint-disable react/jsx-no-constructed-context-values */
import React from "react";
import { screen, waitFor } from "@testing-library/react";
import App from "./App";
import { AuthContext } from "contexts/auth";
import { renderWithRouterAndQueryClient } from "utils/test-utils";

describe("App tests", () => {
  it("renders expected texts when not authenticated", async () => {
    const authContext = {
      token: "token",
      isAuthenticated: false,
      state: { token: "token", isAuthenticated: false },
      clearToken: jest.fn(),
      authenticate: jest.fn(),
    };
    renderWithRouterAndQueryClient(
      <AuthContext.Provider value={authContext}>
        <App />
      </AuthContext.Provider>,
    );

    const element = screen.getByText(/Login in.../i);
    expect(element).toBeInTheDocument();
  });

  it("renders expected texts when authenticated", async () => {
    expect(1).toBe(1);
    const authContext = {
      token: "token",
      isAuthenticated: true,
      state: { token: "token", isAuthenticated: true },
      clearToken: jest.fn(),
      authenticate: jest.fn(),
    };
    renderWithRouterAndQueryClient(
      <AuthContext.Provider value={authContext}>
        <App />
      </AuthContext.Provider>,
    );
    await waitFor(() => {
      const elements = screen.getAllByText(/Buho Stocks/i);
      expect(elements).toHaveLength(2);
    });
    await waitFor(() => {
      const element = screen.getByText(/Bocabitlabs.../i);
      expect(element).toBeInTheDocument();
    });
  });
});
