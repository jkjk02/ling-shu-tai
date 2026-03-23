import { expect, test } from '@playwright/test';

test('workflow canvas supports drag, save, reload, and cleanup through the real backend', async ({ page }) => {
  const workflowName = `Browser Workflow ${Date.now()}`;
  const workflowDescription = 'Workflow created by browser automation';
  const taskLabel = '执行 1';
  const startLabel = '开始 1';

  await page.goto('/workflows');

  await expect(page.getByRole('heading', { name: 'Workflows 编排' })).toBeVisible();
  await expect(page.getByTestId('workflow-list-table')).toContainText('Draft Delivery Workflow');

  await page.getByTestId('workflow-new-button').click();
  await expect(page.getByText('新建中', { exact: true })).toBeVisible();
  await expect(page.locator('.workflow-node')).toHaveCount(0);
  await page.getByPlaceholder('例如：交付流水线').fill(workflowName);
  await page.getByPlaceholder('描述这个 Workflow 的目标与适用场景').fill(workflowDescription);

  await page.getByTestId('workflow-template-start').click();
  await page.getByTestId('workflow-template-task').click();

  await expect(page.locator('.workflow-node')).toHaveCount(2);

  const startNode = page.locator(`.workflow-node[data-node-label="${startLabel}"]`).first();
  const taskNode = page.locator(`.workflow-node[data-node-label="${taskLabel}"]`).first();

  await expect(startNode).toBeVisible();
  await expect(taskNode).toBeVisible();

  await startNode.locator('.workflow-node__port--out').click();
  await taskNode.locator('.workflow-node__port--in').click();

  const initialPosition = await taskNode.evaluate((node) => ({
    left: (node as HTMLElement).style.left,
    top: (node as HTMLElement).style.top,
  }));

  const dragHandle = taskNode.locator('.workflow-node__body');
  const dragBox = await dragHandle.boundingBox();
  if (!dragBox) {
    throw new Error('Task node drag handle is not visible');
  }

  await page.mouse.move(dragBox.x + dragBox.width / 2, dragBox.y + dragBox.height / 2);
  await page.mouse.down();
  await page.mouse.move(dragBox.x + dragBox.width / 2 + 168, dragBox.y + dragBox.height / 2 + 96, { steps: 12 });
  await page.mouse.up();

  await expect
    .poll(async () =>
      taskNode.evaluate((node) => ({
        left: (node as HTMLElement).style.left,
        top: (node as HTMLElement).style.top,
      })),
    )
    .not.toEqual(initialPosition);

  const draggedPosition = await taskNode.evaluate((node) => ({
    left: (node as HTMLElement).style.left,
    top: (node as HTMLElement).style.top,
  }));

  await page.getByTestId('workflow-save-button').click();
  await expect(page.getByTestId('workflow-list-table')).toContainText(workflowName);

  await page.reload();
  await expect(page.getByTestId('workflow-list-table')).toContainText(workflowName);
  await page.getByTestId('workflow-list-table').locator('.el-table__body').getByText(workflowName, { exact: true }).click({ force: true });

  await expect(page.getByPlaceholder('例如：交付流水线')).toHaveValue(workflowName);
  await expect(page.getByPlaceholder('描述这个 Workflow 的目标与适用场景')).toHaveValue(workflowDescription);

  const reloadedTaskNode = page.locator(`.workflow-node[data-node-label="${taskLabel}"]`).first();
  const reloadedStartNode = page.locator(`.workflow-node[data-node-label="${startLabel}"]`).first();

  await expect(reloadedStartNode).toBeVisible();
  await expect(reloadedTaskNode).toBeVisible();
  await expect(reloadedTaskNode).toHaveAttribute('data-node-label', taskLabel);

  const reloadedPosition = await reloadedTaskNode.evaluate((node) => ({
    left: (node as HTMLElement).style.left,
    top: (node as HTMLElement).style.top,
  }));
  expect(reloadedPosition).toEqual(draggedPosition);

  await expect(page.locator('.workflow-edge-label')).toContainText('未命名连线');

  await page.getByTestId('workflow-delete-button').click();
  await page.getByRole('button', { name: '确认删除' }).click();
  await expect(page.getByTestId('workflow-list-table')).not.toContainText(workflowName);
});
