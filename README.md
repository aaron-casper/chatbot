all three scripts depend on python3.8 and chattmarkov.

I find it best to spin up a venv with py3.8 and grab the needed modules there.
example:
`
python3.8 -m venv ./chatbot
cd chatbot
source ./bin/activate
pip install chattymarkov
pip install discord.py`

every script requires brain.json for the markov chain generator.  if it does not exist, it will create it.

A new/blank brain is boring.  Included is speedloader.py

To use speedloader.py, fill ./corpus.txt with example sentences you want your markov bot to "learn".  Then run speedloader.py and restart your bot.
Congratulations, you now have a "smarter" bot.
