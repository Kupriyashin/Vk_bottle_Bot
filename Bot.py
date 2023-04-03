import asyncio
import math
import os
import random
import config
from vkbottle import GroupEventType, GroupTypes
from vkbottle import API
from loguru import logger
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, VKPay

logger.add('debug.log', format="{time},{level},{message}", level='INFO')

bot = Bot(token=config.token_group)
user = API(token=config.token_user)


@logger.catch()
async def random_moew_sentence() -> str:
    try:

        _words = ['мяу'] * random.randint(3, 10)
        logger.info(_words)

        _words[-1] = _words[-1] + str(random.choice(['.', '!', '?', '...']))

        for _ in range(0, len(_words) - 1):

            if random.random() < 0.01:
                _words[_] = _words[_] + str(random.choice(['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']))

            if random.random() < 0.1:
                _words[_] = _words[_] + str(random.choice([',', ':', ' -', '']))

        _sentence = ' '.join(_words)
        _sentence = _sentence.capitalize()
        logger.info(f'Сформированное сообщение random_moew_sentence: {_sentence}')

        return str(_sentence)

    except Exception as process_file_err:
        logger.error(f'Произошла ошибка в преобразовании предложения в meow: {process_file_err}')


@logger.catch()
async def sentence() -> str:
    try:
        _outsectence = []
        if random.random() > 0.5:
            _outsectence.append(await random_moew_sentence())
        elif random.random() < 0.01:
            for a in range(6):
                _outsectence.append(await random_moew_sentence() + ' ')
        elif random.random() < 0.1:
            for b in range(5):
                _outsectence.append(await random_moew_sentence() + ' ')
        elif random.random() < 0.2:
            for c in range(4):
                _outsectence.append(await random_moew_sentence() + ' ')
        elif random.random() < 0.3:
            for d in range(3):
                _outsectence.append(await random_moew_sentence() + ' ')
        elif random.random() < 0.4:
            for f in range(2):
                _outsectence.append(await random_moew_sentence() + ' ')
        elif random.random() < 0.5:
            for g in range(1):
                _outsectence.append(await random_moew_sentence() + ' ')

        _output = ''.join(_outsectence)
        logger.info(f'Сформированное сообщение sentence: {_output}')
        await asyncio.sleep(0.2)

        return _output

    except Exception as err_sentence:
        logger.error(err_sentence)
        return 'Мяу мяу мяу мяу, мяу мяу мяу мяу мяу?'


@logger.catch()
async def ran_art() -> dict:
    try:
        from icrawler.builtin import BingImageCrawler
        import random

        _bing_crawler = BingImageCrawler(
            downloader_threads=4,
            storage={'root_dir': 'Image'}
        )

        _names_cat = (random.choice(open("../popular cat breeds.txt").readlines())).split('\n')[0]
        _fraza_poisk = str(f"{_names_cat} cats photography").replace(' ', '%20')

        _filters = {
            'type': 'photo',
            'color': random.choice(
                ['color', 'white',
                 'gray', 'brown']),
            'size': '>1920x1080',
            'layout': 'wide'
        }

        _bing_crawler.crawl(keyword=_fraza_poisk,
                            filters=_filters,
                            offset=random.randint(0, 3),
                            min_size=(1920, 1080),
                            max_num=50)

        _urls_image = {}
        with open('file_url.txt', 'r', encoding='UTF-8') as urls:
            for line in urls:
                (key, val) = str(line).split('->')
                _urls_image[int(key)] = str(val)[:-1]

        os.remove('file_url.txt')
        _urls_image = random.choice(list(_urls_image.items()))

        _files = os.listdir('../Image')

        for file in _files:
            if str(_urls_image[0]) not in file:
                os.remove(f"Image/{file}")

        logger.info(f"Ссылка на выходное изображение: {_urls_image[-1]}\nНазвание файла: {os.listdir('../Image')[0]}")

        return {'url_image': f"{_urls_image[-1]}", 'name_image': f"{os.listdir('../Image')[0]}"}

    except Exception as err_poluchenie_photo:
        logger.error(f"При поиске фото получил ошибку: {err_poluchenie_photo}")
        return {'url_image': f"https://vk.com/kupriyashinnick", 'name_image': f"Image_error/Error_Image.jpg"}


