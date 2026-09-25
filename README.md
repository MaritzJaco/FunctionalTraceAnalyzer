# Polarion Functional Trace Viewer (Velocity Script)

This repository provides an Apache Velocity script (`polarion_trace_viewer.vm`) designed for Siemens Polarion ALM. It allows engineers to enter a functional requirement Work Item ID, press **Apply / Run Trace**, and visualize its traceability tree (System Requirements, Test Cases, Bugs, and Tasks) along with metric summaries and a matrix table.

---

## 🚀 Features

1. **Input Box & Action Button**: Simple form to enter any requirement ID (e.g. `REQ-101`, `FUNC-204`) and execute the trace.
2. **Polarion Open Java API Integration**: Uses `$trackerService.queryWorkItems(...)` to search and load work items dynamically.
3. **Multi-level Hierarchy Traversal**: Traverses direct linked work items (`linkedWorkItemsStructsDirect`) across 2+ levels.
4. **Summary Metrics Dashboard**: Automatically counts linked System Requirements, Test Cases, and Defects.
5. **Dual Views**:
   - **Tree View**: Hierarchical visual tree showing relationships (`verifies`, `implements`, `relates to`).
   - **Matrix View**: Table listing levels, Work Item IDs, types, roles, titles, and statuses.

---

## 🛠️ Installation in Polarion ALM

### Option A: Polarion Rich Page / Script Widget
1. Open or create a **Rich Page** in your Polarion ALM project.
2. Add a **Script Widget** or **Velocity Script Widget** to the page layout.
3. Copy the contents of `polarion_trace_viewer.vm` into the Velocity script field of the widget.
4. Save the page.

### Option B: Classic Wiki Page
1. Navigate to your Polarion Wiki space.
2. Edit a Wiki Page and wrap the template content in `{velocity}` macro tags:
   ```velocity
   {velocity}
   ## Paste content of polarion_trace_viewer.vm here
   {velocity}
   ```
3. Save and view the Wiki page.

---

## 🧪 Testing

A test harness script `test_velocity_template.py` is included in this repository to parse and validate the syntax of `polarion_trace_viewer.vm`. Run:

```bash
python3 test_velocity_template.py
```
