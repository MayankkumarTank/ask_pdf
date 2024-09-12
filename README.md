## Run service locally

### Install the requirements and set up the third-party services

Open the repo and set up a new Python virtual environment.

```commandline
source .venv/bin/activate
pip install -r requirements.txt
```

### Setup the .env file

Create the .env file at the project root and add these environment variables.

```commandline
OPENAI_API_KEY="xxxxxxxxx"
SLACK_TOKEN="xxxxxxxx"
```

### Run

After completing above step, you are good to go. Just run the main.py file.

```commandline
python main.py
```