@logger.catch()
@bot.on.raw_event(GroupEventType.WALL_REPLY_NEW, dataclass=GroupTypes.WallReplyNew)
async def comments_new_wall(event: GroupTypes.WallReplyNew):
    try:
        logger.info(f'Пришел ивент комментарии: {event.object}')
        if event.object.from_id > 0:

            responce = 'Ответа нет'

            _owner_id = event.object.owner_id
            _post_id = event.object.post_id
            _from_group = True
            _reply_to_comment = event.object.id

            _user_info = await bot.api.users.get(user_ids=[event.object.from_id])
            _user_info = _user_info[0].first_name if _user_info else ''

            _message = await sentence()
            _message = f"@id{event.object.from_id}({_user_info}), {_message}"
            logger.info(f"Сформированная строка для имени юзера и ответ: {_message}")

            _vibor_otpravri = random.random()
            logger.info(f"Рандомное число для выбора действия: {_vibor_otpravri}")

            if _vibor_otpravri > 0.5:
                logger.info(f'Смформировано сообщение для ответа в комментарии: {_message}')

                responce = await bot.api.wall.create_comment(owner_id=_owner_id, post_id=_post_id,
                                                             from_group=_from_group,
                                                             reply_to_comment=_reply_to_comment, message=_message)
            elif _vibor_otpravri < 0.3:
                _fotos = await user.photos.get(
                    owner_id=-219553631,
                    album_id='wall',
                    count=200
                )
                logger.info('Получил список фотографий со страницы в размере 200 штук')

                _arr_id_fotos = []
                for item in _fotos.items:
                    _arr_id_fotos.append(item.id)
                    logger.info('Обработка фотографий')

                responce = await bot.api.wall.create_comment(owner_id=_owner_id, post_id=_post_id,
                                                             from_group=_from_group,
                                                             reply_to_comment=_reply_to_comment, message=_message,
                                                             attachments=[
                                                                 f"photo{_fotos.items[0].owner_id}_{random.choice(_arr_id_fotos)}"])
                logger.info(f"Отправил сообщение вместе с картинкой")

            elif _vibor_otpravri < 0.5:
                _stiker_id = ''

                with open('stikers_id.txt', 'r', encoding='UTF-8') as file_ids:
                    _stiker_id = random.choice(file_ids.readlines())
                    logger.info(f'Получаю рандомный айди стикера: {_stiker_id}')
                logger.info(f"Полученный ади стикера для отправки в комментарии: {_stiker_id}")

                responce = await bot.api.wall.create_comment(owner_id=_owner_id, post_id=_post_id,
                                                             from_group=_from_group,
                                                             reply_to_comment=_reply_to_comment,
                                                             sticker_id=int(_stiker_id))

            logger.info(f'Пришел ответ от метода отправки комментария: {responce}')

    except Exception as comment_error:
        logger.error(comment_error)


# @logger.catch()
# @bot.on.private_message(StickerRule())
# async def privet_ls_stikers(message: Message):
#     try:
#         _stiker_id = ''
#
#         with open('stikers_id.txt', 'r', encoding='UTF-8') as file_ids:
#             _stiker_id = random.choice(file_ids.readlines())
#             logger.info(f'Получаю рандомный айди стикера: {_stiker_id}')
#
#         await message.answer(sticker_id=int(_stiker_id))
#         logger.info(f'Отправил сообщение с рандомных стикером')
#     except Exception as error_stikers:
#         logger.error(error_stikers)

