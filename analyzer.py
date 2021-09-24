#!/usr/bin/env python
# Copyright 2021 Google LLC
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
"""Gets the account infomation of the given MCC and login customer.

"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from src.base_func_module import BaseFuncModule
from src.account_hierarchy_module import AccountHierarchyModule
from src.get_users_module import GetUsersModule

def fetch_login_customer_id(google_ads_client, customer_id) -> str:
    if customer_id is not None:
        return customer_id
    else:
        print(
                "No manager ID is specified. The example will print the "
                "hierarchies of all accessible customer IDs."
            )
        customer_service = google_ads_client.get_service("CustomerService")

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
                return customer.id
            except GoogleAdsException as ex:
                continue

if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    parser = argparse.ArgumentParser(
        description="This analyzer will display the account info "
        "according to the input."
    )
    # process argument(s)
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=False,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-v",
        "--google_ads_version",
        type=str,
        required=False,
        help="Optional version. If none provided, the default value will be v8 "
    )
    parser.add_argument(
        "-vv",
        "--print_details",
        type=str,
        required=False,
        help="Print in detail. If none provided, the default value will be True."
    )
    args = parser.parse_args()

    required_version = args.google_ads_version
    if required_version == None:
        required_version = "v8"

    base_func_obj = BaseFuncModule(args.print_details)

    try:
        googleads_client = GoogleAdsClient.load_from_storage(version=args.google_ads_version)
    except GoogleAdsException as ex:
        base_func_obj.print_ex(ex)
        sys.exit(1)

    login_customer_id = fetch_login_customer_id(googleads_client, args.customer_id)

    try:
        hierarchy_obj = AccountHierarchyModule(googleads_client, login_customer_id)
        hierarchy_obj.main()
        print()
    except GoogleAdsException as ex:
#        base_func_obj.print_ex(ex)
        pass

    try:
        users_obj = GetUsersModule(googleads_client, login_customer_id)
        users_obj.main()
        print()
    except GoogleAdsException as ex:
        base_func_obj.print_ex(ex)
        pass
