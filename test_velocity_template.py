import os
import re

def test_velocity_template():
    vm_filepath = "polarion_trace_viewer.vm"
    assert os.path.exists(vm_filepath), f"File {vm_filepath} does not exist"

    with open(vm_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check version badge
    assert 'v1.0.4' in content, "Missing v1.0.4 version badge"

    # 2. Check null guards for $request
    assert '#if($request)' in content, "Missing $request null check guard"

    # 3. Check HTML input box and submit button
    assert '<input type="text" id="tvReqInput" name="WorkItems"' in content, "Missing requirement text input box with WorkItems parameter"
    assert 'method="GET"' in content, "Missing GET form method"
    assert '<button type="submit"' in content, "Missing submit button"
    assert 'function tvApplyTrace(' in content, "Missing tvApplyTrace JavaScript navigation handler"
    assert 'function tvCopyUrl(' in content, "Missing tvCopyUrl JavaScript handler"

    # 4. Check Velocity directives balance
    if_count = len(re.findall(r'#if\b', content))
    end_count = len(re.findall(r'#end\b', content))
    foreach_count = len(re.findall(r'#foreach\b', content))

    print(f"Template Directives Stats: #if={if_count}, #foreach={foreach_count}, #end={end_count}")
    assert if_count + foreach_count == end_count, f"Directive mismatch: (#if + #foreach = {if_count + foreach_count}) != (#end = {end_count})"

    # 5. Check URL construction parameters & format
    assert '#/project/0030/wiki/Report/Functional%20Traceability%20Analyzer?Title=' in content, "Missing URL construction base"
    assert '&WorkItems=' in content, "Missing WorkItems URL parameter construct"
    assert '&Depth=' in content, "Missing Depth URL parameter construct"

    # 6. Check Polarion Java Open API references & simplified structure
    assert '$trackerService.queryWorkItems' in content, "Missing Polarion trackerService query"
    assert 'linkedWorkItemsStructsDirect' in content, "Missing linked work items traversal"
    assert '$link.linkedItem' in content, "Missing Polarion ILinkedWorkItemStruct.linkedItem property reference"
    assert '$!rootItem.id' in content, "Missing root item ID rendering"
    assert '$!rootItem.title' in content, "Missing root item title rendering"

    print("All Velocity Template validation checks PASSED successfully!")

if __name__ == "__main__":
    test_velocity_template()