@logger.catch()
@bot.on.private_message(text='Дай котика')
async def kotik_v_ls(message: Message):
    try:
        _keybord = Keyboard(inline=True)
        _keybord.add(Text('Дай котика'), color=KeyboardButtonColor.POSITIVE)

        _keybord_vkpay = Keyboard(inline=True)
        _keybord_vkpay.add(Text('Дай котика'), color=KeyboardButtonColor.POSITIVE)
        _keybord_vkpay.row()
        _keybord_vkpay.add(Text('Донатик ниже👇'), color=KeyboardButtonColor.NEGATIVE)
        _keybord_vkpay.row()
        _keybord_vkpay.add(VKPay(hash=f"action=transfer-to-group&group_id={219553631}&aid=10"))

        logger.info('Создал клавиатуру при отправке рандомного кота')

        _fotos = await user.photos.get(
            owner_id=-219553631,
            album_id='wall',
            count=200
        )
        logger.info('Получил список фотографий со страницы в размере 200 штук')

        _arr_id_fotos = []
        for item in _fotos.items:
            _arr_id_fotos.append(item.id)
            logger.info('Обработка фотографий')

        responce = await message.answer(attachment=[
            f"photo{_fotos.items[0].owner_id}_{random.choice(_arr_id_fotos)}"],
            keyboard=_keybord_vkpay if random.random() < 0.1 else _keybord)

        logger.info(f"Отправил сообщение вместе с картинкой, его лог: {responce}")

    except Exception as error_kotik_ls:
        logger.error(f"Произошла ошибка при отправки котика в лс: {error_kotik_ls}")


@logger.catch()
@bot.on.private_message(text=['начать', 'Привет', 'привет', 'Начать', 'как дела?', 'Как дела?', 'Как дела', 'как дела'])
async def otvet_privet(message: Message):
    try:
        _keybord = Keyboard(inline=True)
        _keybord.add(Text('Дай котика'), color=KeyboardButtonColor.POSITIVE)
        _keybord.row()
        _keybord.add(VKPay(hash=f"action=transfer-to-group&group_id={219553631}&aid=10"))

        await message.answer("Привет дорогой друг!\n"
                             "Я бот данной группы, отвечаю за создание постов, ответ на комментарии и могу поговорить в личных сообщениях🦹‍♀️\n"
                             "\n"
                             "Мои доступные функции:\n"
                             "0⃣ Я полностью веду данную группу, начиная от поиска картинок, заканчивая созданием постов\n"
                             "1⃣ Могу поддерживать живое общение в комментариях и в личных сообщениях\n"
                             "2⃣ Скидываю рандомную картинку, если ты напишешь - Дай котика👇\n"
                             "\n"
                             "Если хочешь можешь меня немного поддержать денюжкой💳", keyboard=_keybord)
    except Exception as ot_pr:
        logger.error(f'Произошла ошибка в функции otvet_privet: {ot_pr}')


# @logger.catch()
# @bot.on.private_message(AttachmentTypeRule(
#     attachment_types=["photo", "audio", "video", "doc", "link", "market", "market_album", "gift", "wall",
#                       "wall_reply", "article", "poll", "call", "graffiti", "audio_message", "story",
#                       "group_call_in_progress",
#                       "mini_app"]))  # Если кидается сообщение в котором есть какой-то аттачмнет (фото, видео, файл и т.д.)
# @bot.on.private_message(text='Дай котика')  # Если написано сообщение Дай котика
# async def give_me_kotic(message: Message):
#     try:
#         _keybord = Keyboard(inline=True)
#         _keybord.add(Text('Дай котика'), color=KeyboardButtonColor.POSITIVE)
#
#         _keybord_vkpay = Keyboard(inline=True)
#         _keybord_vkpay.add(Text('Дай котика'), color=KeyboardButtonColor.POSITIVE)
#         _keybord_vkpay.row()
#         _keybord_vkpay.add(Text('Донатик ниже👇'), color=KeyboardButtonColor.NEGATIVE)
#         _keybord_vkpay.row()
#         _keybord_vkpay.add(VKPay(hash=f"action=transfer-to-group&group_id={219553631}&aid=10"))
#
#         logger.info('Создал клавиатуру при отправке рандомного кота')
#
#         _fotos = await user.photos.get(
#             owner_id=-219553631,
#             album_id='wall',
#             count=200
#         )
#         logger.info('Получил список фотографий со страницы в размере 50 штук')
#
#         _arr_id_fotos = []
#         for item in _fotos.items:
#             _arr_id_fotos.append(item.id)
#             logger.info('Обработка фотографий')
#
#         import random
#         await message.answer('Держи котика😺', keyboard=_keybord_vkpay if random.random() < 0.1 else _keybord,
#                              attachment=f"photo{_fotos.items[0].owner_id}_{random.choice(_arr_id_fotos)}")
#         logger.info('Отправил рандомную фотографию')
#         del _fotos
#
#     except Exception as give_cat:
#         logger.error(f"Произошла ошибка в функции give_me_kotic: {give_cat}")


