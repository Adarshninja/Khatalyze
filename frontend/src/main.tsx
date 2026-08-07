import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";

import "./index.css";
import App from "./App";

import { queryClient } from "./lib/queryClient";
import { CurrentStatementProvider } from "./context/CurrentStatementContext";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <CurrentStatementProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </CurrentStatementProvider>
    </QueryClientProvider>
  </React.StrictMode>
);
