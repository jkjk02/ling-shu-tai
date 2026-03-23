import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { existsSync } from 'node:fs';

import { defineConfig } from '@playwright/test';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const isCI = !!process.env.CI;
const chromiumExecutable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
  ? path.resolve(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE)
  : '/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome';
const launchOptions = existsSync(chromiumExecutable)
  ? {
      executablePath: chromiumExecutable,
    }
  : undefined;
const reporter = isCI
  ? [
      ['list'],
      ['html', { open: 'never', outputFolder: 'playwright-report' }],
      ['junit', { outputFile: 'test-results/playwright/results.xml' }],
    ]
  : 'list';

export default defineConfig({
  testDir: path.resolve(__dirname, 'tests/browser'),
  timeout: 30_000,
  retries: isCI ? 1 : 0,
  expect: {
    timeout: 10_000,
  },
  fullyParallel: false,
  workers: 1,
  reporter,
  outputDir: 'test-results/playwright',
  use: {
    baseURL: 'http://127.0.0.1:4173',
    browserName: 'chromium',
    headless: true,
    trace: isCI ? 'on-first-retry' : 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'off',
    launchOptions,
  },
  webServer: [
    {
      command: 'backend/.venv/bin/python backend/tests/playwright_backend.py --host 127.0.0.1 --port 8000',
      url: 'http://127.0.0.1:8000/api/health',
      timeout: 30_000,
      reuseExistingServer: !isCI,
    },
    {
      command: 'npm run dev -- --host 127.0.0.1 --port 4173',
      url: 'http://127.0.0.1:4173',
      timeout: 30_000,
      reuseExistingServer: !isCI,
    },
  ],
});
