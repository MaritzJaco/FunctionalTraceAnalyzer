# Polarion Functional Trace Viewer (Velocity Script)

This repository provides an Apache Velocity script (`polarion_trace_viewer.vm`) designed for Siemens Polarion ALM. It allows engineers to enter a functional requirement Work Item ID, press **Apply / Run Trace**, and visualize its traceability tree (System Requirements, Test Cases, Bugs, and Tasks) along with metric summaries and a matrix table.

---

## 🚀 Features

1. **Input Box & Action Button**: Simple form to enter any requirement ID (e.g. `0030-57578`, `REQ-101`, `FUNC-204`) and execute the trace.
2. **URL Parameter Override**: User input entered in the text box takes immediate precedence over default Rich Page sidebar parameters (`reqId`), allowing flexible interactive searches.
3. **Project Context Display**: Displays the active Polarion Project ID in the report header and metric cards so you can confirm which project is being queried.
4. **Polarion Open Java API Integration**: Uses `$trackerService.queryWorkItems(...)` to search and load work items dynamically.
5. **Multi-level Hierarchy Traversal**: Traverses direct linked work items (`linkedWorkItemsStructsDirect`) across 2+ levels.
6. **Summary Metrics Dashboard**: Automatically counts linked System Requirements, Test Cases, and Defects.
7. **Dual Views**:
   - **Tree View**: Hierarchical visual tree showing relationships (`verifies`, `implements`, `relates to`).
   - **Matrix View**: Table listing levels, Work Item IDs, types, roles, titles, and statuses.

---

## 🛠️ Installation in Polarion ALM

### Option A: Polarion Rich Page / Script Widget
1. Open or create a **Rich Page** in your Polarion ALM project.
2. Add a **Script Widget** or **Velocity Script Widget** to the page layout.
3. If desired, configure a Page Parameter with ID `reqId` in the page settings dialog (or leave blank).
4. Copy the contents of `polarion_trace_viewer.vm` into the Velocity script field of the widget.
5. Save the page.

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

## ❓ Page Parameters FAQ

**Q: Should I have a page parameter with ID `reqId`?**
**A:** Yes, defining a Page Parameter with ID `reqId` in your Rich Page settings is completely fine and supported. The script will use it as the default requirement ID on initial page load, while typing a new requirement ID into the input field and clicking **Apply / Run Trace** will temporarily override it.

---

## 🧪 Testing

A test harness script `test_velocity_template.py` is included in this repository to parse and validate the syntax of `polarion_trace_viewer.vm`. Run:

```bash
python3 test_velocity_template.py
```
