/** Assorted text helpers for display. */

/** Capitalize the first letter of a string. */
export function capitalize(value: string): string {
  if (!value) return value;
  return value.charAt(0).toUpperCase() + value.slice(1);
}

/** Join a list of names into a human-readable string ("a, b and c"). */
export function joinNames(names: string[]): string {
  if (names.length === 0) return "";
  if (names.length === 1) return names[0];
  const head = names.slice(0, -1).join(", ");
  const tail = names[names.length - 1];
  return `${head} and ${tail}`;
}

/** Pluralize a noun based on a count. */
export function pluralize(count: number, noun: string): string {
  if (count === 1) {
    return `${count} ${noun}`;
  } else {
    return `${count} ${noun}s`;
  }
}

/** Truncate a string to a maximum length, appending an ellipsis. */
export function truncate(value: string, max: number): string {
  if (value.length <= max) return value;
  return value.slice(0, max) + "...";
}
