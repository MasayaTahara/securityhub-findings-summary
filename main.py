import os
from dotenv import load_dotenv
import boto3

load_dotenv()
REGION = 'ap-northeast-1'


def get_findings(client):
    paginator = client.get_paginator('get_findings')
    findings = []
    for p in paginator.paginate():
        findings_in_page = p.get('Findings')
        for f in findings_in_page:
            findings.append(f)
    return findings


def count_findings(findings):
    count_critical = 0
    count_high = 0
    count_medium = 0
    count_low = 0
    for f in findings:
        record_state = f.get('RecordState')
        if record_state == 'ACTIVE':
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


if __name__ == '__main__':
    client = boto3.client('securityhub',  region_name=REGION)
    findings = get_findings(client)
    print("Region: {}".format(REGION))
    print("Findings: [CRITICAL, HIGH, MEDIUM, LOW] = {}".format(
        count_findings(findings)))
