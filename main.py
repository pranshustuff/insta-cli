#!/usr/bin/env python3

from fetch import get_filtered_threads
from session import login
import argparse
from dotenv import dotenv_values
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "title": "magenta",
    "you": "blue",
    "other": "yellow",
    "link": "blue",
    "dim": "dim",
})

console = Console(theme=custom_theme)

config = dotenv_values(".env")
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
        console.print(f"\nThread: {thread.thread_title}", style="title")
        
        for message in thread.messages:
            sender_id = message.user_id
            sender_name = next(
                (user.username for user in thread.users if user.pk == sender_id),
                "You"
            )

            is_you = sender_name == "You"
            style = "you" if is_you else "other"

            console.print(f"{sender_name}:", style=style)

            if message.clip is not None:
                code = message.clip.code
                console.print(f"  https://www.instagram.com/reel/{code}", style="link")
            elif message.text is not None:
                console.print(f"  {message.text}")
            elif message.reel_share:
                url = message.reel_share.media.code
                console.print(f"  https://www.instagram.com/reel/{url}", style="link")
            else:
                console.print(f"  [{message.item_type}]", style="dim")

if __name__ == "__main__":
    main()
