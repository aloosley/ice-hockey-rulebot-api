# Ice Hockey Rulebot API
## Getting Started

### Environment Variables

You will need a `.env` file in the root directory that looks like the following
```env
OPENAI_API_KEY="xxxx"  # Your OpenAI API key
PINECONE_API_KEY="xxxx"  # Your Pinecone API key
PINECONE_ENVIRONMENT="xxx"  # Your Pinecone environment name
INDEX_NAME=iihf-rulebook

API_KEY=xxxx  # Password protection for API (just use one letter like "a" for testing)
```

# Getting Started

## Start the App
1. Ensure Docker is installed
1. Run
   ```commandline
   docker compose up --build
   ```
1. The app will be available at <http://localhost:8000>

## Taskfile
Using the Taskfile CLI gives a list of scripts for installing and running.
Here are instructions for [installing task](https://taskfile.dev/installation/).

Once installed, simply run
```commandline
task
```
for a list of all available tasks.

## Development and Experiments
* Install the dev dependencies: `pip install -e ".[dev]"`
* Install pre-commit hooks: `pre-commit install -t pre-commit -t pre-push`
* Development should be done on a feature-branch - commit and push often and share your work via pull request draft
* For new experiments, consider creating a new notebook based on `[iihf-qa-v2.ipynb](notebooks%2Fiihf-qa-v2.ipynb)`
