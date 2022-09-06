# VAmPISecurityTests
VAmPISecurityTests with python and pytest

## Description:
### PyTest program to test VAmPI https://github.com/erev0s/VAmPI vulnerable REST API with OWASP top 10 vulnerabilities
### This is still in development and will be updated with time.
### Currently tests for:
1. Unauthorized password change https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#unauthorized-password-change
### Disclaimer:
### Since the API is meant to be vulnerable, the tests will call it "passed" not because it is actually not vulnerable, but because it is vulnerable.
### Prerequisites
1. pip3 install -U pytest
2. Clone VAmPI, change ENV tokentimetolive=900 in Dockerfile
3. Docker build and then docker run

Run with: "pytest test_VAmPISecurityTests.py --verbose -s"

### Demo Gif
![](demo.gif)