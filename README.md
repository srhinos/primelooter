# Primelooter

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/srhinos/primelooter?label=version)
[![Python](https://img.shields.io/badge/Made%20with-Python%203.9-blue.svg?style=flat-square&logo=Python&logoColor=white)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/srhinos/primelooter)](https://github.com/srhinos/primelooter/blob/main/LICENSE)

Python bot which automatically claims ~~twitch~~ amazon prime gaming loot :D

## Usage

### 1. ⚙️ General Setup
<details>
  <summary><b>Local 📌</b></summary>

  1.  Install python3
  2.  Install package requirements: `pip install -r requirements.txt`
  3.  Install playwright: `python -m playwright install`
  4.  Create your own cookies.txt and publishers.txt (see example files)`
</details>

<details>
  <summary><b>Docker 🐳</b></summary>

  If you want to use the provided docker image (only linux/amd64 plattform for now) you must mount the **config.txt** and **providers.txt** into the **app** path. (example compose file is provided)
</details>

### 2. 🍪 Generate a cookie.txt

1.  Install this addon: [cookie.txt](https://addons.mozilla.org/de/firefox/addon/cookies-txt/) (Firefox) / [cookie.txt](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc/) (Chrome)
2.  Goto: [https://gaming.amazon.com](https://gaming.amazon.com)
3.  Login with your credentials
4.  There should be a new add-on icon in the right corner. Click on it and Export Cookies->Current Site

(Be careful not to share your cookie.txt! Keep it a secret like your credentials)

### 3. 🏢 Create a publishers.txt

Create a publishers.txt like the example file. Each line represents the publisher name used on the [https://gaming.amazon.com](https://gaming.amazon.com) website (add 'all' to claim all offers).

### 4. 🏃 Run

The script offers multiple arguments:
```bash
-p PUBLISHERS, --publishers PUBLISHERS
                      Path to publishers.txt file

-c COOKIES, --cookies COOKIES
                      Path to cookies.txt file

-l, --loop            Shall the script loop itself? (Cooldown 24h)
--dump                Dump html to output
-d, --debug           Print Log at debug level
-nh, --no-headless    Shall the script not use headless mode?
```
If you use docker simply start the container.

If you want to use cron.d instead of letting the script wait 24h you must create a new file under `/etc/cron.d`.

Example:
```
0 0 * * * root : Primelooter ; /usr/bin/python3 /path/to/primelooter.py --cookie /path/to/cookie.txt --publishers /path/to/publishers.txt
```


## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for more information on contributing to this project!

## Disclaimer

Use this bot at your own risk! For more information read the [license](LICENSE) file.
