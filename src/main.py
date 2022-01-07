import csv
import os
from dotenv import load_dotenv
import boto3
import fire
import datetime

import get
import count
import detail
import diff

load_dotenv()
REGION = 'ap-northeast-1'


class Cli(object):

    def __init__(self):
        self._client = boto3.client('securityhub',  region_name=REGION)

    def count(self):
        findings = get.get_all_findings(self._client)
        print("Region: {}".format(REGION))
        print("Compliance status: [FAILED, PASSED] = {}".format(
            count.count_compliance_status(findings)))
        print("Findings: [CRITICAL, HIGH, MEDIUM, LOW] = {}".format(
            count.count_severity(findings)))

    def failed(self, output='failed_findings.csv'):
        failed_findings = get.get_findings_by_compliance_status(
            self._client, compliance_status='FAILED')
        findings_detail = detail.get_findings_detail(failed_findings)

        with open(os.path.join(os.getcwd(), output), 'w') as f:
            labels = findings_detail[0].keys()
            writter = csv.DictWriter(f, fieldnames=labels)
            writter.writeheader()
            writter.writerows(findings_detail)

    def passed(self, output='passed_findings.csv'):
        passed_findings = get.get_findings_by_compliance_status(
            self._client, compliance_status='PASSED')
        findings_detail = detail.get_findings_detail(passed_findings)

        with open(os.path.join(os.getcwd(), output), 'w') as f:
            labels = findings_detail[0].keys()
            writter = csv.DictWriter(f, fieldnames=labels)
            writter.writeheader()
            writter.writerows(findings_detail)

    def summary(self, previous):
        failed_findings = get.get_findings_by_compliance_status(
            self._client, compliance_status='FAILED')
        current_findings_detail = detail.get_findings_detail(failed_findings)

        # Read .csv (previous finding summary)
        with open(os.path.join(os.getcwd(), previous), 'r') as f:
            previous_findings_detail = csv.DictReader(f)

        # Compare current findings and previous findings
        current_findings_summary = diff.get_summary(
            current_findings_detail=current_findings_detail,
            previous_findings_detail=previous_findings_detail
        )

        # Write .csv
        now = datetime.datetime.now()
        output = 'SecurityHub_findings_status_{0:%Y%m%d%H%M}.csv'.format(now)
        with open(os.path.join(os.getcwd(), output), 'w') as f:
            labels = current_findings_summary[0].keys()
            writter = csv.DictWriter(f, fieldnames=labels)
            writter.writeheader()
            writter.writerows(current_findings_summary)


if __name__ == '__main__':
    cli = Cli()
    fire.Fire(cli)
