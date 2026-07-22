import { test, expect, type ConsoleMessage } from "@playwright/test";

/**
 * Smoke tests for the School Climate Hub operator console (index.html).
 *
 * These are deliberately narrow: they assert the console *loads*, the
 * Leaflet map root renders, the primary nav views are present and
 * switchable, the core JSON data fetches succeed, and there are no severe
 * (page-crashing) console errors — not full behavioural coverage of every
 * dashboard interaction.
 */

// Errors we know are benign / expected in a sandboxed CI runner and should
// not fail the smoke test:
//   - Google Fonts / Tailwind CDN / OSM tile 429s under CI network throttling
//   - the chat backend Worker is not reachable in this test (no fetch is
//     triggered on load; this list is a safety net if that ever changes)
const IGNORED_CONSOLE_PATTERNS = [
  /workers\.dev/i,
  /fonts\.googleapis\.com/i,
  /fonts\.gstatic\.com/i,
];

function isIgnorable(msg: ConsoleMessage): boolean {
  const text = msg.text();
  return IGNORED_CONSOLE_PATTERNS.some((re) => re.test(text));
}

test.describe("operator console — smoke", () => {
  test("loads the page with the expected title and shell", async ({ page }) => {
    const errors: string[] = [];
    page.on("console", (msg) => {
      if (msg.type() === "error" && !isIgnorable(msg)) errors.push(msg.text());
    });
    page.on("pageerror", (err) => errors.push(String(err)));

    const response = await page.goto("/index.html");
    expect(response?.ok()).toBeTruthy();
    await expect(page).toHaveTitle(/School Climate Hub/i);

    // Give in-page fetches (scores.json / schools.json / attendance.json) and
    // the Leaflet/Tailwind CDN scripts a moment to settle.
    await page.waitForLoadState("networkidle");

    expect(errors, `Unexpected console/page errors:\n${errors.join("\n")}`).toEqual([]);
  });

  test("renders the Leaflet map container on the Overview view", async ({ page }) => {
    await page.goto("/index.html");
    const map = page.locator("#map");
    await expect(map).toBeVisible();

    // Leaflet stamps its own class + at least one tile pane onto the
    // container once L.map(...) has initialised — a reasonable proxy for
    // "the map actually rendered" without depending on tile network fetches.
    await expect(map).toHaveClass(/leaflet-container/);
    await expect(page.locator("#map .leaflet-pane").first()).toBeAttached();
  });

  test("primary nav views are present and switchable", async ({ page }) => {
    await page.goto("/index.html");

    const expectedViews = ["overview", "schools", "data", "about", "settings"];
    for (const view of expectedViews) {
      await expect(page.locator(`.nav-item[data-view="${view}"]`)).toBeAttached();
    }

    // Overview is active by default.
    await expect(page.locator("#v-overview")).toHaveClass(/active/);

    // Switching to Schools should activate that section and its nav item.
    await page.locator('.nav-item[data-view="schools"]').click();
    await expect(page.locator("#v-schools")).toHaveClass(/active/);
    await expect(page.locator('.nav-item[data-view="schools"]')).toHaveClass(/active/);
  });

  test("schools table populates from schools.json / scores.json", async ({ page }) => {
    await page.goto("/index.html");
    await page.locator('.nav-item[data-view="schools"]').click();

    const rows = page.locator("#rag-tbody tr");
    // 50 schools are shipped in the repo's schools.json / scores.json fixtures.
    await expect(rows.first()).toBeAttached({ timeout: 10_000 });
    await expect(rows).toHaveCount(50);
  });

  test("chat panel opens and closes without a network round-trip", async ({ page }) => {
    await page.goto("/index.html");
    const panel = page.locator("#chat-panel");

    // The panel is always in the DOM (display: flex); it's slid off-screen
    // via `transform: translateX(100%)` and only rendered on-screen once the
    // JS-driven "open" class is toggled — so we assert on that class rather
    // than raw visibility.
    await expect(panel).not.toHaveClass(/open/);

    await page.locator("#chat-fab").click();
    await expect(panel).toHaveClass(/open/);

    await page.locator("#chat-close-btn").click();
    await expect(panel).not.toHaveClass(/open/);
  });
});
