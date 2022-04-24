export function getMethods(o) {
  return Object.getOwnPropertyNames(Object.getPrototypeOf(o)).filter(
    (m) => "function" === typeof o[m]
  );
}
