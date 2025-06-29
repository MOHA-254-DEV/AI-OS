export interface Firewall {
  id: number;
  networkId: number;
  rule: string;
  action: string;
  enabled: boolean;
  createdAt: string;
}
