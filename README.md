<p align="center"><img src="https://raw.githubusercontent.com/nikhiljohn10/cloudflare-api/main/assets/images/logo.svg?sanitize=true" height="130"></p>

[![Publish Package](https://github.com/nikhiljohn10/cloudflare-api/actions/workflows/publish.yml/badge.svg)](https://github.com/nikhiljohn10/cloudflare-api/actions/workflows/publish.yml) [![PyPI - Status](https://img.shields.io/pypi/status/cloudflare-api)](https://pypi.org/project/cloudflare-api) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/nikhiljohn10/cloudflare-api)](https://github.com/nikhiljohn10/cloudflare-api/releases) [![PyPI](https://img.shields.io/pypi/v/cloudflare-api)](https://pypi.org/project/cloudflare-api) [![CodeFactor](https://www.codefactor.io/repository/github/nikhiljohn10/cloudflare-api/badge)](https://www.codefactor.io/repository/github/nikhiljohn10/cloudflare-api) [![GitHub license](https://img.shields.io/github/license/nikhiljohn10/cloudflare-api)](https://github.com/nikhiljohn10/cloudflare-api/blob/main/LICENSE)

Python client for Cloudflare API v4

> Require Python 3.9+

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

Then run the following command in terminal:
```bash
make init
. venv/bin/activate
make test
```

If it is running for first time, you will be asked to enter API Token. Paste the api token copied from Dashboard.

## Example

For this example, `poetry` is used for easy setup.
```bash
python3 -m pip install --user poetry
mkdir -p myapp && cd myapp
poetry init -n
poetry add cloudflare-api
```

Copy the code below in to a new file `./myapp/app.py`.
```python
#!/usr/bin/env python3

from CloudflareAPI import Cloudflare

def main():
  cf = Cloudflare()

  print(cf.account.list())
  print(cf.user.details())
  print(cf.worker.list())
  print(cf.store.list())

if __name__ == "__main__":
    main()
```

You can now run the program using following command:
```bash
poetry run python app.py
```

If it is running for first time, you will be asked to enter API Token. Paste the api token copied from Dashboard. This will create `cf-config.ini` file in your current working directory for future reference of the api token.

You can find more examples in [`examples`](https://github.com/nikhiljohn10/cloudflare-api/tree/main/examples) directory

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

  ### AccountData

  ### AccountSettings

### User

- `details` - Display details of the account's user

  ### UserData

### Worker

- `list` - List all existing workers
- `upload` - Upload a new worker with binding if given
  - Upload file along as javascript
  - Upload file along with metadata as multipart form-data
    - KV Bindings
    - Environment variables
    - Secrets
- `download` - Download an existing worker
- `deploy` - Deploy an existing worker using the subdomain
- `undeploy` - Undeploy an existing worker
- `delete` - Delete an existing worker

  ### Subdomain

  - `create` - Create a new subdomain if none exists
  - `get` - Get the current subdomain from cloudflare account

  ### Cron

  - `update` - Update an existing cron or create new cron for a worker
  - `get` - Get the cron task list of specified worker

### Store(Workers KV)

- `list` - List all existing Namespaces
- `get_ns` - Returns requested Namespace object
- `create` - Create a new namespace
- `rename` - Rename an existing namespace
- `delete` - Delete an existing namespace

  ### Namespace
  
  - `keys` - Display all the keys in the Namespace
  - `read` - Read the value of given key in the Namespace
  - `write` - Write given key-value pair to the Namespace
  - `bulk_write` - Write given key-value pairs in bulk to the Namespace
  - `delete` - Delete given key from the Namespace
  - `bulk_delete` - Delete given keys in bulk from the Namespace

    ### Metadata

    ### NSKey

    ### NSBundler

    - `add` - Add key-value pair with metadata to bundler

**( * : Not accessable with default Worker permissions )**

## Development

### Version Bump

To display current version:
```
make version
```

To bump to new version, where x.y.z is major,minor & patch versions respectively:
```
make VERSION=x.y.z bump
```

The above command does the following:

1. Update version in `__version__.py` inside package
2. Create a commit for the above change
3. Tag the commit with VERSION
4. Push the content in to main branch with tags
5. Python publish workflow action activates
6. Release the version pushed
7. Build python package
8. Publish python package in to pypi.org
