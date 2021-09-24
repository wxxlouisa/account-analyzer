#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Gets the account hierarchy of the given MCC and login customer ID.

If you don't specify manager ID and login customer ID, the example will instead
print the hierarchies of all accessible customer accounts for your
authenticated Google account. Note that if the list of accessible customers for
your authenticated Google account includes accounts within the same hierarchy,
this example will retrieve and print the overlapping portions of the hierarchy
for each accessible customer.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from src.base_func_module import BaseFuncModule

class AccountHierarchyModule():

    def __init__(self, client, customer_id = None):
        self.google_ads_client = client
        self.login_customer_id = customer_id
        self.base_func_obj = BaseFuncModule()

    def main(self):
        googleads_service = self.google_ads_client.get_service("GoogleAdsService")
        customer_service = self.google_ads_client.get_service("CustomerService")
        # A collection of customer IDs to handle.
        seed_customer_ids = []

        # Creates a query that retrieves all child accounts of the manager
        # specified in search calls below.
        query = """
            SELECT
            customer_client.client_customer,
            customer_client.level,
            customer_client.manager,
            customer_client.descriptive_name,
            customer_client.currency_code,
            customer_client.time_zone,
            customer_client.id
            FROM customer_client
            WHERE customer_client.level <= 1"""

        # If a Manager ID was provided in the customerId parameter, it will be
        # the only ID in the list. Otherwise, we will issue a request for all
        # customers accessible by this authenticated Google account.
        if self.login_customer_id is not None:
            seed_customer_ids = [self.login_customer_id]
        else:
            print(
                "No manager ID is specified. The example will print the "
                "hierarchies of all accessible customer IDs."
            )
            accessible_customers = customer_service.list_accessible_customers()
            result_total = len(accessible_customers.resource_names)
            print(f"Total results: {result_total}")
            customer_resource_names = accessible_customers.resource_names
            for resource_name in customer_resource_names:
                print(f'Customer resource name: "{resource_name}"')
            # [END list_accessible_customers]

            for customer_resource_name in customer_resource_names:
                try:
                    # must be set in the login_customer_id
                    customer = customer_service.get_customer(
                        resource_name=customer_resource_name
                    )
                    print("The customer ID is: ", customer.id)
                except GoogleAdsException as ex:
                    continue
                seed_customer_ids.append(customer.id)

        for seed_customer_id in seed_customer_ids:
            # Performs a breadth-first search to build a Dictionary that maps
            # managers to their child accounts (customerIdsToChildAccounts).
            unprocessed_customer_ids = [seed_customer_id]
            customer_ids_to_child_accounts = dict()
            root_customer_client = None

            while unprocessed_customer_ids:
                customer_id = int(unprocessed_customer_ids.pop(0))
                response = googleads_service.search(
                    customer_id=str(customer_id), query=query
                )

                # Iterates over all rows in all pages to get all customer
                # clients under the specified customer's hierarchy.
                for googleads_row in response:
                    customer_client = googleads_row.customer_client

                    # The customer client that with level 0 is the specified
                    # customer.
                    if customer_client.level == 0:
                        if root_customer_client is None:
                            root_customer_client = customer_client
                        continue

                    # For all level-1 (direct child) accounts that are a
                    # manager account, the above query will be run against them
                    # to create a Dictionary of managers mapped to their child
                    # accounts for printing the hierarchy afterwards.
                    if customer_id not in customer_ids_to_child_accounts:
                        customer_ids_to_child_accounts[customer_id] = []

                    customer_ids_to_child_accounts[customer_id].append(
                        customer_client
                    )

                    if customer_client.manager:
                        # A customer can be managed by multiple managers, so to
                        # prevent visiting the same customer many times, we
                        # need to check if it's already in the Dictionary.
                        if (
                            customer_client.id not in customer_ids_to_child_accounts
                            and customer_client.level == 1
                        ):
                            unprocessed_customer_ids.append(customer_client.id)

            if root_customer_client is not None:
                print()
                print(
                    "The hierarchy of customer ID "
                    f"{root_customer_client.id} is printed below:"
                )
                self._print_account_hierarchy(
                    root_customer_client, customer_ids_to_child_accounts, 0
                )
            else:
                print(
                    f"Customer ID {login_customer_id} is likely a test "
                    "account, so its customer client information cannot be "
                    "retrieved."
                )

    def _print_account_hierarchy(
            self, customer_client, customer_ids_to_child_accounts, depth
    ):
        """Prints the specified account's hierarchy using recursion.
        """
        if depth == 0:
            print("Customer ID (Descriptive Name, Currency Code, Time Zone)")
        customer_id = customer_client.id
        print("-" * (depth * 4), end="")
        print(
            f"{customer_id} ({customer_client.descriptive_name}, "
            f"{customer_client.currency_code}, "
            f"{customer_client.time_zone})"
        )
        # Recursively call this function for all child accounts of customer_client.
        if customer_id in customer_ids_to_child_accounts:
            for child_account in customer_ids_to_child_accounts[customer_id]:
                self._print_account_hierarchy(
                    child_account, customer_ids_to_child_accounts, depth + 1
                )
