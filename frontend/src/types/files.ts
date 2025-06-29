export interface File {
  id: number;
  filename: string;
  path: string;
  userId: number;
  organizationId: number;
  uploadedAt: string;
  isDeleted: boolean;
}
