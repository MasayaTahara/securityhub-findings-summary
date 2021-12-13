from dotenv import load_dotenv
import boto3

load_dotenv()
REGION = 'ap-northeast-1'


def get_findings(client):
    paginator = client.get_paginator('get_findings')
    response_iterator = paginator.paginate(
        Filters={
            'RecordState': [
                {
                    'Value': 'ACTIVE',
                    'Comparison': 'EQUALS'
                }
            ],
            'SeverityLabel': [
                {
                    'Value': 'CRITICAL',
                    'Comparison': 'EQUALS'
                },
                {
                    'Value': 'HIGH',
                    'Comparison': 'EQUALS'
                },
                {
                    'Value': 'MEDIUM',
                    'Comparison': 'EQUALS'
                },
                {
                    'Value': 'LOW',
                    'Comparison': 'EQUALS'
                },
            ]
        }
    )
    findings = []
    for p in response_iterator:
        findings_in_page = p.get('Findings')
        for f in findings_in_page:
            findings.append(f)
    return findings


def count_severity(findings):
    count_critical = 0
    count_high = 0
    count_medium = 0
    count_low = 0
    for f in findings:
        severity = f.get('Severity').get('Label')
        if severity == 'CRITICAL':
            count_critical += 1
        elif severity == 'HIGH':
            count_high += 1
        elif severity == 'MEDIUM':
            count_medium += 1
        elif severity == 'LOW':
            count_low += 1
    return [count_critical, count_high, count_medium, count_low]


def count_compliance_status(findings):
    count_failed = 0
    count_passed = 0
    for f in findings:
        compliance = f.get('Compliance')
        if compliance != None:
            compliance_status = compliance.get('Status')
            if compliance_status == 'FAILED':
                count_failed += 1
            elif compliance_status == 'PASSED':
                count_passed += 1
    return [count_failed, count_passed]


if __name__ == '__main__':
    client = boto3.client('securityhub',  region_name=REGION)
    findings = get_findings(client)
    print("Region: {}".format(REGION))
    print("Compliance status: [FAILED, PASSED] = {}".format(
        count_compliance_status(findings)))
    print("Findings: [CRITICAL, HIGH, MEDIUM, LOW] = {}".format(
        count_severity(findings)))
