import argparse
import textwrap


def build_draft_prompt(message: str) -> str:
    return textwrap.dedent(f"""
    Draft a short, professional WhatsApp reply to the message below.
    Use a polite, concise tone and avoid long paragraphs.
    Keep the reply between 2 and 4 sentences.
    Include a clear next step or question when appropriate.
    Do not use markdown, bullet points, or code blocks.

    Original message:
    {message}
    """)


def build_summary_prompt(message: str) -> str:
    return textwrap.dedent(f"""
    Summarize the key point of the WhatsApp message below in one sentence.
    Keep it factual and short.

    Original message:
    {message}
    """)


def build_reply_workflow_prompt(message: str) -> str:
    return textwrap.dedent(f"""
    1. Read the WhatsApp message below.
    2. Summarize it in one sentence.
    3. Draft a short professional reply to the sender.
    4. Keep the final reply polite, helpful, and concise.
    5. If the message is a question, answer it directly and ask for the next step.
    6. Do not include extra explanation or commentary in the final reply.

    Original message:
    {message}
    """)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='WhatsApp prompt flow helper for OpenClaw.'
    )
    parser.add_argument(
        '--action',
        choices=['draft', 'summarize', 'workflow'],
        required=True,
        help='Type of helper prompt to generate.'
    )
    parser.add_argument(
        '--message',
        required=True,
        help='The incoming WhatsApp message text.'
    )

    args = parser.parse_args()
    if args.action == 'draft':
        print(build_draft_prompt(args.message))
    elif args.action == 'summarize':
        print(build_summary_prompt(args.message))
    elif args.action == 'workflow':
        print(build_reply_workflow_prompt(args.message))


if __name__ == '__main__':
    main()
