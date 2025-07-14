# Read DMs from your terminal

## How to install
- Downaload the code
- Create a .env in the same directory with:
  ```
  USERNAME=<Your-Username>
  PASSWORD=<Your=password>
  ```
- `pip install -r requirements.txt`

**Important** : Go to where your instagrapi is installed. Then go to `instagrapi > types.py` and delete line `419 clips_metadata: Optional[ClipsMetadata] = None`. 

Will update if any changes occur in the code and I figure things in a better way.



## Features

`python3 main.py` - Reads your latest 5 threads and 5 messages each.

**Flags** : 
- `--unread` : only unread
- `--threads <n>` : reads top n threads
- `--messages <x>` : reads last x messages from top n threads
             
