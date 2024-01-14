# f2pool_telegram_bot

**Simple but effective interface between f2pool and telegram bot**

## How to use it:

1. Clone or download the folder.
2. Add file `secret.py` in the root directory and insert the following variables:
   - `token` the telegram bot token.
   - `f2pool_api_key` the f2pool API key.

Example:

```
token = "123456789:ABCDEFG1234567"
f2pool_api_key = "yr4nmtqfs4wemeiz"
```
3. Run `main.py`.

4. The script checks if the `whitelist` and `error_log` files exist, otherwise, it will create them.

5. Insert the `CHAT_ID` of the users you want to allow to use the bot in `whitelist.txt`, one per line.

Contact me for any questions
