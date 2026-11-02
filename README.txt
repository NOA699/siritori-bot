# まる用・無限しりとりBot

## できること
- 指定したDiscordチャンネルでしりとり
- 次の単語の頭文字をチェック
- 「ん」で終わったら「あ」から自動リセット
- `!しりとり状態` で現在の状態を確認
- `!しりとりリセット` で手動リセット

## 注意
この簡易版は、単語の辞書チェックや過去に出た単語の重複判定はしません。
「ん」が出たら最初から続けられる仕様です。

## 起動に必要なもの
- Python 3.10以上
- discord.py

インストール:
```bash
python -m pip install -U discord.py
```

## 設定（環境変数）
`DISCORD_TOKEN`: Discord Developer Portalで発行したBotトークン
`SHIRITORI_CHANNEL_ID`: しりとりをするチャンネルのID

Windows PowerShellでの一時設定例:
```powershell
$env:DISCORD_TOKEN="ここにBotトークン"
$env:SHIRITORI_CHANNEL_ID="ここにチャンネルID"
python bot.py
```

Botのトークンは他人に送らないでください。

## Discord側の設定
Developer PortalのBotページで **Message Content Intent** をONにしてください。
Botには対象チャンネルで「チャンネルを見る」「メッセージを送る」「メッセージ履歴を読む」権限が必要です。
