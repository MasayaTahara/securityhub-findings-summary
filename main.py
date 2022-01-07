import json
import os
from dotenv import load_dotenv
import boto3
import fire

import get
import count
import detail

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

    def failed(self, output='failed_findings.json'):
        failed_findings = get.get_findings_by_compliance_status(
            self._client, compliance_status='FAILED')
        findings_detail = detail.get_findings_detail(failed_findings)
        with open(os.path.join(os.getcwd(), output), 'w') as f:
            json.dump(findings_detail, f, ensure_ascii=False, indent=4)

    def passed(self, output='passed_findings.json'):
        passed_findings = get.get_findings_by_compliance_status(
            self._client, compliance_status='PASSED')
        findings_detail = detail.get_findings_detail(passed_findings)
        with open(os.path.join(os.getcwd(), output), 'w') as f:
            json.dump(findings_detail, f, ensure_ascii=False, indent=4)

    def summary(self, diff):
        failed_findings = get.get_findings_by_compliance_status(
            self._client, compliance_status='FAILED')


if __name__ == '__main__':
    cli = Cli()
    fire.Fire(cli)
