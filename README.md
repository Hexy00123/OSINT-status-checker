# OSINT Online Status Checker Tool

This tool monitors the online status of social media users with interactive analytics.

  Currently works only with Telegram accounts.

## Getting Started

### Prerequisites

- Python 3.11
- Docker & Docker Compose
- Telegram Account (for parsing)

### Setup

Copy the `.example.env` file to `.env`:
```bash
cp .example.env .env
```

### Usage

Run docker compose using the following command:
```bash
docker compose up
```
- Authorize Telegram Account for parsing by QR-code at [http://localhost:8000/qr/](http://localhost:8000/qr/)
- Go to [http://localhost:8501/](http://localhost:8501/)

### Additional Notes

- Swagger API at [http://localhost:8000/docs](http://localhost:8000/docs)
- Ensure that your Telegram account is not restricted from using the API.
- Be mindful of Telegram's terms of service and API usage policies.
