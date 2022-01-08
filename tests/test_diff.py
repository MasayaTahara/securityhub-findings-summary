import src.diff

import os
import csv
import pytest


def test_compare_and_get_summary_1():
    # Case1 1 MODIFIED
    previous = get_findings_from_csv(
        'tests/data/SecurityHub_findings_status_200001010000.csv')
    current = get_findings_from_csv(
        'tests/data/current_findings_1.csv')
    summary = get_findings_from_csv(
        'tests/data/summary_1.csv')

    assert summary == src.diff.compare_and_get_summary(
        current_findings_detail=current, previous_findings_detail=previous)


def test_compare_and_get_summary_2():
    # Case2 2 MODIFIED
    previous = get_findings_from_csv(
        'tests/data/SecurityHub_findings_status_200001020000.csv')
    current = get_findings_from_csv(
        'tests/data/current_findings_2.csv')
    summary = get_findings_from_csv(
        'tests/data/summary_2.csv')

    assert summary == src.diff.compare_and_get_summary(
        current_findings_detail=current, previous_findings_detail=previous)


def test_compare_and_get_summary_3():
    # Case3 NEW/MODIFIED
    previous = get_findings_from_csv(
        'tests/data/SecurityHub_findings_status_200001030000.csv')
    current = get_findings_from_csv(
        'tests/data/current_findings_3.csv')
    summary = get_findings_from_csv(
        'tests/data/summary_3.csv')

    assert summary == src.diff.compare_and_get_summary(
        current_findings_detail=current, previous_findings_detail=previous)


def test_compare_and_get_summary_4():
    # Case4 NEW/MODIFIED/DELETED
    previous = get_findings_from_csv(
        'tests/data/SecurityHub_findings_status_200001040000.csv')
    current = get_findings_from_csv(
        'tests/data/current_findings_4.csv')
    summary = get_findings_from_csv(
        'tests/data/summary_4.csv')

    assert summary == src.diff.compare_and_get_summary(
        current_findings_detail=current, previous_findings_detail=previous)


def get_findings_from_csv(file_name):
    findings = []
    with open(os.path.join(os.getcwd(), file_name), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            findings.append(row)
        return findings
