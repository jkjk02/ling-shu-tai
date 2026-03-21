from __future__ import annotations

import json
import unittest

from support import BackendServerHarness


class ApiRegressionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.harness = BackendServerHarness()
        cls.harness.start()

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            cls.harness.assert_default_data_unchanged()
        finally:
            cls.harness.stop()

    def test_health_endpoint(self) -> None:
        status, payload = self.harness.request_json("GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["service"], "ling-shu-tai-backend")

    def test_dashboard_and_discovery_include_seeded_and_discovered_resources(self) -> None:
        status, discovery = self.harness.request_json("GET", "/discovery")
        self.assertEqual(status, 200)
        self.assertEqual(len(discovery), 3)
        status_by_tool = {item["tool"]: item for item in discovery}
        self.assertEqual(status_by_tool["codex"]["status"], "available")
        self.assertEqual(status_by_tool["codex"]["discovered_skill_files"], 1)
        self.assertEqual(status_by_tool["cludea"]["discovered_skill_files"], 1)
        self.assertEqual(status_by_tool["cludea"]["discovered_mcp_files"], 1)
        self.assertEqual(status_by_tool["opencode"]["discovered_mcp_files"], 1)

        status, dashboard = self.harness.request_json("GET", "/dashboard")
        self.assertEqual(status, 200)
        self.assertEqual(dashboard["total_skills"], 3)
        self.assertEqual(dashboard["total_mcps"], 3)
        self.assertEqual(dashboard["total_agents"], 1)
        self.assertEqual(dashboard["total_workflows"], 1)

        summaries = {item["tool"]: item for item in dashboard["tool_summaries"]}
        self.assertEqual(summaries["codex"]["skills"], 2)
        self.assertEqual(summaries["cludea"]["skills"], 1)
        self.assertEqual(summaries["cludea"]["mcps"], 1)
        self.assertEqual(summaries["opencode"]["mcps"], 2)

    def test_skills_crud_and_discovered_read_only(self) -> None:
        create_payload = {
            "name": "Regression Skill",
            "description": "Managed skill created by automated test",
            "cli_tool": "codex",
            "trigger_command": "/regression",
            "script_content": "Run regression",
            "script_language": "markdown",
            "tags": ["automation"],
        }
        status, created = self.harness.request_json("POST", "/skills", create_payload)
        self.assertEqual(status, 201)
        self.assertEqual(created["id"], "regression-skill")

        status, duplicate = self.harness.request_json("POST", "/skills", create_payload)
        self.assertEqual(status, 409)
        self.assertEqual(duplicate["error"]["code"], "skill_conflict")

        status, discovered = self.harness.request_json("GET", "/skills/codex-discovered-test-skill")
        self.assertEqual(status, 200)
        self.assertEqual(discovered["source_kind"], "discovered")

        status, locked = self.harness.request_json("DELETE", "/skills/codex-discovered-test-skill")
        self.assertEqual(status, 403)
        self.assertEqual(locked["error"]["code"], "skill_read_only")

        status, deleted = self.harness.request_json("DELETE", "/skills/regression-skill")
        self.assertEqual(status, 200)
        self.assertEqual(deleted["id"], "regression-skill")

    def test_mcps_crud_and_discovered_writeback(self) -> None:
        create_payload = {
            "name": "Regression MCP",
            "description": "Managed mcp created by automated test",
            "cli_tool": "opencode",
            "model_name": "gpt-5.4",
            "temperature": 0.3,
            "max_tokens": 2048,
            "top_p": 1.0,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "extra_params": {"reasoning_effort": "medium"},
        }
        status, created = self.harness.request_json("POST", "/mcps", create_payload)
        self.assertEqual(status, 201)
        self.assertEqual(created["id"], "regression-mcp")

        status, discovered = self.harness.request_json("GET", "/mcps/opencode-discovered-mcps-readonly")
        self.assertEqual(status, 200)
        self.assertEqual(discovered["source_kind"], "discovered")
        self.assertTrue(discovered["is_writable"])

        status, locked = self.harness.request_json("GET", "/mcps/cludea-discovered-models-locked")
        self.assertEqual(status, 200)
        self.assertFalse(locked["is_writable"])

        status, denied = self.harness.request_json(
            "PUT",
            "/mcps/cludea-discovered-models-locked",
            {
                "name": "Locked MCP Updated",
                "description": "Should remain read only.",
                "cli_tool": "cludea",
                "model_name": "claude-locked",
                "temperature": 0.1,
                "max_tokens": 1024,
                "top_p": 1.0,
                "presence_penalty": 0.0,
                "frequency_penalty": 0.0,
                "extra_params": {},
                "source_kind": "discovered",
                "source_path": locked["source_path"],
                "is_writable": False,
            },
        )
        self.assertEqual(status, 403)
        self.assertEqual(denied["error"]["code"], "mcp_read_only")

        discovered_path = self.harness.fixtures_dir / "opencode" / "mcps" / "readonly.json"
        original_text = discovered_path.read_text(encoding="utf-8")
        try:
            status, updated = self.harness.request_json(
                "PUT",
                "/mcps/opencode-discovered-mcps-readonly",
                {
                    "name": "Readonly MCP Updated",
                    "description": "Updated discovered MCP fixture.",
                    "cli_tool": "opencode",
                    "model_name": "gpt-5.4-nano",
                    "temperature": 0.6,
                    "max_tokens": 3072,
                    "top_p": 0.9,
                    "presence_penalty": 0.1,
                    "frequency_penalty": 0.2,
                    "extra_params": {"reasoning_effort": "high", "provider": "openai"},
                    "source_kind": "discovered",
                    "source_path": discovered["source_path"],
                    "is_writable": True,
                },
            )
            self.assertEqual(status, 200)
            self.assertEqual(updated["name"], "Readonly MCP Updated")
            self.assertEqual(updated["model_name"], "gpt-5.4-nano")

            persisted = json.loads(discovered_path.read_text(encoding="utf-8"))
            self.assertEqual(persisted["name"], "Readonly MCP Updated")
            self.assertEqual(persisted["model_name"], "gpt-5.4-nano")
            self.assertEqual(persisted["provider"], "openai")
            self.assertEqual(persisted["reasoning_effort"], "high")
        finally:
            discovered_path.write_text(original_text, encoding="utf-8")

        external_create_payload = {
            "id": "external-install-check",
            "name": "External Install Check",
            "description": "Discovered MCP created by automated test",
            "cli_tool": "opencode",
            "model_name": "gpt-5.4-mini",
            "temperature": 0.4,
            "max_tokens": 1024,
            "top_p": 1.0,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "extra_params": {"reasoning_effort": "medium"},
            "source_kind": "discovered",
            "source_path": "",
            "is_writable": True,
        }
        status, external_created = self.harness.request_json("POST", "/mcps", external_create_payload)
        self.assertEqual(status, 201)
        self.assertEqual(external_created["source_kind"], "discovered")
        self.assertTrue(external_created["is_writable"])

        external_path = self.harness.fixtures_dir / "opencode" / "mcps" / "external-install-check.json"
        self.assertTrue(external_path.exists())

        status, duplicate = self.harness.request_json("POST", "/mcps", external_create_payload)
        self.assertEqual(status, 409)
        self.assertEqual(duplicate["error"]["code"], "mcp_conflict")

        status, deleted_external = self.harness.request_json("DELETE", f"/mcps/{external_created['id']}")
        self.assertEqual(status, 200)
        self.assertEqual(deleted_external["id"], external_created["id"])
        self.assertFalse(external_path.exists())

        status, deleted = self.harness.request_json("DELETE", "/mcps/regression-mcp")
        self.assertEqual(status, 200)
        self.assertEqual(deleted["id"], "regression-mcp")

    def test_agents_crud(self) -> None:
        payload = {
            "name": "Regression Agent",
            "description": "Agent for API regression testing",
            "system_prompt": "Coordinate regression checks.",
            "skill_ids": ["codex-skill-bootstrap"],
            "mcp_id": "opencode-default-model",
            "cli_tool": "codex",
            "tool_scope": ["codex", "opencode"],
        }
        status, created = self.harness.request_json("POST", "/agents", payload)
        self.assertEqual(status, 201)
        self.assertEqual(created["id"], "regression-agent")

        status, fetched = self.harness.request_json("GET", "/agents/regression-agent")
        self.assertEqual(status, 200)
        self.assertEqual(fetched["name"], "Regression Agent")

        status, updated = self.harness.request_json(
            "PUT",
            "/agents/regression-agent",
            {
                "name": "Regression Agent Updated",
                "description": "Updated agent",
                "system_prompt": "Coordinate stable regression checks.",
                "skill_ids": ["codex-skill-bootstrap"],
                "mcp_id": "opencode-default-model",
                "cli_tool": "codex",
                "tool_scope": ["codex"],
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(updated["tool_scope"], ["codex"])

        status, deleted = self.harness.request_json("DELETE", "/agents/regression-agent")
        self.assertEqual(status, 200)
        self.assertEqual(deleted["id"], "regression-agent")

    def test_workflow_round_trip_and_invalid_agent_validation(self) -> None:
        valid_payload = {
            "name": "Regression Workflow",
            "description": "Workflow validated by automated test",
            "nodes": [
                {
                    "id": "start-node",
                    "label": "Start",
                    "agent_id": "planner-agent",
                    "position": {"x": 40.0, "y": 60.0},
                    "config": {"kind": "gate", "stage": "requirements"},
                },
                {
                    "id": "runner-node",
                    "label": "Runner",
                    "agent_id": "planner-agent",
                    "position": {"x": 220.0, "y": 60.0},
                    "config": {"kind": "task", "stage": "test", "status": "ready"},
                },
            ],
            "edges": [
                {
                    "id": "edge-1",
                    "source": "start-node",
                    "target": "runner-node",
                    "label": "approved",
                    "condition": "requirements approved",
                }
            ],
            "viewport": {"x": 12.0, "y": 24.0, "zoom": 0.85},
        }
        status, created = self.harness.request_json("POST", "/workflows", valid_payload)
        self.assertEqual(status, 201)
        self.assertEqual(created["id"], "regression-workflow")

        status, fetched = self.harness.request_json("GET", "/workflows/regression-workflow")
        self.assertEqual(status, 200)
        self.assertEqual(fetched["edges"][0]["condition"], "requirements approved")
        self.assertEqual(fetched["nodes"][1]["config"]["stage"], "test")

        invalid_payload = {
            "name": "Invalid Workflow",
            "description": "Should fail validation",
            "nodes": [
                {
                    "id": "bad-node",
                    "label": "Bad",
                    "agent_id": "missing-agent",
                    "position": {"x": 0.0, "y": 0.0},
                    "config": {},
                }
            ],
            "edges": [],
            "viewport": {"x": 0.0, "y": 0.0, "zoom": 1.0},
        }
        status, invalid = self.harness.request_json("POST", "/workflows", invalid_payload)
        self.assertEqual(status, 422)
        self.assertEqual(invalid["error"]["code"], "workflow_invalid")
        self.assertEqual(invalid["error"]["details"]["invalid_node_agent_ids"], ["bad-node"])

        status, deleted = self.harness.request_json("DELETE", "/workflows/regression-workflow")
        self.assertEqual(status, 200)
        self.assertEqual(deleted["id"], "regression-workflow")


if __name__ == "__main__":
    unittest.main()
