# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Current (main branch) | ✅ |
| Previous versions | ❌ |

## Reporting a Vulnerability

### How to Report

If you discover a security vulnerability in this project, please report it responsibly.

**Do NOT**:
- Open a public issue
- Discuss the vulnerability in public channels
- Exploit the vulnerability for any purpose

**DO**:
- Send an email to: security@cognition.ai
- Include detailed information about the vulnerability
- Provide steps to reproduce (if possible)
- Allow us 90 days to address the vulnerability before public disclosure

### What to Include in Your Report

Please include the following information in your vulnerability report:

1. **Description**: A clear description of the vulnerability
2. **Impact**: The potential impact of the vulnerability
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Affected Versions**: Which versions are affected
5. **Suggested Fix** (optional): Any suggestions for fixing the issue

### Response Timeline

- **Initial Response**: Within 48 hours
- **Detailed Analysis**: Within 7 business days
- **Fix Timeline**: Within 90 days (depending on severity)
- **Public Disclosure**: After fix is deployed and tested

### Coordinated Disclosure

We follow responsible disclosure practices:
- We will work with you to understand and validate the vulnerability
- We will keep you informed of our progress
- We will credit you in the security advisory (if desired)
- We will coordinate the public disclosure timeline with you

## Security Features

### Built-in Security Measures

This project includes multiple layers of security:

1. **Static Application Security Testing (SAST)**
   - Bandit for Python security issues
   - Semgrep for custom security rules
   - Automated on every push and PR

2. **Dependency Scanning**
   - Safety for Python package vulnerabilities
   - pip-audit for dependency security
   - Trivy for comprehensive vulnerability scanning
   - Dependabot for automated dependency updates

3. **Secrets Detection**
   - Gitleaks for secret detection in code
   - TruffleHog for advanced secret scanning
   - Pre-commit hooks to prevent secrets from being committed

4. **Code Quality**
   - Black for code formatting
   - Flake8 for linting
   - Pylint for code quality checks
   - isort for import sorting

5. **Infrastructure Security**
   - Checkov for IaC security (if applicable)
   - Container security scanning with Trivy
   - Security Scorecard for supply chain security

6. **License Compliance**
   - Automatic license checking
   - SPDX license verification

## Security Best Practices

### For Developers

1. **Never commit secrets**
   - Use environment variables for sensitive data
   - Never hardcode API keys, passwords, or tokens
   - Use `.env` files (never commit them)

2. **Keep dependencies updated**
   - Review Dependabot PRs promptly
   - Test dependency updates thoroughly
   - Pin critical dependency versions

3. **Follow secure coding practices**
   - Validate all user inputs
   - Use parameterized queries to prevent SQL injection
   - Implement proper error handling
   - Use encryption for sensitive data

4. **Use pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Run security scans locally**
   ```bash
   # Run Bandit
   bandit -r .

   # Run Safety
   safety check

   # Run Gitleaks
   gitleaks detect --source .
   ```

### For Operations

1. **Environment Variables**
   - Store secrets in GitHub Secrets or equivalent
   - Rotate credentials regularly
   - Use different credentials for different environments

2. **Access Control**
   - Implement least privilege access
   - Use multi-factor authentication
   - Regular access reviews

3. **Monitoring**
   - Enable security logging
   - Set up alerts for suspicious activity
   - Regular security audits

## Security Configuration Files

### Key Security Files

- `.github/workflows/security-ci.yml` - CI/CD security pipeline
- `.github/dependabot.yml` - Automated dependency updates
- `.pre-commit-config.yaml` - Pre-commit security hooks
- `pyproject.toml` - Tool configurations
- `.gitignore` - Prevents sensitive files from being committed

### Environment Variables

Required environment variables (set in GitHub Secrets or `.env`):

```bash
# API Keys
ANTHROPIC_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here

# Optional Security Tools
SEMGREP_APP_TOKEN=your_semgrep_token
GITLEAKS_LICENSE=your_gitleaks_license

# LangSmith (optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=rfp-proposal-generator
```

## Dependency Management

### Automated Updates

We use Dependabot for automated dependency updates:
- Weekly checks for Python dependencies
- Weekly checks for GitHub Actions
- Security alerts for vulnerable dependencies
- Automated PR creation for updates

### Manual Review Process

1. Review Dependabot PRs promptly
2. Test changes in a development environment
3. Check for breaking changes
4. Review changelogs for security fixes
5. Merge and deploy to production

### Vulnerability Response

When a vulnerability is discovered in a dependency:

1. **Critical (CVSS 9.0+)**: Fix within 48 hours
2. **High (CVSS 7.0-8.9)**: Fix within 7 days
3. **Medium (CVSS 4.0-6.9)**: Fix within 30 days
4. **Low (CVSS 0.1-3.9)**: Fix in next regular update

## Incident Response

### Severity Levels

- **Critical**: Immediate threat to data security or system integrity
- **High**: Significant security issue requiring urgent attention
- **Medium**: Security issue that should be addressed soon
- **Low**: Minor security issue with limited impact

### Response Process

1. **Detection**: Automated monitoring or reporter
2. **Triage**: Assess severity and impact
3. **Containment**: Implement immediate mitigation
4. **Eradication**: Remove root cause
5. **Recovery**: Restore normal operations
6. **Lessons Learned**: Document and improve processes

## Security Audits

### Regular Security Reviews

- **Code Reviews**: All code goes through security-focused review
- **Dependency Audits**: Quarterly review of all dependencies
- **Penetration Testing**: Annual penetration testing
- **Compliance Checks**: Regular compliance verification

### Third-Party Security Tools

We use several third-party security tools:
- GitHub Advanced Security (Code Scanning, Secret Scanning)
- Semgrep for custom security rules
- Trivy for vulnerability scanning
- Safety for Python package security
- Gitleaks for secret detection

## Compliance

This project aims to comply with:

- **OWASP Top 10**: Protection against common web vulnerabilities
- **CIS Controls**: Implementation of critical security controls
- **NIST Cybersecurity Framework**: Alignment with NIST guidelines
- **SOC 2**: Security, availability, and processing integrity

## Security Contacts

- **Security Team**: security@cognition.ai
- **GitHub Security Advisory**: Use GitHub's security advisory feature
- **Emergency Contact**: [To be configured]

## Acknowledgments

We thank all security researchers who responsibly report vulnerabilities to help improve the security of this project.

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Controls](https://www.cisecurity.org/controls/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

**Last Updated**: April 24, 2026