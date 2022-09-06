# VAmPISecurityTests
VAmPISecurityTests with python and pytest

## Description:
### PyTest program to test VAmPI https://github.com/erev0s/VAmPI vulnerable REST API with OWASP top 10 vulnerabilities
### This is still in development and will be updated with time.
### Currently tests for:
1. Unauthorized password change https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#unauthorized-password-change
2. SQL Injection https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#sql-injection
### Prerequisites
1. pip3 install -U pytest
2. Clone VAmPI
3. Build and run a vulnerable VAmPI "docker run -d -e vulnerable=1 -e tokentimetolive=800 -p 5000:5000 vampire_docker:latest"
4. Docker build and then docker run
5. Build and run a non vulnerable VAmPI "docker run -d -e vulnerable=0 -e tokentimetolive=800 -p 5050:5050 vampire_docker:latest"
6. Docker build and then docker run


Run with: "pytest test_VAmPISecurityTests.py --verbose -s"

### Demo Gif
![](demo.gif)