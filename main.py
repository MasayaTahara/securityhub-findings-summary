import os
from dotenv import load_dotenv
import boto3

load_dotenv()


def get_findings(client):
    paginator = client.get_paginator('get_findings')
    findings = []
    for p in paginator.paginate():
        findings_in_page = p.get('Findings')
        for f in findings_in_page:
            findings.append(f)
    return findings


def show_findings(findings):
    count = 0
    for f in findings:
        count += 1
        severity = f.get('Severity').get('Label')
        title = f.get('Title')
        resources = [r.get('Id') for r in f.get('Resources')]
        print("#{} / {} / {} / {}".format(count, severity, title, resources))


if __name__ == '__main__':
    client = boto3.client('securityhub')
    findings = get_findings(client)
    show_findings(findings)
