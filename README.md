# securityhub-findings-summary
Create summary of AWS Security Hub findings

```sh
# Count findings
poetry run python main.py count
Region: ap-northeast-1
Compliance status: [FAILED, PASSED] = [36, 381]
Findings: [CRITICAL, HIGH, MEDIUM, LOW] = [5, 2, 16, 18]

# Show failed findings with file name "failed_findings.csv"
poetry run python main.py failed

# Show passed findings with file name "passed_findings.csv"
poetry run python main.py passed
```


## Set up
```sh
# Install tool
brew install poetry

# Set environment variables
cp .env.sample .env
# Edit .env

# Install packages
poetry install

# Show help
poetry run python main.py --help
```
