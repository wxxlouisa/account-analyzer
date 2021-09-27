# account-analyzer

This is an Account Analyzer tool based on google-ads-python.


Requirements
------------
* Python 3.7+

Documentation
------------
### step 1

Firstly copy the ```account-analyzer/account-analyzer-demo.yaml```  into your home directory and rename it:
```bash
cp account-analyzer-demo.yaml $HOME/account-analyzer-demo.yaml
```
To get a quick start, you're suggested to follow the [Google Ads API Quickstart][2] to prepare the correct Developer token as well as other secrets, using your ```google-ads.yaml``` to config them. Make sure every insertion is ready.


### step 2
If you've successfully get a secerts.json from step 1, you can go ahead. Otherwise please download it from https://console.developers.google.com/apis/credentials.

Remember that you may need to refresh your token periodically. You can run the ``` authenticate_in_desktop_application.py``` to make it, for example:
```bash
python authenticate_in_desktop_application.py --client_secrets_path=$HOME/secrets.json
```
Then insert the generated refresh token into your ```$HOME/google-ads.yaml```

### Run this demo
Now you can run this demo by directly compiling:
```bash
python analyzer.py
```
There're more unrequired arguments for you to specify your request:

* -c --customer_id  specify the manager account you want to see, otherwise it will display all the accessible customer on your OAuth credentials.
```bash
python analyzer.py -c 1234567890
```
* -v --google_ads_version   default="v8", specify the google-ads version.
```bash
python analyzer.py -v "v8"
```

* -vv --print_details   If none provided, the default value will be True. 
```bash
python analyzer.py -vv False
```


Authors
-------
* [Xuanxuan Wang][1]

[0]: https://docs.google.com/document/d/10Di-4ylMyJKYzONzsS_Vy3woxHnF0w3Pmm6Seu0mKf4/edit?usp=sharing
[1]: https://github.com/wxxlouisa
[2]: https://developers.google.com/google-ads/api/docs/start
