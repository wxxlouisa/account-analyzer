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
"""Gets the list of users with access to the account of the given MCC and login customer ID.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from src.base_func_module import BaseFuncModule

class GetUsersModule():

    def __init__(self, client, customer_id):
        self.google_ads_client = client
        self.login_customer_id = customer_id
        self.base_func_obj = BaseFuncModule()

    def main(self):
        googleads_service = self.google_ads_client.get_service("GoogleAdsService")
        customer_service = self.google_ads_client.get_service("CustomerService")
        query = f"""
        SELECT
        customer_user_access.user_id,
        customer_user_access.email_address,
        customer_user_access.access_role,
        customer_user_access.access_creation_date_time,
        customer_user_access.inviter_user_email_address
        FROM customer_user_access
        """
        search_request = self.google_ads_client.get_type("SearchGoogleAdsRequest")
        search_request.customer_id = str(self.login_customer_id)
        search_request.query = query
        response = googleads_service.search(request=search_request)

        for customer_user_access in response:
            user_access = customer_user_access.customer_user_access
            print(
                "Customer user access with "
                f"User ID = '{user_access.user_id}', "
                f"Access Role = '{user_access.access_role}', and "
                f"Creation Time = {user_access.access_creation_date_time} "
                f"was found in Customer ID: {self.login_customer_id}."
            )
