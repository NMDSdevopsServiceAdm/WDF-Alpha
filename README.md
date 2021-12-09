# WDF Alpha Prototype

This repo contains prototype code produced during the Skills for Care Workforce Development Fund Alpha phase to get feedback on designs and assumptions. The objective was to learn through prototyping rather than deliver production grade code.

## Setup

```sh
# Install python packages
poetry install

# Install frontend packages, build the frontend
npm ci
npm run build

# Init DB
./manage.py migrate

# Import data
./manage.py import_qualifications
./manage.py import_employees  # fake data
./manage.py import_providers

# Start app
./manage.py runserver
```

## Configuration

Env vars can be used to set

- `DEBUG`
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `DATABASE_URL`

If not set, development defaults will be assumed

## Testing values

- Use the qualification number `603/3496/4` to make a claim
- On the employee search page, the search works, but pressing search with nothing in the box will show the full list of fake people
- A valid ULN will be pre-populated but any 10 digit number starting with 2 (e.g: `2000000001`, `2000000002`, etc) is valid. To test the invalid cases:
  - `1000000001` will throw name does not match learner
  - `1000000002` will throw partial name match
  - Any other value (e.g: `1000000003`, but also `abc`) will throw invalid ULN
