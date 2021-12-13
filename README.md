# securityhub-findings-summary
Create summary of AWS Security Hub findings

```sh
❯ poetry run python main.py count
Region: ap-northeast-1
Compliance status: [FAILED, PASSED] = [36, 381]
Findings: [CRITICAL, HIGH, MEDIUM, LOW] = [5, 2, 16, 18]
```


## Set up
```sh
# Set environment variables
cp .env.sample .env
# Edit .env

# Install packages
poetry install

# Count severity
poetry run python main.py count
```
