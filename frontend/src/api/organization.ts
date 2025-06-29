import api from "../utils/apiClient";
import { Organization } from "../types/organization";

export async function getMyOrganizations(): Promise<Organization[]> {
  const res = await api.get("/organizations/my");
  return res.data;
}
