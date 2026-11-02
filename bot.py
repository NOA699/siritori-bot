import os
import re
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID_TEXT = os.getenv("SHIRITORI_CHANNEL_ID")

if not TOKEN:
    raise RuntimeError("環境変数 DISCORD_TOKEN が設定されていません。")
if not CHANNEL_ID_TEXT:
    raise RuntimeError("環境変数 SHIRITORI_CHANNEL_ID が設定されていません。")

CHANNEL_ID = int(CHANNEL_ID_TEXT)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ひらがな・カタカナの小文字を通常サイズに寄せる簡易変換
SMALL_TO_NORMAL = str.maketrans({
    "ぁ":"あ", "ぃ":"い", "ぅ":"う", "ぇ":"え", "ぉ":"お",
    "ゃ":"や", "ゅ":"ゆ", "ょ":"よ", "っ":"つ", "ゎ":"わ",
    "ァ":"ア", "ィ":"イ", "ゥ":"ウ", "ェ":"エ", "ォ":"オ",
    "ャ":"ヤ", "ュ":"ユ", "ョ":"ヨ", "ッ":"ツ", "ヮ":"ワ",
})

def normalize_word(text: str) -> str:
    # 空白や句読点、絵文字等を除き、ひらがな・カタカナだけを対象にする
    text = text.strip().translate(SMALL_TO_NORMAL)
    text = re.sub(r"[ー〜～]", "", text)
    kana = re.findall(r"[ぁ-ゖァ-ヺ]", text)
    return "".join(kana)

def first_kana(word: str) -> str:
    return word[0] if word else ""

def last_kana(word: str) -> str:
    return word[-1] if word else ""

current_start = "あ"
last_word = None

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user} (ID: {bot.user.id})")
    print(f"しりとりチャンネル ID: {CHANNEL_ID}")

@bot.event
async def on_message(message: discord.Message):
    global current_start, last_word

    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        await bot.process_commands(message)
        return

    raw = message.content
    word = normalize_word(raw)

    if not word:
        await bot.process_commands(message)
        return

    # 最初の単語、またはリセット後は「あ」など指定文字から開始
    if first_kana(word) != current_start:
        await message.reply(
            f"❌「{current_start}」から始まる言葉を入れてね！",
            mention_author=False
        )
        await bot.process_commands(message)
        return

    # 「ん」で終わる単語を投稿したら、しりとりを「あ」からリセット
    if last_kana(word) == "ん":
        last_word = None
        current_start = "あ"
        await message.reply(
            f"🔄「{raw.strip()}」は「ん」で終わったよ！しりとりリセット！次は「あ」から！",
            mention_author=False
        )
        await bot.process_commands(message)
        return

    last_word = word
    current_start = last_kana(word)
    await message.add_reaction("✅")
    await message.reply(
        f"次は「{current_start}」から！",
        mention_author=False
    )

    await bot.process_commands(message)

@bot.command(name="しりとり状態")
async def shiritori_status(ctx: commands.Context):
    if ctx.channel.id != CHANNEL_ID:
        return
    if last_word is None:
        await ctx.reply(f"しりとり中！最初は「{current_start}」からだよ。")
    else:
        await ctx.reply(f"最後の言葉は「{last_word}」！次は「{current_start}」からだよ。")

@bot.command(name="しりとりリセット")
async def shiritori_reset(ctx: commands.Context):
    global current_start, last_word
    if ctx.channel.id != CHANNEL_ID:
        return
    current_start = "あ"
    last_word = None
    await ctx.reply("🔄 しりとりを「あ」からリセットしたよ！")

bot.run(TOKEN)
