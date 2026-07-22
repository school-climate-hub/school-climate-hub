import { defineConfig, devices } from "@playwright/test";
import path from "node:path";

// The site under test is the static repo root (index.html + schools.json +
// scores.json + attendance.json, all sibling files). We serve it with the
// stdlib http.server rather than adding a JS dev-server dependency, since
// this is a static GitHub Pages site with no build step.
const PORT = 4173;
const REPO_ROOT = path.resolve(__dirname, "..");

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : "list",
  timeout: 30_000,

  use: {
    baseURL: `http://127.0.0.1:${PORT}`,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },

  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
  ],

  webServer: {
    command: `python3 -m http.server ${PORT} --bind 127.0.0.1 --directory "${REPO_ROOT}"`,
    url: `http://127.0.0.1:${PORT}/index.html`,
    reuseExistingServer: !process.env.CI,
    timeout: 20_000,
  },
});
