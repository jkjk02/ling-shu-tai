import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { existsSync } from 'node:fs';

import { defineConfig } from '@playwright/test';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const fixturesRoot = path.resolve(__dirname, 'backend/tests/fixtures');
const chromiumExecutable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
  ? path.resolve(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE)
  : '/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome';
const launchOptions = existsSync(chromiumExecutable)
  ? {
      executablePath: chromiumExecutable,
    }
  : undefined;

export default defineConfig({
  testDir: path.resolve(__dirname, 'tests/browser'),
  timeout: 30_000,
  expect: {
    timeout: 10_000,
  },
  fullyParallel: false,
  workers: 1,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:4173',
    browserName: 'chromium',
    headless: true,
    trace: 'retain-on-failure',
    launchOptions,
  },
  webServer: [
    {
      command: 'backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000',
      url: 'http://127.0.0.1:8000/api/health',
      timeout: 30_000,
      reuseExistingServer: !process.env.CI,
      env: {
        ...process.env,
        LINGSHU_CODEX_ROOT: path.join(fixturesRoot, 'codex'),
        LINGSHU_CLUDEA_ROOT: path.join(fixturesRoot, 'cludea'),
        LINGSHU_OPENCODE_ROOT: path.join(fixturesRoot, 'opencode'),
      },
    },
    {
      command: 'npm run dev -- --host 127.0.0.1 --port 4173',
      url: 'http://127.0.0.1:4173',
      timeout: 30_000,
      reuseExistingServer: !process.env.CI,
    },
  ],
});
