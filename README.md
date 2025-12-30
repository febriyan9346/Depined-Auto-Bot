# Depined Auto Bot

🔗 **Website:** [https://app.depined.org/onboarding](https://app.depined.org/onboarding)

🎁 **Referral Code:** `DEwtQqL7nGMKIv`

---

## 📋 Description

Depined Auto Bot is an automated bot designed to manage multiple Depined accounts efficiently. This bot handles login, widget connections, and point tracking across multiple accounts with support for proxy rotation and Cloudflare Turnstile captcha solving.

## ✨ Features

- 🔐 **Multi-Account Support** - Manage unlimited accounts simultaneously
- 🌐 **Proxy Support** - Optional proxy rotation for enhanced privacy
- 🤖 **Auto Captcha Solving** - Automatic Cloudflare Turnstile bypass using 2Captcha
- 📊 **Real-Time Statistics** - Track points balance and daily earnings
- 🔄 **Auto Widget Connect** - Automatic widget connection for point accumulation
- ⏰ **Configurable Cycles** - Runs continuously with customizable intervals
- 🎨 **Colorful Console Output** - Easy-to-read colored logs with timestamps

## 📦 Requirements

- Python 3.7 or higher
- 2Captcha API Key ([Get it here](https://2captcha.com/?from=16945738))
- Active Depined account(s)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/febriyan9346/Depined-Auto-Bot.git
cd Depined-Auto-Bot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Create `2captcha.txt`
Add your 2Captcha API key (one per line):
```
your_2captcha_api_key_here
```

### 2. Create `accounts.txt`
Add your Depined accounts in the format `email:password` (one per line):
```
email1@example.com:password1
email2@example.com:password2
email3@example.com:password3
```

### 3. Create `proxy.txt` (Optional)
Add your proxies if you want to use proxy mode (one per line):
```
http://user:pass@ip:port
http://user:pass@ip:port
socks5://user:pass@ip:port
```

Supported proxy formats:
- `http://ip:port`
- `http://user:pass@ip:port`
- `https://ip:port`
- `socks5://ip:port`

## 🚀 Usage

Run the bot:
```bash
python bot.py
```

You will be presented with two options:
1. **Run with proxy** - Uses proxies from `proxy.txt`
2. **Run without proxy** - Direct connection

The bot will:
- Login to each account
- Connect the widget
- Fetch and display profile information
- Show points balance and daily earnings
- Display epoch earnings
- Repeat the cycle every 5 minutes

## 📊 Output Example

```
[12:34:56] [INFO] API Key loaded
[12:34:56] [SUCCESS] Loaded 5 accounts successfully
[12:34:56] [SUCCESS] Loaded 10 proxies
[12:34:56] [CYCLE] Cycle #1 Started
[12:34:57] [INFO] Account #1/5
[12:34:57] [INFO] Proxy: http://proxy1.example.com:8080
[12:34:57] [INFO] ema***@example.com
[12:35:00] [INFO] Solving Cloudflare Turnstile captcha...
[12:35:15] [SUCCESS] Captcha solved successfully!
[12:35:16] [SUCCESS] Login successful!
[12:35:17] [INFO] Processing Task:
[12:35:18] [SUCCESS] Widget connected successfully!
[12:35:20] [SUCCESS] User: username123
[12:35:20] [SUCCESS] Total Points: 1,234.56 | Today: +123
[12:35:21] [SUCCESS] Epoch 42: +15 points earned
```

## ⚠️ Important Notes

- Keep your `2captcha.txt` and `accounts.txt` files secure
- The bot uses random delays between requests to avoid detection
- Each cycle runs every 5 minutes (300 seconds)
- 2Captcha service costs apply for each captcha solved
- Make sure you have sufficient 2Captcha balance

## 🔧 Troubleshooting

### "2captcha.txt is empty or not found!"
- Ensure you have created the `2captcha.txt` file in the same directory as `bot.py`
- Add your 2Captcha API key to the file

### "accounts.txt is empty or not found!"
- Create the `accounts.txt` file with your account credentials
- Format: `email:password` (one per line)

### Login Failed
- Check your account credentials
- Verify your 2Captcha balance
- Check your internet connection or proxy settings

### Captcha Solving Timeout
- This usually means 2Captcha service is slow or your API key has issues
- Check your 2Captcha dashboard for balance and service status

## 📝 File Structure

```
Depined-Auto-Bot/
│
├── bot.py              # Main bot script
├── 2captcha.txt        # Your 2Captcha API key
├── accounts.txt        # Your Depined accounts
├── proxy.txt           # Your proxy list (optional)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 📦 Dependencies

- `requests` - HTTP library
- `colorama` - Colored terminal output
- `pytz` - Timezone handling

## ⚖️ Disclaimer

This bot is for educational purposes only. Use at your own risk. The author is not responsible for any consequences resulting from the use of this bot. Make sure to comply with Depined's terms of service.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/febriyan9346/Depined-Auto-Bot/issues).

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**FEBRIYAN**

- GitHub: [@febriyan9346](https://github.com/febriyan9346)

## ⭐ Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|---------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

---

⭐ **If you find this project helpful, please give it a star!** ⭐
