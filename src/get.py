def get_all_findings(client):
    paginator = client.get_paginator('get_findings')
    response_iterator = paginator.paginate(
        Filters={
            'RecordState': [
                {
                    'Value': 'ACTIVE',
                    'Comparison': 'EQUALS'
                }
            ],
        }
    )
    findings = []
    for p in response_iterator:
        findings_in_page = p.get('Findings')
        for f in findings_in_page:
            findings.append(f)
    return findings


def get_findings_by_compliance_status(client, compliance_status='FAILED'):
    paginator = client.get_paginator('get_findings')
    response_iterator = paginator.paginate(
        Filters={
            'RecordState': [
                {
                    'Value': 'ACTIVE',
                    'Comparison': 'EQUALS'
                }
            ],
            'ComplianceStatus': [
                {
                    'Value': compliance_status,
                    'Comparison': 'EQUALS'
                }
            ]
        }
    )
    findings = []
    for p in response_iterator:
        findings_in_page = p.get('Findings')
        for f in findings_in_page:
            findings.append(f)
    return findings