@logger.catch()
@bot.on.private_message(text='Донатик ниже👇')
async def donatic(message: Message):
    try:
        _keybord = Keyboard(inline=True)
        _keybord.add(Text('Дай котика'), color=KeyboardButtonColor.POSITIVE)

        _keybord = Keyboard(inline=True)
        _keybord.add(Text('Дай котика'), color=KeyboardButtonColor.POSITIVE)
        _keybord.row()
        _keybord.add(Text('Донатик ниже👇'), color=KeyboardButtonColor.NEGATIVE)
        _keybord.row()
        _keybord.add(VKPay(hash=f"action=transfer-to-group&group_id={219553631}&aid=10"))

        await message.answer('Я считаю это правильный выбор😼', keyboard=_keybord,
                             attachment=f"photo-219553631_457239167")
        logger.info('отправил фотку для доната')
    except Exception as donat_err:
        logger.error(f"Произошла ошибка при нажатии на кнопку 'Донатик ниже👇': {donat_err} ")


@logger.catch()
@bot.loop_wrapper.interval(hours=4)
async def post():
    try:
        from vkbottle import PhotoWallUploader
        _image_uploader = PhotoWallUploader(user)

        _image = await ran_art()
        logger.info(f"Получил _image для загрузки фотографии: {_image}")

        # random.choice(['292373196', '292373202', '292373213', '292373219', '292373225'])
        _attachment = await _image_uploader.upload(file_source=f"Image/{_image['name_image']}")
        logger.info(f"Получил _attachment для загрузки фотографии: {_attachment}")

        _message = await sentence()

        await user.wall.post(owner_id=-219553631, from_group=True, attachments=_attachment,
                             copyright=_image['url_image'], message=_message)
        logger.info('Я отправил пост на страницу группы')

        _files = os.listdir('../Image')
        for file in _files:
            os.remove(f"Image/{file}")
            logger.info(f"Очищаю папку с фотографиями")

        _files = os.listdir(os.path.abspath(os.curdir))
        logger.info(_files)

        for file in _files:
            if 'file_url' in file:
                os.remove('file_url.txt')
                logger.info('Удаляю файл с данными о картинках')

    except Exception as upload_err:
        logger.error(f"Возникла ошибка при публикации записи на стене сообщества: {upload_err}")


