# Telegram Configuration for Phase 2a Content Alerts

## Bot & Channels

| Item | Value |
|---|---|
| **Bot Token** | `TELEGRAM_BOT_TOKEN` (GitHub secret + Routine env var) |
| **Reviewer Chat** | `TELEGRAM_REVIEWER_CHAT_ID` = `-1003902679807` (Personal Assistant group) |
| **Content Pipeline Topic** | `CONTENT_PIPELINE_TOPIC_ID` = `67` (message_thread_id in Personal Assistant group) |
| **Facilitators Group** | `TELEGRAM_GROUP_CHAT_ID` = `-1002312729680` |

---

## Notification Flow

### On git push to `content/week-*` → `content-publish.yml` GHA

Triggered automatically when the Routine pushes the branch (Step P5). Sends **one** notification to the reviewer group:

| Target | Message |
|---|---|
| Content Pipeline topic (thread_id=67) | 📬 "PR Ready for Review — Week N: Topic" with PR URL + `/approve`, `/rework`, `/reject` actions |

This fires only on the **first push** per branch (idempotent — skipped on rework re-pushes).

### On PR merge → `pr-notify.yml` GHA

| Target | Message |
|---|---|
| Facilitators group | 🎉 "Content Published — Week N is live" |
| Content Pipeline topic | ✅ "Week N merged by [user]" |

### On `/rework` → API trigger → Content Rework Routine

No Telegram notification sent automatically during rework. The Routine commits to the same branch; `pr-notify.yml` fires on the `synchronize` event if configured.

### On `/reject` → `pr-commands.yml` GHA

| Target | Message |
|---|---|
| Content Pipeline topic | ❌ "PR Rejected — branch deleted. Reason: [reason]" |

---

## API Call Pattern

```bash
# To Content Pipeline topic (with thread_id)
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${REVIEWER_CHAT_ID}" \
  -d "message_thread_id=${TOPIC_ID}" \
  -d "parse_mode=Markdown" \
  --data-urlencode "text=${MESSAGE}"

# To Facilitators group (no thread_id)
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${GROUP_CHAT_ID}" \
  -d "parse_mode=Markdown" \
  --data-urlencode "text=${MESSAGE}"
```

---

## Notes

- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_REVIEWER_CHAT_ID`, `CONTENT_PIPELINE_TOPIC_ID` must be set in both the Routine environment AND as GitHub Actions secrets (used by `content-publish.yml` and `pr-commands.yml`)
- `TELEGRAM_GROUP_CHAT_ID` is only needed as a GitHub Actions secret (used by `pr-notify.yml` post-merge)
- The pipeline itself (Claude Routine) does **not** send Telegram directly — all notifications go through GHA workflows
