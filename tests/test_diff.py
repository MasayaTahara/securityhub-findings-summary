import src.diff

import os
import csv


def test_get_summary():

    # Case1 NEW/MODIFIED/DELETED

    previous = get_findings_from_csv(
        'tests/data/SecurityHub_findings_status_200001010000.csv')
    current = get_findings_from_csv(
        'tests/data/current_findings_1.csv')
    summary = get_findings_from_csv(
        'tests/data/SecurityHub_findings_status_200001030000.csv')

    assert summary == src.diff.get_summary(
        current_findings_detail=current, previous_findings_detail=previous)


def get_findings_from_csv(file_name):
    findings = []
    with open(os.path.join(os.getcwd(), file_name), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            findings.append(row)
        return findings