@logger.catch()
@bot.loop_wrapper.interval(days=1)
async def happy_birthday():
    try:
        from datetime import datetime
        _friends_happy_birthday = []
        _friends_count = await user.friends.get()
        _friends_count = _friends_count.count

        _friends_count_items = []
        for _ in range(math.ceil(int(_friends_count) / 100)):

            _item = await user.friends.get(order='name', offset=_ * 100, count=100, fields=['bdate'])
            logger.info(f'Получил 100 пользователей из друзей: {_item.items}\n')

            for _1 in _item.items:
                _friends_count_items.append(_1)
                logger.info(f"Добавляю в _friends_count_items элемент: {_1}")

        for _user in _friends_count_items:
            logger.info(
                f"\nИнформация о пользователе: {_user.first_name} {_user.last_name} https://vk.com/id{_user.id},\n"
                f"Дата рождения: {_user.bdate}, тип даты рождения {type(_user.bdate)}\n")
            try:
                if (int(_user.bdate.split('.')[0]) == datetime.now().day) and (
                        int(_user.bdate.split('.')[1]) == datetime.now().month):
                    _friends_happy_birthday.append(_user)
                    logger.info(
                        f"Сегодня день рождения у пользователя: {_user.first_name} {_user.last_name} https://vk.com/id{_user.id}")
            except Exception as bdate_error:
                logger.info(f"Ошибка при определении даты рождения: {bdate_error}")

        for _ in _friends_happy_birthday:
            logger.info(
                f"Сегодня празднует свой день рождения следующие пользователи: {_.first_name} {_.last_name} https://vk.com/id{_.id}")

            await user.messages.send(user_ids=[int(_.id)], random_id=random.randint(-2147483648, 2147483647),
                                     message=f"Добрейшего времени суток! 🌍\n"
                                             f"Поздравляю с днем рождения и желаю всего самого наилучшего!")

    except Exception as happy_error:
        logger.error(f"Произошла ошибка в поздравлении с днем рождения: {happy_error}")


@logger.catch()
@bot.on.private_message()
async def otvet_v_ls(message: Message):
    try:
        responce = 'Ответа нет'
        _message = await sentence()

        _vibor_otpravri = random.random()
        logger.info(f"Рандомное число для выбора действия: {_vibor_otpravri}")

        if (_vibor_otpravri < 1) and (_vibor_otpravri > 0.4):
            logger.info(f'Смформировано сообщение для ответа в лс: {_message}')

            responce = await message.answer(_message)

        elif _vibor_otpravri < 0.1:

            _keybord = Keyboard(inline=True)
            _keybord.add(Text('Дай котика'), color=KeyboardButtonColor.POSITIVE)

            _keybord_vkpay = Keyboard(inline=True)
            _keybord_vkpay.add(Text('Дай котика'), color=KeyboardButtonColor.POSITIVE)
            _keybord_vkpay.row()
            _keybord_vkpay.add(Text('Донатик ниже👇'), color=KeyboardButtonColor.NEGATIVE)
            _keybord_vkpay.row()
            _keybord_vkpay.add(VKPay(hash=f"action=transfer-to-group&group_id={219553631}&aid=10"))

            logger.info('Создал клавиатуру при отправке рандомного кота')

            _fotos = await user.photos.get(
                owner_id=-219553631,
                album_id='wall',
                count=200
            )
            logger.info('Получил список фотографий со страницы в размере 200 штук')

            _arr_id_fotos = []
            for item in _fotos.items:
                _arr_id_fotos.append(item.id)
                logger.info('Обработка фотографий')

            responce = await message.answer(message=_message, attachment=[
                f"photo{_fotos.items[0].owner_id}_{random.choice(_arr_id_fotos)}"],
                                            keyboard=_keybord_vkpay if random.random() < 0.1 else _keybord)

            logger.info(f"Отправил сообщение вместе с картинкой")

        elif (_vibor_otpravri > 0.1) and (_vibor_otpravri < 0.4):
            _stiker_id = ''

            with open('stikers_id.txt', 'r', encoding='UTF-8') as file_ids:
                _stiker_id = random.choice(file_ids.readlines())
                logger.info(f'Получаю рандомный айди стикера: {_stiker_id}')
            logger.info(f"Полученный ади стикера для отправки в комментарии: {_stiker_id}")

            responce = await message.answer(sticker_id=int(_stiker_id))

        logger.info(f'Пришел ответ от метода отправки комментария: {responce}')

    except Exception as otvet_ls_err:
        await message.answer(
            message='Мяу мяу мяу мяу мяу - мяу мяу мяу мяу мяу? Мяу мяу мяу мяу мяу мяу? Мяу мяу мяу мяу мяу мяу!')
        logger.error(f"Возникла ошибка при ответе в лс группы: {otvet_ls_err}")
        logger.catch()


if __name__ == '__main__':
    bot.run_forever()
