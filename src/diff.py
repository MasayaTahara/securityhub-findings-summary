def get_summary(current_findings_detail, previous_findings_detail) -> list:
    current_findings_summary = []
    for current_finding in current_findings_detail:
        # for previous_finding in previous_findings_detail:
            #     print(previous_finding)

        current_findings_summary.append(create_summary_dict(
            finding_id=current_finding['FindingID'],
            resource_ids=current_finding['ResourceIds'],
            title=current_finding['Title'],
            description=current_finding['Description'],
            severity=current_finding['Severity'],
            created_at=current_finding['CreatedAt'],
            standards=current_finding['Standards'],
            # TODO: Status check logic needed
            status='NEW',
        ))
    return current_findings_summary


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
