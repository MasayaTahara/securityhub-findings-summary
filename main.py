import json
import os
from dotenv import load_dotenv
import boto3
import fire

load_dotenv()
REGION = 'ap-northeast-1'


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


def create_finding_str(compliance_status: str, severity_label: str, title: str, description: str, resource_ids: list) -> dict:
    finding = {
        'ComplianceStatus': compliance_status,
        'SeverityLabel': severity_label,
        'Title': title,
        'Description': description,
        'ResourceIds': resource_ids
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
            finding_detail = create_finding_str(
                compliance_status=compliance_status, severity_label=severity, title=title, description=description, resource_ids=resource_ids)
            findings_detail.append(finding_detail)
    return findings_detail


class Cli(object):

    def __init__(self):
        self._client = boto3.client('securityhub',  region_name=REGION)

    def count(self):
        findings = get_all_findings(self._client)
        print("Region: {}".format(REGION))
        print("Compliance status: [FAILED, PASSED] = {}".format(
            count_compliance_status(findings)))
        print("Findings: [CRITICAL, HIGH, MEDIUM, LOW] = {}".format(
            count_severity(findings)))

    def failed(self, file_path='failed_findings.json'):
        failed_findings = get_findings_by_compliance_status(
            self._client, compliance_status='FAILED')
        findings_detail = get_findings_detail(failed_findings)
        with open(os.path.join(os.getcwd(), file_path), 'w') as f:
            json.dump(findings_detail, f, ensure_ascii=False, indent=4)

    def passed(self, file_path='passed_findings.json'):
        passed_findings = get_findings_by_compliance_status(
            self._client, compliance_status='PASSED')
        findings_detail = get_findings_detail(passed_findings)
        with open(os.path.join(os.getcwd(), file_path), 'w') as f:
            json.dump(findings_detail, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    cli = Cli()
    fire.Fire(cli)
