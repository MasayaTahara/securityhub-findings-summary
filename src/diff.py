def get_summary(current_findings_detail, previous_findings_detail) -> list:
    findings_summary = []

    # Get previous/current finding IDs
    previous_finding_ids = [previous_finding.get(
        'FindingID') for previous_finding in previous_findings_detail]
    current_finding_ids = [current_finding.get(
        'FindingID') for current_finding in current_findings_detail]

    for current_finding in current_findings_detail:
        # Check whether previous finding IDs contain current finding ID
        if current_finding.get('FindingID') in previous_finding_ids:
            status = 'NOTIFIED'
        else:
            status = 'NEW'

        findings_summary.append(create_summary_dict(
            finding_id=current_finding['FindingID'],
            resource_ids=current_finding['ResourceIDs'],
            title=current_finding['Title'],
            description=current_finding['Description'],
            severity=current_finding['Severity'],
            created_at=current_finding['CreatedAt'],
            standards=current_finding['Standards'],
            status=status,
        ))

    # Check whether current finding IDs contain previous finding ID (not DELETED status)
    for previous_finding in previous_findings_detail:
        if previous_finding.get('Status') != 'DELETED':
            if not previous_finding.get('FindingID') in current_finding_ids:
                findings_summary.append(create_summary_dict(
                    finding_id=previous_finding['FindingID'],
                    resource_ids=previous_finding['ResourceIDs'],
                    title=previous_finding['Title'],
                    description=previous_finding['Description'],
                    severity=previous_finding['Severity'],
                    created_at=previous_finding['CreatedAt'],
                    standards=previous_finding['Standards'],
                    status='DELETED',
                ))

    return findings_summary


def create_summary_dict(status: str, severity: str,
                        title: str, description: str, resource_ids: list, standards: list,
                        finding_id: str, created_at: str) -> dict:
    summary = {
        'FindingID': finding_id,
        'Status': status,
        'ResourceIDs': resource_ids,
        'Title': title,
        'Description': description,
        'Severity': severity,
        'CreatedAt': created_at,
        'Standards': standards,
    }
    return summary
