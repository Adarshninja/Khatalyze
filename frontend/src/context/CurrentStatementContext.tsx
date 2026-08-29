import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import type { ReactNode } from "react";

type CurrentStatementContextType = {
  statementId: string | null;
  setStatementId: (id: string |null) => void;
};

const CurrentStatementContext =
  createContext<CurrentStatementContextType | undefined>(undefined);

export function CurrentStatementProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [statementId, setStatementIdState] = useState<string | null>(() => {
    return localStorage.getItem("currentStatementId");
  });

  const setStatementId = (id: string | null) => {
    setStatementIdState(id);

    if (id) {
      localStorage.setItem("currentStatementId", id);
    } else {
      localStorage.removeItem("currentStatementId");
    }
  };

  useEffect(() => {
    const stored = localStorage.getItem("currentStatementId");

    if (stored && stored !== statementId) {
      setStatementIdState(stored);
    }
  }, []);

  return (
    <CurrentStatementContext.Provider
      value={{
        statementId,
        setStatementId,
      }}
    >
      {children}
    </CurrentStatementContext.Provider>
  );
}

export function useCurrentStatement() {
  const context = useContext(CurrentStatementContext);

  if (!context) {
    throw new Error(
      "useCurrentStatement must be used inside CurrentStatementProvider"
    );
  }

  return context;
}
