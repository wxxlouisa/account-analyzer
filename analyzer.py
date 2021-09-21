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

from base_func_module import BaseFuncModule
from account_hierarchy_module import AccountHierarchyModule
from get_users_module import GetUsersModule


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
        required=True,
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
        "--print_exception_details",
        type=str,
        required=False,
        help="Print exception in detail. If none provided, the default value will be false "
    )
    args = parser.parse_args()

    required_version = args.google_ads_version
    if required_version == None:
        required_version = "v8"
    base_func_obj = BaseFuncModule(args.print_exception_details)

    try:
        googleads_client = GoogleAdsClient.load_from_storage(version=args.google_ads_version)
    except GoogleAdsException as ex:
        base_func_obj.print_ex(ex)
        sys.exit(1)

    try:
        hierarchy_obj = AccountHierarchyModule(googleads_client, args.customer_id)
        hierarchy_obj.main()
    except GoogleAdsException as ex:
        base_func_obj.print_ex(ex)

    try:
        users_obj = GetUsersModule(googleads_client, args.customer_id)
        users_obj.main()
    except GoogleAdsException as ex:
        base_func_obj.print_ex(ex)
