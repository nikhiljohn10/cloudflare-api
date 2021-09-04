#!/usr/bin/env python3

from typing import List, Optional
from CloudflareAPI.core import CFBase
from CloudflareAPI.dataclass.account import AccountData, AccountSettings
from CloudflareAPI.exceptions import CFError
from CloudflareAPI.utils import jsonPrint


class Account(CFBase):
    def __init__(self) -> None:
        self.__list: Optional[List[AccountData]] = None
        self.request = self.get_request("accounts")
        self.id = self.get_id()
        self.details()

    def __get_object(self, account: AccountData):
        return AccountData(
            id=account["id"],
            name=account["name"],
            settings=AccountSettings(
                enforce_twofactor=account["settings"]["enforce_twofactor"],
                access_approval_expiry=account["settings"]["access_approval_expiry"],
                use_account_custom_ns_by_default=account["settings"][
                    "use_account_custom_ns_by_default"
                ],
            ),
            created_on=account["created_on"],
        )

    def __get_list(self):
        if self.__list is not None:
            return self.__list
        else:
            return self.list()

    def list(
        self, page: int = 1, per_page: int = 20, order: str = ""
    ) -> List[AccountData]:
        if order and (order != "asc" and order != "desc"):
            raise CFError("Invalid order parameter. Only 'asc' or 'desc' allowed.")
        params = {"page": page, "per_page": per_page, "order": order}
        data = self.request.get(params=params)
        self.__list = [self.__get_object(account) for account in data]
        return self.__list

    def get_id(self) -> str:
        if "id" in self.props() and self.id is not None:
            return self.id
        alist = self.__get_list()
        if len(alist) == 1:
            self.id = alist[0].id
            return alist[0].id
        if len(alist) > 1:
            print("Please use one of the account id as parameter in Cloudflare class")
            print("Accounts: ")
            for account in self.list():
                print("   ", account.name, ":", account.id)
            exit()
        raise CFError("No account found")

    def details(self):
        data = self.request.get(self.id)
        # url = self.build_url(account_id)
        # account = self.request.get(url)
        # if minimal and "legacy_flags" in account.keys():
        #     del account["legacy_flags"]
        # return account

    # This method is not accessable due to default token permissions
    def rename(self, account_id: str, name: str):
        url = self.build_url(account_id)
        account = self.request.put(url, json=dict(name=name))
        return account
