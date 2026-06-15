export function px(value: string | undefined, fallback: string) {
  return `${value || fallback}px`;
}

export function font(value: string | undefined) {
  return value || "Arial, Helvetica, sans-serif";
}

export function htmlFont(value: string | undefined) {
  return value || "Arial, Helvetica, sans-serif";
}

export function htmlSize(value: string | undefined, fallback: string) {
  return `${value || fallback}px`;
}
