# cloudflare-api

[![Python Package](https://github.com/nikhiljohn10/cloudflare-api/actions/workflows/python-publish.yml/badge.svg)](https://github.com/nikhiljohn10/cloudflare-api/actions/workflows/python-publish.yml) ![PyPI - Status](https://img.shields.io/pypi/status/cloudflare-api) [![PyPI](https://img.shields.io/pypi/v/cloudflare-api)](https://pypi.org/project/cloudflare-api) [![CodeFactor](https://www.codefactor.io/repository/github/nikhiljohn10/cloudflare-api/badge)](https://www.codefactor.io/repository/github/nikhiljohn10/cloudflare-api) [![GitHub license](https://img.shields.io/github/license/nikhiljohn10/cloudflare-api)](https://github.com/nikhiljohn10/cloudflare-api/blob/main/LICENSE)

Python client for Cloudflare API v4

## Usage

### Python Package

```bash
pip install cloudflare-api
```

Sample code can be found inside [/test.py](https://github.com/nikhiljohn10/cloudflare-api/blob/main/test.py) 

### Source Code

```bash
git clone https://github.com/nikhiljohn10/cloudflare-api
cd cloudflare-api
```

### Instructions to get new API Token
1. Go to [Dashboard](https://dash.cloudflare.com/profile/api-tokens)
2. Create Token
3. Use `Edit Cloudflare Workers` template
4. Select one account from **Account Resources**
5. Select `All Zones` or specific zones under **Zone Resources**
6. Continue to summary
7. Create Token
8. Copy the token and save it somewhere secret & secure.

Create a `secret.py` in the root directory with following content and replace `API_TOKEN`'s value with the token obtained from Cloudflare Dashboard:
```python
API_TOKEN = "API_TOKEN"
```

Then run the following command in terminal:
```bash
make test
```

> *Note: The `secret.py` file is ignored by git*

## Example

For this example, `poetry` is used for easy setup.
```bash
python3 -m pip install poetry
poetry new cloudflare-app
cd cloudflare-app
poetry add cloudflare-api
```

Copy the code below in to a new file `./cloudflare-app/__main__.py`.
```python
#!/usr/bin/env python3

from CloudflareAPI import Cloudflare, jsonPrint

def main():
  cf = Cloudflare(token="API_TOKEN")
  print(cf.worker.list())
  print(cf.store.list())
```
Now replace `API_TOKEN` values with values obtained from Cloudflare dashboard. You can now run the program using following command:
```
poetry run python cloudflare-app
```

## Default Permissions

**1. Account**
   - Workers Tail ( Read )
   - Workers KV Storage ( Edit )
   - Workers Scripts ( Edit )
   - Account Settings ( Read )

**2. Zones**
   - Workers Routes ( Edit )

**3. Users**
   - User Details ( Read )

## Available endpoints

### Account

- `list` - List all accounts where given token have access
- `get_id` - Return account id if only one account exists. Otherwise display all accounts availabe and exit.
- `details` - Display details of an account
- `rename`__*__ - Rename an existing account 

### Worker

- `list` - List all existing workers
- `upload` - Upload a new worker with binding if given
- `download` - Download an existing worker
- `deploy` - Deploy an existing worker using the subdomain
- `undeploy` - Undeploy an existing worker
- `delete` - Delete an existing worker

  ### Subdomain

  - `create` - Create a new subdomain if none exists
  - `get` - Get the current subdomain from cloudflare account

### Store(Workers KV)

- `list` - List all existing Namespaces
- `get_id` - Find the namespace id of the namespace
- `create` - Create a new namespace
- `rename` - Rename an existing namespace
- `delete` - Delete an existing namespace

**( * : Not accessable with default Worker Token )**