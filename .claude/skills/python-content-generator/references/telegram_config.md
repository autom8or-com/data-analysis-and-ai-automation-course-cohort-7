# Telegram Configuration for Phase 2a Content Alerts

## Bot & Channels

| Item | Value |
|---|---|
| **Bot Token** | `TELEGRAM_BOT_TOKEN` in `.env` |
| **Reviewer Chat** | `TELEGRAM_REVIEWER_CHAT_ID` = `-1003902679807` (Personal Assistant group) |
| **Content Pipeline Topic** | `CONTENT_PIPELINE_TOPIC_ID` = `67` (message_thread_id in Personal Assistant group) |
| **Facilitators Group** | `TELEGRAM_GROUP_CHAT_ID` = `-1002312729680` |

## Notification Flow (Two-Phase)

### Phase 1: Generation (Pipeline Steps 11c & 13)

Sent during content generation, before PR merge:

| Step | Event | Target | Purpose |
|---|---|---|---|
| 11c | PR Created | Content Pipeline topic (thread_id=67) | 📬 "PR Ready for Review — Week N" with link + merge/rework/close actions |
| 13 | Pipeline Complete | Content Pipeline topic (thread_id=67) | ⚙️ "Pipeline Complete — waiting for your review" with status summary |

### Phase 2: Publishing (GitHub Actions, post-merge)

Sent when you merge the PR:

| Trigger | Event | Target | Purpose |
|---|---|---|---|
| PR merged | Content Published | Facilitators group | 🎉 "Content Published! Solutions on Drive, NocoDB updated" |

## PR Notification Template (Step 11c)

```
📬 **PR Ready for Review — Week {N}**

**Topic:** {Topic Name}
**Branch:** `content/week-NN-slug`

🔗 {PR URL}

**Actions:**
• Merge to publish content to students
• Comment `/rework` to request changes
• Close to cancel
```

## Pipeline Status Template (Step 13)

```
⚙️ **Phase 2a Python — Week {N} Pipeline Complete**

**Topic:** {Topic Name}
**Branch:** `content/week-NN-slug`

✅ Content generated & PR created
✅ Solutions uploaded to Google Drive

⏳ *Waiting for your review and merge on GitHub*
```

## Rework Alert (Rework Comment Poller cron)

Triggered by the rework poller (every 30 min) when `/rework <notes>` is found on an open PR:

```
🔄 **Rework Requested — PR #{N}**

**Branch:** `content/week-NN-slug`
**By:** {author}

**Notes:** {rework notes}

🔗 {PR URL}

*Checking out branch and fixing now...*
```

## API Call Pattern

```bash
# To Content Pipeline topic (with thread_id)
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${REVIEWER_CHAT_ID}" \
  -d "message_thread_id=${TOPIC_ID}" \
  -d "text=${MESSAGE}" \
  -d "parse_mode=Markdown"

# To Facilitators group (no thread_id)
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${GROUP_CHAT_ID}" \
  -d "text=${MESSAGE}" \
  -d "parse_mode=Markdown"
```

## Notes

- Bible quotes were removed from the pipeline (Step 13 is a status message, not a "published" celebration)
- The GitHub Actions workflow (`pr-notify.yml`) handles the merge notification
- All values are stored in `.env` at repo root AND as GitHub Actions secrets
