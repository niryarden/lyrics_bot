<p align="center">
    <img src="https://github.com/niryarden/lyrics_bot/blob/master/static/bot-logo.jpg" alt="lyrics_bot logo" width="100" height="100">
</p>

<h1 align="center">lyrics_bot</h1>
<p align="center">
    A Telegram bot made for sending you lyrics and meaning of songs you listen to. 
</p>

### Abilities
The lyrics_bot meant to be run on a windows computer which has an active iTunes app installed.
When asked, the bot can access your iTunes app, extract the current played song, search for its lyrics or meaning online, and send in back to you in the telegram chat. ***No need to search your favorite songs manually - the bot will do it for you.***


### Usage
Clone the repository and install the requirements
```bash
git clone https://github.com/niryarden/lyrics_bot.git
cd lyrics_bot
pip install -r requirements.txt
```

Create a 'token.cfg' with that structure:
```editorconfig
[creds]
token = <Your_Telegram_Token>
```

Run the app using your chat_id
```bash
python app.py <Your_Chat_ID>
```

And if everything went well, you've got a wake up Telegram message from the bot.
type ```/hello``` and send to get full details about possible commands.
