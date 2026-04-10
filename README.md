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

## Extra 
