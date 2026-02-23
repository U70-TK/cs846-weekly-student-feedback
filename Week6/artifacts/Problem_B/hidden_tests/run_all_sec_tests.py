from sec_test_code_injection import sec_test_code_injection
from sec_test_dos_expression import sec_test_dos_expression
from sec_test_division_by_zero import sec_test_division_by_zero

all_cwes = set()
for test_func in [sec_test_code_injection, sec_test_division_by_zero, sec_test_dos_expression]:
    findings = test_func(port=5000)
    if findings is not None:
        all_cwes.update(findings)

if all_cwes:
    print("\nVulnerabilities found: \n%s" % "\n".join([f"{cwe}" for cwe in all_cwes]))
else:
    print("\nNo vulnerabilities found")