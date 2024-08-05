# Defog Desktop

Defog is a privacy friendly AI data analyst that lets you ask data questions in plain English, while ensuring that your actual data never leaves your servers.

## Getting Started

1. If you have not yet gotten a Defog API Key, sign up at https://defog.ai/signup to get a free API key! The free key lets you query up to 5 tables with 25 total columns, and up to 1000 queries per month.
2. Install requirements with `pip install -r requirements.txt`
3. Update `config.env` with your API Key
4. Launch defog with `python main.py`. This will automatically open up http://localhost:33364/static/extract-metadata.html in your browser.
5. If this is your first time using defog, log in with the user id `admin`, and the password `admin`
