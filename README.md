# OSINT Online Status Checker Tool

This tool monitors the online status of social media users with interactive analytics.

## Getting Started with Telegram parser

### Prerequisites

- Python 3.11

### Setup

1. **Obtain Telegram API Credentials:**
   - Visit [my.telegram.org](https://my.telegram.org/auth?to=apps) and log in with your Telegram account.
   - Fill out the form to create a new application and save the `api_id` and `api_hash`.

2. **Configure Environment Variables:**
   - Copy the `.example.env` file to `.env`:
     ```bash
     cp .example.env .env
     ```
   - Open the `.env` file and fill in the following details:
     - `api_id`: Your Telegram API ID.
     - `api_hash`: Your Telegram API hash.

3. **Install Dependencies:**
   - Set up the required packages:
     ```bash
      cd tg_scrapper
      pip install --upgrade pip
      pip install -r requirements.txt
     ```

### Usage

- Run the tool using the following command:
  ```bash
  cd src
  python3 main.py
  ```

### Additional Notes

- Ensure that your Telegram account is not restricted from using the API.
- Be mindful of Telegram's terms of service and API usage policies.
