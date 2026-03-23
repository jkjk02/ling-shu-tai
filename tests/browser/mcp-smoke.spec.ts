import { expect, test } from '@playwright/test';

test('key pages render through browser navigation', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: '平台总览' })).toBeVisible();
  await expect(page.getByText('资源规模')).toBeVisible();

  await page.getByTestId('nav-skills').click();
  await expect(page.getByRole('heading', { name: 'Skills 管理' })).toBeVisible();
  await expect(page.getByText('Skills 列表')).toBeVisible();

  await page.getByTestId('nav-agents').click();
  await expect(page.getByRole('heading', { name: 'Agents 管理' })).toBeVisible();
  await expect(page.getByText('Agents 列表')).toBeVisible();

  await page.getByTestId('nav-workflows').click();
  await expect(page.getByRole('heading', { name: 'Workflows 编排' })).toBeVisible();
  await expect(page.getByText('节点模板', { exact: true })).toBeVisible();
});

test('mcp page shows discovered states and create dialog', async ({ page }) => {
  await page.goto('/mcps');

  await expect(page.getByRole('heading', { name: 'MCPs 管理' })).toBeVisible();
  await expect(page.getByText('MCP 列表')).toBeVisible();
  await expect(page.locator('.el-table')).toContainText('Readonly MCP');
  await expect(page.locator('.el-table')).toContainText('Locked MCP');

  await page.locator('.el-table__body').getByText('Readonly MCP').click();
  await expect(page.getByText('MCP 详情')).toBeVisible();
  await expect(page.getByText('可写')).toBeVisible();

  await page.locator('.el-table__body').getByText('Locked MCP').click();
  await expect(page.getByText('只读')).toBeVisible();

  await page.getByTestId('mcp-create-button').click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await expect(page.getByRole('heading', { name: '新建 MCP' })).toBeVisible();
  const installTargetGroup = page.getByLabel('写入目标');
  await expect(installTargetGroup.getByText('managed', { exact: true })).toBeVisible();
  await expect(installTargetGroup.getByText('external', { exact: true })).toBeVisible();
});

test('mcp page can submit a managed MCP through the real backend', async ({ page }) => {
  const createdName = 'Browser Managed MCP';
  const createdDescription = 'Managed MCP created by Playwright browser automation';
  const createdModelName = 'gpt-5.4-mini';

  await page.goto('/mcps');

  await page.getByTestId('mcp-create-button').click();
  const dialog = page.getByRole('dialog');
  await dialog.getByRole('textbox', { name: '*名称', exact: true }).fill(createdName);
  await dialog.getByRole('textbox', { name: '描述', exact: true }).fill(createdDescription);
  await dialog.getByRole('textbox', { name: '*模型名称', exact: true }).fill(createdModelName);
  await dialog.getByRole('button', { name: '保存' }).click();

  await expect(dialog).toBeHidden();
  await expect(page.locator('.el-table')).toContainText(createdName);

  await page.reload();
  await expect(page.locator('.el-table')).toContainText(createdName);

  const createdRow = page.locator('.el-table__body tr').filter({ hasText: createdName });
  await createdRow.getByText(createdName).click();

  const detailCard = page.locator('.split-grid > .el-card').nth(1);
  await expect(detailCard.getByText('MCP 详情')).toBeVisible();
  await expect(detailCard).toContainText(createdModelName);
  await expect(detailCard).toContainText(createdDescription);

  await createdRow.getByRole('button', { name: '删除' }).click();
  await page.getByRole('button', { name: '确认删除' }).click();
  await expect(page.locator('.el-table')).not.toContainText(createdName);
});
