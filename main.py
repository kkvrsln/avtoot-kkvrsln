import asyncio
import re
from telethon import TelegramClient, events
from telethon.events import Album

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
)

try:
    import qrcode
except ImportError:
    print("Библиотека qrcode не установлена.")
    print("Установите её командой: pip install qrcode[pil]")
    exit(1)

# ────────────────────────────────────────────────
#                НАСТРОЙКИ
# ────────────────────────────────────────────────

API_ID = 38870972
API_HASH = '05e908f1db256106d24985c1062fa440'

SESSION_NAME = 'qr_terminal_session'

FROM_CHANNELS = [
    '@remontrykami',
    -1001761455651,
    -1001127375190,
    'jsksmsmzklz',
    # -1003405358962,  # если нужно — добавь
]

TARGET_CHANNEL = '@muzhchannel'

FOOTER = "\n\n✦ [Мужской Канал](https://t.me/muzhchannel)"

ONLY_WITH_MEDIA = False

# ─── Фразы, по которым решаем копировать пост ──────────────────────────────
# Если хотя бы одна из фраз найдена в тексте → копируем
# Если список пустой → копируем всё (как раньше)
TRIGGER_PHRASES = [
    "Мужские Хитрости",
    "Ремонт своими руками",
    "Мудрый Строитель",
    # добавляйте свои фразы сюда
    # "девушки", "отношения", "деньги", и т.д.
]

# Если хотите копировать посты, в которых НЕТ этих фраз — поменяйте на True
INVERT_MATCH = False   # True = копировать, если НИ ОДНА фраза НЕ найдена

FORBIDDEN_PHRASES = [
    "Мужские Хитрости",
    "Ремонт своими руками",
    "Мудрый Строитель",
    "• мы в MAX 📲",
    # добавляйте свои
]

# ────────────────────────────────────────────────

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


def should_copy_post(text: str) -> bool:
    """Возвращает True, если пост нужно копировать по правилу триггеров"""
    if not TRIGGER_PHRASES:
        return True  # если триггеры не заданы — копируем всё

    text_lower = text.lower()

    found_any = any(
        phrase.lower() in text_lower
        for phrase in TRIGGER_PHRASES
    )

    if INVERT_MATCH:
        return not found_any
    else:
        return found_any


def clean_text(text: str) -> str:
    if not text:
        return ""

    result = text
    for phrase in FORBIDDEN_PHRASES:
        if not phrase.strip():
            continue
        escaped = re.escape(phrase)
        result = re.sub(escaped, '', result, flags=re.IGNORECASE)

    lines = []
    prev_was_empty = False

    for line in result.splitlines():
        stripped = line.strip()
        if stripped:
            lines.append(line.rstrip())
            prev_was_empty = False
        else:
            if not lines or prev_was_empty:
                continue
            lines.append('')
            prev_was_empty = True

    while lines and not lines[-1].strip():
        lines.pop()

    cleaned = "\n".join(lines)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

    return cleaned.strip()


# Обработчик одиночных сообщений
@client.on(events.NewMessage(chats=FROM_CHANNELS))
async def single_message_handler(event):
    if event.grouped_id is not None:
        return

    if ONLY_WITH_MEDIA and not event.message.media:
        return

    original_text = event.message.message or ""
    
    # Проверка по триггер-фразам
    if not should_copy_post(original_text):
        return

    try:
        clean_caption = clean_text(original_text)

        if clean_caption.strip():
            final_text = clean_caption + FOOTER
        else:
            final_text = FOOTER.lstrip()

        if not final_text.strip() and not event.message.media:
            return

        if event.message.media:
            await client.send_file(
                TARGET_CHANNEL,
                event.message.media,
                caption=final_text,
                silent=True,
                link_preview=False,
                parse_mode='md'
            )
        else:
            await client.send_message(
                TARGET_CHANNEL,
                final_text,
                silent=True,
                link_preview=False,
                parse_mode='md'
            )

        chat_repr = event.chat.title or event.chat.username or event.chat_id
        print(f"→ Скопировано (одиночное) | {chat_repr} | id: {event.message.id}")

    except Exception as e:
        print(f"Ошибка (одиночное) {event.chat_id}: {type(e).__name__}: {e}")


# Обработчик альбомов
@client.on(Album(chats=FROM_CHANNELS))
async def album_handler(event: Album.Event):
    if ONLY_WITH_MEDIA and not any(m.media for m in event.messages):
        return

    # Собираем весь текст альбома
    all_text_parts = []
    for msg in event.messages:
        if msg.message:
            all_text_parts.append(msg.message)

    full_text = "\n\n".join(all_text_parts)

    # Проверяем, нужно ли копировать этот альбом
    if not should_copy_post(full_text):
        return

    try:
        captions = []
        for msg in event.messages:
            if msg.message:
                cleaned = clean_text(msg.message)
                if cleaned.strip():
                    captions.append(cleaned)

        combined_caption = "\n\n".join(captions).strip()
        if combined_caption:
            final_caption = combined_caption + FOOTER
        else:
            final_caption = FOOTER.lstrip()

        await client.send_file(
            TARGET_CHANNEL,
            file=event.messages,
            caption=final_caption,
            silent=True,
            link_preview=False,
            parse_mode='md'
        )

        chat_repr = event.chat.title or event.chat.username or event.chat_id
        print(f"→ Скопирован альбом ({len(event.messages)} медиа) | {chat_repr} | grouped_id={event.grouped_id}")

    except Exception as e:
        print(f"Ошибка при отправке альбома из {event.chat_id}: {type(e).__name__}: {e}")


async def main():
    print("Запуск Telegram копипастера...")

    await client.connect()
    print("Соединение установлено")

    if not await client.is_user_authorized():
        print("\n=== АВТОРИЗАЦИЯ ПО QR-КОДУ ===\n")
        while True:
            try:
                qr_login = await client.qr_login()
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=4)
                qr.add_data(qr_login.url)
                qr.make(fit=True)

                print("Отсканируйте QR-код в Telegram → Настройки → Устройства → Подключить устройство")
                qr.print_ascii(invert=True)
                print("\nСсылка:", qr_login.url)
                print("\nОжидаю сканирования...")

                await qr_login.wait()
                print("Авторизация успешна!")
                break
            except Exception as e:
                if "AuthTokenExpiredError" in str(e):
                    print("QR-код истёк, генерирую новый...")
                    continue
                print(f"Ошибка QR-авторизации: {e}")
                return
    else:
        print("Уже авторизован")

    print("\nКэшируем источники...")
    for src in FROM_CHANNELS:
        try:
            ent = await client.get_entity(src)
            print(f"  • {ent.title or ent.username or src}")
        except Exception as ex:
            print(f"  • {src} → ошибка: {ex}")

    print("\n" + "═" * 60)
    print("  КОПИПАСТЕР ЗАПУЩЕН")
    print(f"  Триггер-фраз: {len(TRIGGER_PHRASES)} шт, инверсия = {INVERT_MATCH}")
    print("═" * 60)

    print(f"Цель: {TARGET_CHANNEL}")
    me = await client.get_me()
    print(f"Аккаунт: {me.first_name} (@{me.username or 'нет'})")

    print("\nОжидаю посты...")
    await client.run_until_disconnected()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nОстановлено (Ctrl+C)")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        if client.is_connected():
            loop.run_until_complete(client.disconnect())
        if not loop.is_closed():
            loop.close()
