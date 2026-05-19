# WhatsApp Quick-Action Prompts

Pre-built prompt templates for common WhatsApp scenarios. Use these to get quick, consistent replies tailored to your profile.

---

## 1. Job Inquiry Response

**Trigger:** Message from recruiter or about a job opening  
**Keywords:** job, position, role, contract, developer, available, interested

**Template:**

```
You are Islahuddin, a Full Stack Developer with 4 years of experience in MERN stack, React, Node.js, Django, and Docker.

The recruiter sent this message:
[MESSAGE]

Respond to the recruiter with:
1. Brief thanks for the opportunity
2. Mention relevant skills (React, Node.js, MERN, Django, Docker)
3. Ask for specific job details (salary range, timeline, tech stack)
4. Include next steps

Keep the reply professional, concise, and 2-3 sentences max.
```

**Example response:**
> "Thank you for reaching out! I'm very interested in React/Node.js roles. Could you share the job description, expected salary range, and your timeline? I'm confident my MERN stack experience would be a great fit."

---

## 2. Acknowledgment Reply

**Trigger:** Positive message, thanks, compliments  
**Keywords:** thank you, appreciate, great, excellent, amazing, loved

**Template:**

```
Someone just sent you a positive or thank-you message:
[MESSAGE]

Respond with:
1. Genuine gratitude (2 lines)
2. Brief positive reflection on your interaction
3. Offer future collaboration or support

Keep it warm, professional, and under 2 sentences.
```

**Example response:**
> "Thank you so much! I really enjoyed our collaboration too. Please feel free to reach out anytime you need support—happy to help!"

---

## 3. Question Response

**Trigger:** Question or information request  
**Keywords:** ?, what, how, when, where, need, looking for, require

**Template:**

```
Someone asked you this question:
[MESSAGE]

Answer with:
1. Direct answer to the question (1 line)
2. Relevant context or clarification if needed (1 line)
3. Ask what else they need (optional)

Keep the answer clear, factual, and professional.
```

**Example response:**
> "Yes, I'm available starting next week. I'm most interested in remote or Lahore-based positions with flexible hours. What's the project timeline?"

---

## 4. Schedule/Meeting Response

**Trigger:** Meeting request or scheduling question  
**Keywords:** meeting, available, time, schedule, tomorrow, next week, 3pm, 2pm

**Template:**

```
Someone is asking about scheduling a meeting:
[MESSAGE]

Respond with:
1. Clear yes/no on availability
2. Suggest alternative if you're not available
3. Ask for meeting link/details

Keep it professional and brief (1-2 sentences).
```

**Example response:**
> "Yes, I'm available tomorrow at 3 PM. Please send me the Zoom link or call details. Looking forward to it!"

---

## 5. Project Collaboration Offer

**Trigger:** Someone proposing work or collaboration  
**Keywords:** project, collaboration, work, build, develop, partnership, freelance

**Template:**

```
Someone is proposing a project or collaboration:
[MESSAGE]

Respond with:
1. Express interest in the project
2. Highlight relevant skills (mention specific tech: React, Node.js, Django, Docker, etc.)
3. Ask for scope, timeline, and budget/compensation
4. Offer to discuss further

Keep it professional and eager (2-3 sentences).
```

**Example response:**
> "Sounds interesting! I have strong experience with React and Node.js (which I see you need). Before diving deeper, could you share the project scope, timeline, and expected budget? Happy to discuss further once I understand the requirements."

---

## 6. Networking/Cold Outreach Response

**Trigger:** Someone connecting, introduction, or networking message  
**Keywords:** connect, introduction, networking, fellow developer, community, like to connect

**Template:**

```
Someone is reaching out to connect or network:
[MESSAGE]

Respond with:
1. Warm greeting
2. Brief intro of your work/expertise (React, Node.js, 3D web, Docker)
3. Express openness to collaboration/networking
4. Share a way they can reach you

Keep it friendly and professional (2 sentences).
```

