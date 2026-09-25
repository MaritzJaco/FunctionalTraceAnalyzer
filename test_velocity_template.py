import os
import re

def test_velocity_template():
    vm_filepath = "polarion_trace_viewer.vm"
    assert os.path.exists(vm_filepath), f"File {vm_filepath} does not exist"

    with open(vm_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check HTML input box and submit button
    assert '<input type="text" id="tvReqInput" name="reqId"' in content, "Missing requirement text input box"
    assert '⚡ Apply / Run Trace' in content, "Missing Apply / Run button"
    assert 'function tvApplyTrace(' in content, "Missing tvApplyTrace JavaScript navigation handler"

    # 2. Check Velocity directives balance
    if_count = len(re.findall(r'#if\b', content))
    end_count = len(re.findall(r'#end\b', content))
    foreach_count = len(re.findall(r'#foreach\b', content))

    print(f"Template Directives Stats: #if={if_count}, #foreach={foreach_count}, #end={end_count}")
    assert if_count + foreach_count == end_count, f"Directive mismatch: (#if + #foreach = {if_count + foreach_count}) != (#end = {end_count})"

    # 3. Check Polarion Java Open API references & property access
    assert '$trackerService.queryWorkItems' in content, "Missing Polarion trackerService query"
    assert 'linkedWorkItemsStructsDirect' in content, "Missing linked work items traversal"
    assert '$link.linkedItem' in content, "Missing Polarion ILinkedWorkItemStruct.linkedItem property reference"
    assert '$!rootItem.id' in content, "Missing root item rendering"
    assert '$trackerService.projectsService' not in content, "Should not access invalid $trackerService.projectsService property"

    print("All Velocity Template validation checks PASSED successfully!")

if __name__ == "__main__":
    test_velocity_template()
