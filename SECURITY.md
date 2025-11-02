# Security Policy

## 📒 Reporting Security Vulnerabilities

We take the security of Sturgeon AI seriously. If you discover a security vulnerability, please report it to us as soon as possible.

### 📨 How to Report

**Please DO NOT report security vulnerabilities publicly (e.g., via GitHub Issues).**

Instead, please send an email to:
- “ **security@sturgeon-ai.com**

Please include:
- Detailed description of the vulnerability
- Steps to reproduce the issue
- Potential impact of the vulnerability
- Any possible mitigations you've identified

## 🛄️ Response Time

We aim to respond to security reports within:
- **24 hours**: Initial acknowledgment
- **7 days**: Detailed response with timeline
- **90 days**: Resolution or mitigation plan

## 🔰‍⚖️ Security Measures

### Authentication & Authorization
- ✅ **JWT Token Authentication**: All API endpoints use JWT tokens for authentication
- ✅ **Password Hashing**: Passwords are hashed using bcrypt with salt rounds >= 10
- ✅ **Role-Based Access Control (RBAC)**: Users have specific roles (free, pro, enterprise)
- ✅ **Session Management**: Secure session handling with HTTPOnly cookies

### Data Protection
- 💤 **Encryption at Rest**: All sensitive data is encrypted in the database
- 💤 **Encryption in Transit**: All communication uses TLS 1.2+ 
- 💤 **Environment Variables**: Sensitive configs are stored in .env.local (never committed)
- 💤 **API Keys**: Stripe and other API keys are stored securely

### Application Security
- 🛟 **Input Validation**: All user input is validated and sanitized
- 🛟 **SQL Injection Protection**: Using Supabase ORM with parameterized queries
- 🛜 **XSS Protection**: All output is sanitized and Content Security Policy (CSP) will be enabled
- 🛜 **CSRF Protection**: All forms use CSRF tokens
- 🛜 **Rate Limiting**: API endpoints have rate limits to prevent abuse

### Dependency Security
- 📦 **Automated Scanning**: Dependabot enabled for vulnerability alerts
- 📦 **Regular Updates**: Dependencies are regularly updated to latest secure versions
- 📦 **Lockfiles**: Using package-lock.json/vercel.lock for deterministic builds

### Infrastructure Security
- 📟 **Hosting**: Vercel with enterprise security features
- 📟 **Database**: Supabase with Row Level Security (RLS) enabled
- 📟 **Payments**: Stripe PCI compliant payment processing
- 📟 **Backups**: Automated daily backups of critical data

## 📋 Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------|
| 2.0.x   | ✅ Supported       |
| 1.x.x   | ✅ Supported       |
| < 1.0   | ❌ Not Supported   |

## 📜 Compliance

- ✕ **GDPR**: Compliant with EU data protection regulations
- ╕ **CCPA**: Compliant with California Consumer Privacy Act
- ╕ **SOC 2**: Third-party services (Vercel, Supabase, Stripe) are SOC 2 compliant

## 🔐 Auditing & Logging

- **Audit Logs**: All authentication attempts are logged
- **Error Monitoring**: Centralized error tracking and alerting
- **Access Logs**: All API access is logged and monitored

## 🦮 Best Practices for Users

1. **Use Strong Passwords**: Minimum 8 characters with mix of upper/lower case, numbers, and special characters
2. **Enable 2FA**: Two-factor authentication will be available soon
3. **Keep API Keys Secure**: Never share or commit API keys to public repositories
4. **Regular Account Reviews**: Review account activity and connected applications
5. **Report Suspicious Activity**: Contact support immediately if you notice anything unusual

## 🔗 Security Updates
	Notifications about security updates will be posted to:
- GitHub Security Advisories
- Official blog at https://sturgeon-ai.com/blog
- Twitter @sturgeonai

## 💋 Contact

For general security questions (non-vulnerability related):
- 📧 Email: support@sturgeon-ai.com
- 💬 Website: https://sturgeon-ai.com

---

**Thank you for helping keep Sturgeon AI and our users safe!** 💚 💙