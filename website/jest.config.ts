import type {Config} from "@jest/types";

const config: Config.InitialOptions = {
  preset: "ts-jest/presets/js-with-babel-esm",
  verbose: true,
  globals: {
    "ts-jest": {
      useESM: true
    }
  },
  transform: {
    svelte$: [
      "svelte-jester", {preprocess: true}
    ]
  },
  transformIgnorePatterns: [
    "node_modules/(?!(@smui|svelte-star-rating|svelte-fullcalendar|@roxi/routify))"
  ],
  moduleFileExtensions: ["js", "ts", "svelte"],
  testEnvironment: "jsdom",
  setupFilesAfterEnv: [
    "./jest-setup.ts",
    "@testing-library/jest-dom/extend-expect"
  ],
  moduleDirectories: ["node_modules", "src"]
}

export default config;
