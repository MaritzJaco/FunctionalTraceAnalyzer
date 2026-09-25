import os
import re

def test_velocity_template():
    vm_filepath = "polarion_trace_viewer.vm"
    assert os.path.exists(vm_filepath), f"File {vm_filepath} does not exist"

    with open(vm_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check version badge
    assert 'v1.0.2' in content, "Missing v1.0.2 version badge"

    # 2. Check HTML input box and submit button
    assert '<input type="text" id="tvReqInput" name="reqId"' in content, "Missing requirement text input box"
    assert 'method="GET"' in content, "Missing GET form method"
    assert '<button type="submit"' in content, "Missing submit button"
    assert 'function tvApplyTrace(' in content, "Missing tvApplyTrace JavaScript navigation handler"

    # 3. Check Velocity directives balance
    if_count = len(re.findall(r'#if\b', content))
    end_count = len(re.findall(r'#end\b', content))
    foreach_count = len(re.findall(r'#foreach\b', content))

    print(f"Template Directives Stats: #if={if_count}, #foreach={foreach_count}, #end={end_count}")
    assert if_count + foreach_count == end_count, f"Directive mismatch: (#if + #foreach = {if_count + foreach_count}) != (#end = {end_count})"

    # 4. Check query construction syntax
    assert '#set($query = "id:${selectedReqId}")' in content, "Missing expected $query initialization"
    assert '#set($query = "project.id:${currentProjId} AND id:${selectedReqId}")' in content, "Missing expected project $query"

    # 5. Check Polarion Java Open API references & simplified structure
    assert '$trackerService.queryWorkItems' in content, "Missing Polarion trackerService query"
    assert 'linkedWorkItemsStructsDirect' in content, "Missing linked work items traversal"
    assert '$link.linkedItem' in content, "Missing Polarion ILinkedWorkItemStruct.linkedItem property reference"
    assert '$!rootItem.id' in content, "Missing root item ID rendering"
    assert '$!rootItem.title' in content, "Missing root item title rendering"

    print("All Velocity Template validation checks PASSED successfully!")

if __name__ == "__main__":
    test_velocity_template()
