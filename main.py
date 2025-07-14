#!/usr/bin/env python3

from fetch import get_filtered_threads
from session import login
import argparse
from dotenv import dotenv_values
from rich.console import Console # type: ignore
from rich.theme import Theme # type: ignore
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

custom_theme = Theme({
    "title": "red",
    "you": "cyan",
    "other": "yellow",
    "link": "blue",
    "dim": "dim",
})

console = Console(theme=custom_theme)

config = dotenv_values("/home/pranshu/insta-cli/.env")
user = config["USERNAME"]
pwd = config["PASSWORD"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unread", action="store_true")
    parser.add_argument("--thread", type=int, default=5)
    parser.add_argument("--messages", type=int, default=5)

    args = parser.parse_args()

    client = login()

    threads = get_filtered_threads(
        client,
        amount=args.thread,
        useful_limit=args.messages,
        selected_filter="unread" if args.unread else ""
    )

    for thread in threads:
        # Title box for each thread
        thread_title = Text(thread.thread_title, style="title")
        console.print(Panel(thread_title, expand=False, border_style="title"))

        # Message list
        for message in thread.messages:
            sender_id = message.user_id
            sender_name = next(
                (user.username for user in thread.users if user.pk == sender_id),
                "You"
            )

            is_you = sender_name == "You"
            name_style = "you" if is_you else "other"
            name_label = Text(sender_name, style=name_style)

            # Construct message content
            if message.clip is not None:
                content = f"https://www.instagram.com/reel/{message.clip.code}"
                console.print(Panel(Text(content, style="link"), title=name_label, expand=False))
            elif message.text is not None:
                console.print(Panel(Text(message.text), title=name_label, expand=False))
            elif message.reel_share:
                code = message.reel_share.media.code
                content = f"https://www.instagram.com/reel/{code}"
                console.print(Panel(Text(content, style="link"), title=name_label, expand=False))
            else:
                console.print(Panel(Text(f"[{message.item_type}]", style="dim"), title=name_label, expand=False))

        console.print()  # Empty line between threads
if __name__ == "__main__":
    main()