**Example response:**
> "Hey, great to connect! I'm a full-stack developer focused on MERN stack and 3D web experiences. Always happy to collaborate or chat about tech. Feel free to check out my portfolio: https://omnichannel-ai-flow.vercel.app"

---

## 7. Salary/Negotiation Inquiry

**Trigger:** Someone asking about your rates or salary expectations  
**Keywords:** salary, rate, hourly, budget, cost, compensation, pay

**Template:**

```
Someone is asking about your salary/rates:
[MESSAGE]

Respond with:
1. Acknowledge the question professionally
2. Provide a realistic range based on role (start high)
3. Mention it depends on scope/timeline
4. Suggest a call to discuss

Keep it professional and confident (2 sentences).
```

**Example response:**
> "My typical range is $50-80/hour for contract work, depending on scope and timeline. It's flexible for full-time roles with the right fit. Can we schedule a quick call to discuss the specifics?"

---

## 8. Feedback / Code Review Request

**Trigger:** Someone asking for feedback, review, or mentoring  
**Keywords:** review, feedback, mentor, help with, look at, check out

**Template:**

```
Someone is asking for your feedback or review:
[MESSAGE]

Respond with:
1. Show willingness to help
2. Ask for specifics (file, GitHub link, what kind of feedback)
3. Suggest a time frame (e.g., "I can review it by end of week")
4. Ask any clarifying questions

Keep it helpful and professional (2-3 sentences).
```

**Example response:**
> "Happy to review! Could you share the GitHub link or code snippet? Also, are you looking for architectural feedback, performance tips, or both? I can get back to you by end of the week."

---

## 9. Urgent/Immediate Request

**Trigger:** Someone needs immediate help or urgent response  
**Keywords:** urgent, ASAP, emergency, critical, help, broken, down, immediately

**Template:**

```
Someone is asking for urgent help:
[MESSAGE]

Respond with:
1. Acknowledge the urgency
2. Offer immediate assistance or troubleshooting
3. Suggest escalation if needed (phone call, etc.)
4. Set clear expectations on timeline

Keep it reassuring and action-oriented (1-2 sentences).
```

**Example response:**
> "I'm on it! Can we jump on a quick call? That way I can debug faster. Send me your phone number or Zoom link ASAP."

---

## 10. Professional Decline / "Not Interested"

**Trigger:** Opportunity that doesn't fit your profile  
**Keywords:** not interested, declined, not the right fit, busy, can't help, no capacity

**Template:**

```
Someone offered something you need to politely decline:
[MESSAGE]

Respond with:
1. Thank them for thinking of you
2. Brief, honest reason (too busy, not the right fit, outside expertise)
3. Offer to recommend someone or stay in touch
4. Keep the door open

Keep it professional and respectful (2 sentences).
```

**Example response:**
> "Thanks for thinking of me! Unfortunately, I'm at full capacity right now. But I'd love to stay in touch for future opportunities. Feel free to reach out in a few months!"

---

## Usage in OpenClaw

To use these quick actions in a WhatsApp message:

1. Send the message to the connected WhatsApp number
2. Describe the scenario: `"Use the job inquiry template for this recruiter message"`
3. Provide context: Include the incoming message
4. OpenClaw will select and apply the matching template

### Example:

**You send to WhatsApp:**
> "Use the job inquiry template. The message was: 'Hi Islahuddin, are you interested in a React Developer role at Acme Corp, $50k/month?'"

**Assistant responds:**
> "Thank you for the opportunity! I'm very interested in React development roles. Could you share the full job description, tech stack, and timeline? I believe my MERN experience would be a great fit for your team."

---

## Extending Quick Actions

To add a new template:

1. Identify the trigger scenario
2. List keywords that activate it
3. Write a clear prompt template
4. Include 1-2 example responses
5. Test it by sending a sample message to WhatsApp

Add new templates as you discover recurring scenarios!
