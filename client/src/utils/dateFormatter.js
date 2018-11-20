export function toDateInputValue(date) {
  return date.toISOString().slice(0, 10);
}
