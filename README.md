# Python Flask SSO Proof of Concept (PoC)

This repository contains a minimal proof-of-concept implementation of Single Sign-On (SSO) using the SAML protocol in a Python Flask application. It demonstrates how to integrate a Python web app with an Identity Provider (IdP) for centralized authentication using the OneLogin Python SAML Toolkit.

***

## Features

- SAML-based SSO login and logout
- SP (Service Provider) metadata endpoint for IdP integration
- User session management after successful authentication
- Simple Flask web app structure with clear SSO flow

***

## Prerequisites

- Python 3.10+
- An Identity Provider supporting SAML 2.0 (e.g., Okta, OneLogin, Azure AD)
- Flask and python3-saml library (listed in requirements.txt)

***

## Setup Instructions

1. **Clone this repository:**

```bash
git clone <repo-url>
cd flask_sso_poc
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure SAML settings:**
    - Edit the `settings.json` file with your Identity Provider’s metadata:
        - IdP entity ID
        - Single Sign-On and Single Logout URLs
        - IdP x509 certificate
    - Update the Service Provider URLs if your app is not running locally.
5. **Run the Flask application:**

```bash
python app.py
```

6. **Access the app:**
    - Open `http://localhost:5000` in your browser.
    - You will be redirected to your configured IdP for login.
    - Upon successful login, you will be redirected back to the app and logged in.

***

## Application Endpoints

- `/` — Protected homepage; requires SSO authentication.
- `/login/` — Initiates the SSO login flow by redirecting to the IdP.
- `/acs/` — Assertion Consumer Service endpoint; receives SAML responses.
- `/logout/` — Logs out from the app and optionally from the IdP.
- `/metadata/` — Provides SP metadata XML for IdP integration.

***

## Notes and Best Practices

- Always run the app behind HTTPS in production.
- Secure your Flask secret key appropriately.
- Ensure the clock on your server and IdP are synchronized.
- Validate and handle SAML responses securely to avoid security risks.
- This PoC is intended for learning and testing; adapt it carefully for production environments.

***

## Troubleshooting

- If you encounter login errors, check the logs for SAML response validation issues.
- Ensure your `settings.json` matches exactly with your IdP metadata values.
- Confirm callback URLs configured in the IdP correspond to your Flask app endpoints.

***

## References

- [OneLogin Python SAML Toolkit](https://github.com/onelogin/python3-saml)
- [SAML 2.0 Specifications](https://docs.oasis-open.org/security/saml/v2.0/)
