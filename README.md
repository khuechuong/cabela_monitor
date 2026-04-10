# cabela_monitor
This is a "stealth" web scraper designed to bypass Akamai bot detection. It monitors Cabela’s used gun inventory for specific deals (e.g., Glocks under $400) and provides a real-time terminal readout. When a new item is added or removed, the script triggers a physical audio alert through your computer's speakers.

## Environment
Only tested on Ubuntu 22.04

## Installation

```
sudo apt update
sudo apt install chromium-browser chromium-chromedriver
pip install undetected-chromedriver
```

## Testing

### Verify Autdio
```
paplay /usr/share/sounds/freedesktop/stereo/complete.oga
```

## Run
```
python3 cabela_monitor.py
```

## Customizing Your Search 
To change what the script looks for, go to Line 38 in [cabela_monitor.py](https://github.com/khuechuong/cabela_monitor/blob/main/cabela_monitor.py):

```
url = "https://www.cabelas.com/l/used-guns#sortCriteria=%40offerprice%20ascending&f-cartridge_or_gauge=9mm%20Luger,9mm%20Parabellum,9mm&f-brand=Glock&nf-offerpricefilter=100...400"
```
How to get the perfect URL:

- Open your browser and go to Cabelas.com Used Guns.

- Select your filters (e.g., Brand, Price, Caliber).

- Copy the full URL from the address bar and paste it into the script.
