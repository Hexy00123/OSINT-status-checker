# OSINT Online Status Checker Tool

This tool monitors the online status of Telegram users with interactive analytics.

## Getting Started

### Prerequisites

- Python 3.11

### Setup

1. **Obtain Telegram API Credentials:**
   - Visit [my.telegram.org](https://my.telegram.org/auth?to=apps) and log in with your Telegram account.
   - Fill out the form to create a new application and save the `api_id` and `api_hash`.

2. **Configure Environment Variables:**
   - Copy the `example.env` file to `.env`:
     ```bash
     cp example.env .env
     ```
   - Open the `.env` file and fill in the following details:
     - `api_id`: Your Telegram API ID.
     - `api_hash`: Your Telegram API hash.
     - `chat_ids`: List of chat IDs from which to monitor users.

3. **Install Dependencies:**
   - Run the installation script to set up the required packages:
     ```bash
     bash scripts/install_requirements.sh
     ```

### Usage

- Run the tool using the following command:
  ```bash
  cd src
  python parser.py
  ```

### Additional Notes

- Ensure that your Telegram account is not restricted from using the API.
- Be mindful of Telegram's terms of service and API usage policies.
