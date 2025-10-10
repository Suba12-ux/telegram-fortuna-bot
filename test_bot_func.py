from app import main

def test_tocen():
	print(main.BOT_TOKEN)
	assert type(main.BOT_TOKEN) == str