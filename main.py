from vkbottle.user import User , Message
import vk_api
import os
import json
from tokens import main , otvets
bot = User(token=main["token"])
@bot.on.private_message()
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    for otvet in otvets:
        if message.text.lower() == otvet:
            if "Sticker" in otvets[otvet]:
                id = otvets[otvet].split()
                await message.answer(sticker_id=id[1])
            else:
                await message.answer(otvets[otvet])
bot.run_forever()








