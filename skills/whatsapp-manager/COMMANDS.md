# WhatsApp Command Mappings

This document maps common WhatsApp phrases to OpenClaw actions and prompt flows.

## Core Commands

### Summarize Message
When user sends: `"Summarize my last message"` or `"Explain that message"`

Trigger action:
```bash
exec: python ~/.openclaw/skills/whatsapp-manager/scripts/whatsapp_prompt_flow.py --action summarize --message "<message_text>"
```

**Prompt used:**
"Summarize the key point of the WhatsApp message below in one sentence. Keep it factual and short."

---

### Draft Professional Reply
When user sends: `"Draft a reply"`, `"Help me respond"`, or `"Write a professional response"`

Trigger action:
```bash
exec: python ~/.openclaw/skills/whatsapp-manager/scripts/whatsapp_prompt_flow.py --action draft --message "<message_text>"
```

**Prompt used:**
"Draft a short, professional WhatsApp reply to the message below. Use a polite, concise tone and avoid long paragraphs. Keep the reply between 2 and 4 sentences. Include a clear next step or question when appropriate."

---

### Full Workflow (Summary + Reply)
When user sends: `"Help me respond to this message"` or `"Full response workflow"`

Trigger action:
```bash
exec: python ~/.openclaw/skills/whatsapp-manager/scripts/whatsapp_prompt_flow.py --action workflow --message "<message_text>"
```

**Prompt used:**
1. Read the WhatsApp message
2. Summarize it in one sentence
3. Draft a short professional reply
4. Format the final reply as concise, helpful text

---

## Context-Aware Triggers

### Job Inquiry / Recruiter Message
Detects when message contains: `job`, `contract`, `available`, `position`, `role`, `hiring`, `developer`, `engineer`, `technical`

Use quick-action template: **Job Inquiry Response** (see QUICK_ACTIONS.md)

### Thanks / Appreciation
Detects when message contains: `thank`, `thanks`, `appreciate`, `grateful`, `excellent`, `great work`

Use quick-action template: **Acknowledgment Reply** (see QUICK_ACTIONS.md)

### Question / Request for Information
Detects when message contains: `?` or words: `what`, `how`, `when`, `where`, `why`, `need`, `require`, `looking for`

Use quick-action template: **Question Response** (see QUICK_ACTIONS.md)

---

## Command Registration (OpenClaw Integration)

Add these to your WhatsApp assistant's recognized phrases:

```
"summarize|summary|explain that|what did they say" → summarize action
"draft|respond|reply|help me respond|write a response" → draft action
"full workflow|complete response|full help" → workflow action
"job question|recruiter asking" → job_inquiry quick action
"thanks|thank you|appreciation" → acknowledgment quick action
"how do i|what should i|need help" → question quick action
```

---

## Usage Examples

### Example 1: Recruiter inquiry
**Incoming:** "Hi Islahuddin, are you open to a React developer role at TechCorp?"

**User command:** `Draft a reply`

**Assistant generates:**
```
Thank you for the opportunity! I'm interested in React development roles, especially with MERN stack. Could you share the job details, timeline, and compensation range?
```

---

### Example 2: Thanks message
**Incoming:** "Thanks for the great collaboration on the project!"

**User command:** `Summarize and reply`

**Assistant generates:**
```
Summary: Sender is thanking you for good project collaboration.

Reply: Thank you! I really enjoyed working with you too. Feel free to reach out if you need any support in the future.
```

---

### Example 3: General question
**Incoming:** "Are you available for a meeting tomorrow at 3 PM?"

**User command:** `Draft a professional response`

**Assistant generates:**
```
Yes, I'm available tomorrow at 3 PM. Please send me the meeting link or details. Thanks!
```

---

## Extending Commands

To add new command mappings:

1. Edit this file and add a new section
2. Define the trigger phrases
3. Point to the action/template
4. Test with `openclaw test --skill whatsapp-manager`
