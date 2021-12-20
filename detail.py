def create_finding_str(compliance_status: str, severity_label: str, title: str, description: str, resource_ids: list, standards: list) -> dict:
    finding = {
        'ComplianceStatus': compliance_status,
        'SeverityLabel': severity_label,
        'Title': title,
        'Description': description,
        'ResourceIds': resource_ids,
        'Standards': standards,
    }
    return finding


def get_findings_detail(findings) -> list:
    findings_detail = []
    for f in findings:
        compliance = f.get('Compliance')
        if compliance != None:
            compliance_status = compliance.get('Status')
            severity = f.get('Severity').get('Label')
            title = f.get('Title')
            description = f.get('Description')
            resource_ids = [resource.get('Id')
                            for resource in f.get('Resources')]
            standards = f.get('Types')

            finding_detail = create_finding_str(
                compliance_status=compliance_status, severity_label=severity, title=title, description=description, resource_ids=resource_ids, standards=standards)
            findings_detail.append(finding_detail)
    return findings_detail
