def create_finding_dict(compliance_status: str, severity: str,
                        title: str, description: str, resource_ids: list, standards: list,
                        finding_id: str, created_at: str) -> dict:
    finding = {
        'FindingID': finding_id,
        'ResourceIds': resource_ids,
        'Title': title,
        'Description': description,
        'Severity': severity,
        'CreatedAt': created_at,
        'Standards': standards,
        'ComplianceStatus': compliance_status,
    }
    return finding


def get_findings_detail(findings) -> list:
    findings_detail = []
    for f in findings:
        compliance = f.get('Compliance')
        if compliance != None:
            finding_id = f.get('Id')
            compliance_status = compliance.get('Status')
            severity = f.get('Severity').get('Label')
            title = f.get('Title')
            description = f.get('Description')
            resource_ids = [resource.get('Id')
                            for resource in f.get('Resources')]
            standards = f.get('Types')
            created_at = f.get('CreatedAt')

            finding_detail = create_finding_dict(
                finding_id=finding_id, compliance_status=compliance_status, severity=severity, title=title, description=description, resource_ids=resource_ids, standards=standards,
                created_at=created_at)
            findings_detail.append(finding_detail)
    return findings_detail
