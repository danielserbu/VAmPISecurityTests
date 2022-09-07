# VAmPISecurityTests
VAmPISecurityTests with python and pytest

## Description:
### PyTest program to test VAmPI https://github.com/erev0s/VAmPI vulnerable REST API with OWASP top 10 vulnerabilities
### This is still in development and will be updated with time.
### Currently tests for:
1. SQL Injection https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#sql-injection
2. Unauthorized password change https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#unauthorized-password-change
3. Mass Assignment https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#mass-assignment
4. Excessive data exposure https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#excessive-data-exposure
5. User and Password Enumeration https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#user-and-password-enumeration
6. Rate Limiting https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#lack-of-resources-amp-rate-limiting
### Currently undone tests:
1. RegexDOS (Denial of service) https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#regexdos-denial-of-service
2. Broken Object Level Authorization https://erev0s.com/blog/vampi-vulnerable-api-security-testing/#broken-object-level-authorization
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