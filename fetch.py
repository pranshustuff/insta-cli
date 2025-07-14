# fetch.py

USEFUL_TYPES = {
    "text", "media", "reel_share", "media_share", "link",
    "felix_share", "story_share", "clip"
}


def get_filtered_threads(client, amount=5, useful_limit=5, selected_filter=""):
    threads = client.direct_threads(amount=amount, selected_filter=selected_filter)
    filtered_threads = []

    for thread in threads:
        sorted_messages = sorted(thread.messages, key=lambda m: m.timestamp, reverse=True)
        useful_messages = [m for m in sorted_messages if m.item_type in USEFUL_TYPES]

        # Trim to useful_limit
        useful_messages = useful_messages[:useful_limit]
        useful_messages.sort(key=lambda m: m.timestamp)

        thread.messages = useful_messages
        filtered_threads.append(thread)

    return filtered_threads

