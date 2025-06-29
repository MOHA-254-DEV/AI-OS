import React, { createContext, useState, useEffect, useContext, ReactNode } from "react";
import { Organization } from "../types/organization";
import * as orgApi from "../api/organization";

interface OrganizationContextType {
  organizations: Organization[];
  refresh: () => Promise<void>;
}

const OrganizationContext = createContext<OrganizationContextType | undefined>(undefined);

export const OrganizationProvider = ({ children }: { children: ReactNode }) => {
  const [organizations, setOrganizations] = useState<Organization[]>([]);

  const refresh = async () => {
    const data = await orgApi.getMyOrganizations();
    setOrganizations(data);
  };

  useEffect(() => {
    refresh();
  }, []);

  return (
    <OrganizationContext.Provider value={{ organizations, refresh }}>
      {children}
    </OrganizationContext.Provider>
  );
};

export const useOrganization = () => {
  const ctx = useContext(OrganizationContext);
  if (!ctx) throw new Error("useOrganization must be used within OrganizationProvider");
  return ctx;
};
