# Telegram Configuration for Phase 2a Content Alerts

## Bot Setup

- **Bot Token**: `TELEGRAM_BOT_TOKEN` in `.env` (repo root, gitignored)
- **Group Chat ID**: `TELEGRAM_GROUP_CHAT_ID` in `.env` (repo root, gitignored)

## Message Template

```
📚 Phase 2a Python — Week N Content Published

**Topic:** [Topic Name]
**Week:** N of 8
**Session:** [Wednesday / Thursday]

✅ Lesson plan: [GitHub link]
📂 Solutions: [Google Drive link]

🎯 Key coverage:
- [Key skill 1]
- [Key skill 2]
- [Key skill 3]

[Optional: AI introduction note]
[Optional: Streamlit note]

Bible verse: [Quote N of 8]
```

## Rotating Bible Quotes (8 weeks)

| Week | Quote |
|---|---|
| 1 | "The wise store up knowledge..." (Proverbs 10:14) |
| 2 | "For to one is given through the Spirit the utterance of wisdom..." (1 Corinthians 12:8) |
| 3 | "The fear of the LORD is the beginning of knowledge..." (Proverbs 1:7) |
| 4 | "Lean not on your own understanding..." (Proverbs 3:5) |
| 5 | "By wisdom a house is built, and by understanding it is established..." (Proverbs 24:3) |
| 6 | "Apply your heart to instruction and your ears to words of knowledge." (Proverbs 23:12) |
| 7 | "Great is our Lord and mighty in power; his understanding has no limit." (Psalm 147:5) |
| 8 | "Now to him who is able to do immeasurably more than all we ask or imagine..." (Ephesians 3:20) |

## API Call Pattern

```bash
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${GROUP_ID}" \
  -d "text=${MESSAGE}" \
  -d "parse_mode=Markdown"
```
