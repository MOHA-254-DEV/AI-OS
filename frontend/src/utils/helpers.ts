export function formatDateTime(dt: string | Date): string {
  const date = typeof dt === "string" ? new Date(dt) : dt;
  return date.toLocaleString();
}
