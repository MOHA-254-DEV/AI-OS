export interface Quota {
  id: number;
  organizationId: number;
  quotaType: string;
  value: number;
  used: number;
  active: boolean;
  updatedAt: string;
}
