#!/usr/bin/env python3

from CloudflareAPI import Cloudflare
from CloudflareAPI import jp

from secret import API_TOKEN, ACCOUNT_ID

def main():
    cf = Cloudflare(token=API_TOKEN, account_id=ACCOUNT_ID)
    workers = cf.worker.list()
    jp(workers)

if __name__ == "__main__":
    main()
