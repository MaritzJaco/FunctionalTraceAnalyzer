document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const reqInput = document.getElementById('req-input');
    const runTraceBtn = document.getElementById('run-trace-btn');
    const clearBtn = document.getElementById('clear-btn');
    const toggleConfigBtn = document.getElementById('toggle-config-btn');
    const configPanel = document.getElementById('config-panel');
    const sampleBtns = document.querySelectorAll('.chip-btn');

    const resultsSection = document.getElementById('results-section');
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorBox = document.getElementById('error-box');
    const errorMessage = document.getElementById('error-message');
    const exportJsonBtn = document.getElementById('export-json-btn');

    // Config Elements
    const serverUrlInput = document.getElementById('server-url');
    const projectIdInput = document.getElementById('project-id');
    const authTokenInput = document.getElementById('auth-token');
    const useMockCheckbox = document.getElementById('use-mock');

    // Tabs
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    let currentTraceData = null;

    // Toggle Config Panel
    toggleConfigBtn.addEventListener('click', () => {
        configPanel.classList.toggle('hidden');
    });

    // Quick Sample Selection
    sampleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            reqInput.value = btn.getAttribute('data-req');
            reqInput.focus();
        });
    });

    // Clear Button
    clearBtn.addEventListener('click', () => {
        reqInput.value = '';
        resultsSection.classList.add('hidden');
        errorBox.classList.add('hidden');
        currentTraceData = null;
    });

    // Tab Switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(`${targetTab}-view-tab`).classList.add('active');
        });
    });

    // Execute Trace Query
    runTraceBtn.addEventListener('click', () => {
        const requirement = reqInput.value.trim();
        if (!requirement) {
            showError('Please enter a Functional Requirement ID or description.');
            return;
        }

        hideError();
        resultsSection.classList.add('hidden');
        loadingSpinner.classList.remove('hidden');

        const payload = {
            requirement: requirement,
            server_url: serverUrlInput.value,
            project_id: projectIdInput.value,
            token: authTokenInput.value,
            use_mock: useMockCheckbox.checked
        };

        fetch('/api/trace', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            loadingSpinner.classList.add('hidden');
            if (data.success) {
                currentTraceData = data;
                renderTraceView(data);
                resultsSection.classList.remove('hidden');
            } else {
                showError(data.error || 'Failed to retrieve functional trace from Polarion.');
            }
        })
        .catch(err => {
            loadingSpinner.classList.add('hidden');
            showError('Network error connecting to Polarion server interface: ' + err.message);
        });
    });

    // Export JSON
    exportJsonBtn.addEventListener('click', () => {
        if (!currentTraceData) return;
        const blob = new Blob([JSON.stringify(currentTraceData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `polarion-trace-${currentTraceData.root_item.id || 'export'}.json`;
        a.click();
        URL.revokeObjectURL(url);
    });

    function showError(msg) {
        errorMessage.textContent = msg;
        errorBox.classList.remove('hidden');
    }

    function hideError() {
        errorBox.classList.add('hidden');
    }

    // Render Metrics and Views
    function renderTraceView(data) {
        // Metrics Dashboard
        const root = data.root_item || {};
        document.getElementById('root-req-id').textContent = root.id || 'N/A';
        document.getElementById('root-req-type').textContent = root.type || 'Functional Requirement';

        const cov = data.coverage || {};
        document.getElementById('count-sys').textContent = cov.system_reqs || 0;
        document.getElementById('count-tests').textContent = cov.test_cases || 0;

        const testSummary = cov.test_status_summary || {};
        document.getElementById('test-verdict-summary').textContent =
            `${testSummary.passed || 0} Passed, ${testSummary.failed || 0} Failed (${testSummary.coverage_percent || 0}% Pass Rate)`;

        document.getElementById('count-bugs').textContent = cov.bugs || 0;
        document.getElementById('bug-severity-summary').textContent = `${cov.bugs || 0} Active Defects Found`;

        // Render Tree
        const treeContainer = document.getElementById('tree-container');
        treeContainer.innerHTML = '';
        treeContainer.appendChild(createTreeNode(root, null, true));

        if (data.linked_items && data.linked_items.length > 0) {
            data.linked_items.forEach(child => {
                treeContainer.appendChild(createTreeNode(child));
            });
        }

        // Render Table
        const tableBody = document.getElementById('trace-table-body');
        tableBody.innerHTML = '';
        const rows = [];
        flattenTraceForTable(root, 'Root (L0)', 'Primary Focus', rows);

        if (data.linked_items) {
            data.linked_items.forEach(child => {
                flattenTraceForTable(child, 'L1', child.relationship || 'implements', rows);
            });
        }

        rows.forEach(r => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><span class="badge badge-info">${r.level}</span></td>
                <td><span class="item-id">${r.id}</span></td>
                <td>${r.type}</td>
                <td><span class="relationship-tag">${r.relationship}</span></td>
                <td>${r.title}</td>
                <td>${getStatusBadge(r.status || r.verdict)}</td>
            `;
            tableBody.appendChild(tr);
        });
    }

    // Helper: Tree Node Element Builder
    function createTreeNode(item, parentRelationship = null, isRoot = false) {
        const nodeDiv = document.createElement('div');
        nodeDiv.className = `tree-node ${isRoot ? 'root-node' : ''}`;

        const card = document.createElement('div');
        card.className = 'node-card';

        const header = document.createElement('div');
        header.className = 'node-header';

        const idSpan = document.createElement('span');
        idSpan.className = 'item-id';
        idSpan.textContent = item.id;

        const typeBadge = document.createElement('span');
        typeBadge.className = `badge ${getTypeBadgeClass(item.type)}`;
        typeBadge.textContent = item.type;

        const titleSpan = document.createElement('span');
        titleSpan.className = 'item-title';
        titleSpan.textContent = item.title;

        header.appendChild(idSpan);
        header.appendChild(typeBadge);

        if (item.relationship) {
            const relSpan = document.createElement('span');
            relSpan.className = 'relationship-tag';
            relSpan.textContent = `⬅ ${item.relationship}`;
            header.appendChild(relSpan);
        }

        header.appendChild(titleSpan);

        const detailsDiv = document.createElement('div');
        detailsDiv.className = 'node-details';

        let extraInfo = '';
        if (item.status) extraInfo += `Status: ${item.status} | `;
        if (item.verdict) extraInfo += `Verdict: ${item.verdict} | `;
        if (item.assignee) extraInfo += `Owner: ${item.assignee} | `;
        if (item.description) extraInfo += `Summary: ${item.description.substring(0, 100)}...`;

        detailsDiv.textContent = extraInfo;

        card.appendChild(header);
        card.appendChild(detailsDiv);
        nodeDiv.appendChild(card);

        if (item.children && item.children.length > 0) {
            item.children.forEach(child => {
                nodeDiv.appendChild(createTreeNode(child, child.relationship));
            });
        }

        return nodeDiv;
    }

    function flattenTraceForTable(item, level, relationship, rowList) {
        rowList.push({
            level: level,
            id: item.id,
            type: item.type,
            relationship: item.relationship || relationship,
            title: item.title,
            status: item.status || item.verdict || 'N/A'
        });

        if (item.children && item.children.length > 0) {
            item.children.forEach(child => {
                flattenTraceForTable(child, 'L2', child.relationship || 'verifies', rowList);
            });
        }
    }

    function getTypeBadgeClass(type) {
        if (!type) return 'badge-info';
        if (type.includes('Functional')) return 'badge-info';
        if (type.includes('System')) return 'badge-warning';
        if (type.includes('Test')) return 'badge-success';
        if (type.includes('Bug') || type.includes('Defect')) return 'badge-danger';
        return 'badge-info';
    }

    function getStatusBadge(status) {
        if (!status) return '<span class="badge badge-info">N/A</span>';
        if (status === 'Passed' || status === 'PASSED' || status === 'Approved' || status === 'Done') {
            return `<span class="badge badge-success">${status}</span>`;
        }
        if (status === 'Failed' || status === 'FAILED' || status === 'OPEN') {
            return `<span class="badge badge-danger">${status}</span>`;
        }
        return `<span class="badge badge-warning">${status}</span>`;
    }
});
