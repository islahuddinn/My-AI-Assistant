---
name: voice_reply
description: Handles WhatsApp voice notes — transcribes incoming voice notes and can reply with a voice note using TTS.
---

# Voice Note Reply Skill

This is an always-on skill that governs how the assistant handles voice notes.

## Standing behavior (always active)

### When you receive a voice note on WhatsApp:
1. The voice note is automatically transcribed to text by OpenClaw's Whisper integration
2. Treat the transcription like any other message and respond accordingly
3. Always include the transcription at the top of your reply so the user knows what was understood:
   ```
   🎤 Heard: "[transcription]"
   ```
4. Then provide your actual response below.

### When to reply with a voice note:
- If the user says **"reply with voice"** or **"send voice note"** — reply using TTS
- If the user's message was a voice note AND they have previously asked for voice replies — use TTS
- Otherwise, reply with text by default

### TTS reply format:
When responding with audio, keep the spoken reply concise and conversational. Avoid:
- Long lists
- Code blocks
- URLs
- Markdown formatting

Instead, say things like: "I found 5 jobs matching your criteria. The top one is a Senior React Developer at Acme Corp paying four to six thousand dollars per month."

## Commands
- "reply with voice" — toggle TTS replies ON for this conversation
- "text only" — switch back to text replies
- "what did you hear?" — repeat the transcription of the last voice note

## Notes
- Voice note transcription is handled natively by OpenClaw's Baileys WhatsApp channel
- TTS is configured in `setup/config/openclaw.json` under `messages.tts`
- Supported TTS providers: OpenAI (alloy, nova, shimmer), ElevenLabs
