import re
import urllib.parse
import requests

class PolarionService:
    def __init__(self):
        pass

    def get_trace(self, requirement_input, config=None):
        if config is None:
            config = {}

        use_mock = config.get("use_mock", True)
        server_url = config.get("server_url", "https://polarion.example.com").rstrip("/")
        project_id = config.get("project_id", "DRIVE_SYS")
        token = config.get("token", "")

        # If use_mock is True or no valid real URL is provided, return rich mock data
        if use_mock or "example.com" in server_url or not server_url:
            return self._generate_mock_trace(requirement_input, project_id)

        try:
            return self._fetch_polarion_trace(requirement_input, server_url, project_id, token)
        except Exception as e:
            # Fallback or pass error message
            return {
                "success": False,
                "error": f"Failed to connect to Polarion server at {server_url}: {str(e)}",
                "fallback_mock": self._generate_mock_trace(requirement_input, project_id)
            }

    def _fetch_polarion_trace(self, requirement_input, server_url, project_id, token):
        # Extract potential work item ID (e.g., REQ-101, FUNC-002)
        match = re.search(r'([A-Z0-9]+-[0-9]+)', requirement_input, re.IGNORECASE)
        item_id = match.group(1).upper() if match else requirement_input.strip()

        headers = {
            "Accept": "application/vnd.api+json",
            "Authorization": f"Bearer {token}" if token else ""
        }

        # Query workitem from Polarion REST API
        endpoint = f"{server_url}/polarion/rest/v1/projects/{project_id}/workitems/{item_id}"
        resp = requests.get(endpoint, headers=headers, timeout=5)

        if resp.status_code == 200:
            data = resp.json()
            # Construct standard trace response format from API response
            wi_data = data.get("data", {})
            attributes = wi_data.get("attributes", {})

            return {
                "success": True,
                "query": requirement_input,
                "project_id": project_id,
                "server_url": server_url,
                "root_item": {
                    "id": wi_data.get("id", item_id),
                    "type": attributes.get("type", "Functional Requirement"),
                    "title": attributes.get("title", requirement_input),
                    "status": attributes.get("status", "Approved"),
                    "severity": attributes.get("severity", "High"),
                    "description": attributes.get("description", {}).get("value", requirement_input)
                },
                "linked_items": [],
                "coverage": {
                    "system_reqs": 0,
                    "test_cases": 0,
                    "bugs": 0,
                    "tasks": 0,
                    "test_status_summary": {"passed": 0, "failed": 0, "blocked": 0}
                }
            }
        else:
            # Return detailed error if API request fails
            return {
                "success": False,
                "error": f"Polarion API returned status code {resp.status_code}: {resp.text[:200]}"
            }

    def _generate_mock_trace(self, requirement_input, project_id):
        clean_input = requirement_input.strip()

        # Match pattern like REQ-101, FUNC-202 or extract words
        req_match = re.search(r'(REQ|FUNC|SYS|DSGN)-?(\d+)', clean_input, re.IGNORECASE)
        if req_match:
            req_prefix = req_match.group(1).upper()
            req_num = req_match.group(2)
            req_id = f"{req_prefix}-{req_num}"
        else:
            req_id = "FUNC-101"

        title = clean_input if len(clean_input) > 0 else "Emergency Braking Functional Control Algorithm"
        if len(title) > 80:
            short_title = title[:77] + "..."
        else:
            short_title = title

        # Create structured, realistic trace hierarchy
        root_item = {
            "id": req_id,
            "type": "Functional Requirement",
            "title": short_title,
            "description": clean_input or "The system shall calculate distance to target object and trigger automatic braking within 50ms when obstacle probability exceeds 95%.",
            "status": "In Review" if "review" in clean_input.lower() else "Approved",
            "severity": "Critical" if "safety" in clean_input.lower() or "braking" in clean_input.lower() else "High",
            "author": "J. Miller (Systems Engineer)",
            "updated": "2026-09-20"
        }

        linked_items = [
            {
                "id": f"SYS-{int(req_id.split('-')[-1] if '-' in req_id and req_id.split('-')[-1].isdigit() else 100) + 10}",
                "type": "System Requirement",
                "relationship": "verifies / implements",
                "title": f"Radar Sensor Data Processing for {short_title}",
                "status": "Approved",
                "assignee": "A. Chen",
                "children": [
                    {
                        "id": f"TEST-{int(req_id.split('-')[-1] if '-' in req_id and req_id.split('-')[-1].isdigit() else 100) + 101}",
                        "type": "Test Case",
                        "relationship": "verified by",
                        "title": "Verify obstacle distance threshold response time < 50ms",
                        "status": "Passed",
                        "verdict": "PASSED",
                        "last_run": "2026-09-24 14:32",
                        "children": []
                    },
                    {
                        "id": f"BUG-{int(req_id.split('-')[-1] if '-' in req_id and req_id.split('-')[-1].isdigit() else 100) + 501}",
                        "type": "Defect / Bug",
                        "relationship": "triggers defect",
                        "title": "Radar latency spike during target re-acquisition under rain simulation",
                        "status": "In Progress",
                        "verdict": "OPEN",
                        "severity": "Medium",
                        "children": []
                    }
                ]
            },
            {
                "id": f"SYS-{int(req_id.split('-')[-1] if '-' in req_id and req_id.split('-')[-1].isdigit() else 100) + 11}",
                "type": "System Requirement",
                "relationship": "verifies / implements",
                "title": f"Brake Actuator Signal Protocol for {short_title}",
                "status": "Approved",
                "assignee": "M. Weber",
                "children": [
                    {
                        "id": f"TEST-{int(req_id.split('-')[-1] if '-' in req_id and req_id.split('-')[-1].isdigit() else 100) + 102}",
                        "type": "Test Case",
                        "relationship": "verified by",
                        "title": "Brake pressure ramp-up curve validation against ISO 26262 ASIL-D",
                        "status": "Passed",
                        "verdict": "PASSED",
                        "last_run": "2026-09-24 15:10",
                        "children": []
                    },
                    {
                        "id": f"TEST-{int(req_id.split('-')[-1] if '-' in req_id and req_id.split('-')[-1].isdigit() else 100) + 103}",
                        "type": "Test Case",
                        "relationship": "verified by",
                        "title": "CAN bus message injection test under simulated hardware fault",
                        "status": "Passed",
                        "verdict": "PASSED",
                        "last_run": "2026-09-24 16:05",
                        "children": []
                    }
                ]
            },
            {
                "id": f"TASK-{int(req_id.split('-')[-1] if '-' in req_id and req_id.split('-')[-1].isdigit() else 100) + 301}",
                "type": "Task",
                "relationship": "tracked by",
                "title": "Update ASIL-D Safety Case Documentation for functional requirement",
                "status": "Done",
                "assignee": "S. Taylor",
                "children": []
            }
        ]

        # Calculate coverage metrics
        total_sys = sum(1 for item in linked_items if item["type"] == "System Requirement")
        test_cases = []
        bugs = []
        tasks = []

        def collect_children(items):
            for item in items:
                if item["type"] == "Test Case":
                    test_cases.append(item)
                elif "Bug" in item["type"] or "Defect" in item["type"]:
                    bugs.append(item)
                elif item["type"] == "Task":
                    tasks.append(item)
                if "children" in item and item["children"]:
                    collect_children(item["children"])

        collect_children(linked_items)

        passed_tests = sum(1 for t in test_cases if t.get("verdict") == "PASSED")
        failed_tests = sum(1 for t in test_cases if t.get("verdict") == "FAILED")
        blocked_tests = sum(1 for t in test_cases if t.get("verdict") == "BLOCKED")

        return {
            "success": True,
            "query": requirement_input,
            "project_id": project_id,
            "server_url": "https://polarion.internal.corp (Mock Engine)",
            "root_item": root_item,
            "linked_items": linked_items,
            "coverage": {
                "system_reqs": total_sys,
                "test_cases": len(test_cases),
                "bugs": len(bugs),
                "tasks": len(tasks),
                "test_status_summary": {
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "blocked": blocked_tests,
                    "coverage_percent": round((passed_tests / len(test_cases) * 100) if test_cases else 0, 1)
                }
            }
        }
