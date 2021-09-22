# account-analyzer

This is an Account Analyzer tool based on google-ads-python.

------------
Requirements
------------
* Python 3.7+

Documentation
------------
To get a quick start, you're suggested to follow the [Google Ads API Quickstart][2] to prepare the correct Developer token as well as other secrets, using a ```google-ads.yaml``` to config them.

Remember that you may need to refresh your token periodically. You can run the ``` authenticate_in_desktop_application.py``` to make it, for example:
```bash
python authenticate_in_desktop_application.py --client_secrets_path=$HOME/secrets.json
```

Authors
-------
* [Xuanxuan Wang][1]

[0]: https://docs.google.com/document/d/10Di-4ylMyJKYzONzsS_Vy3woxHnF0w3Pmm6Seu0mKf4/edit?usp=sharing
[1]: https://github.com/wxxlouisa
[2]: https://developers.google.com/google-ads/api/docs/start
