from typing import TextIO
from notion.client import NotionClient
from io import TextIOWrapper


def get_token(io: TextIO) -> str:
    read: str = io.read()

    if read.find("token_v2=") == -1:
        return "err"

    split_result: [str] = read.split("token_v2=")

    if len(split_result) != 2:
        return "err"

    return split_result[1]


account: TextIO = open("notion_account.env", "r")
token = get_token(account)

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2="<" + token + ">")

# Replace this URL with the URL of the page you want to edit
page = client.get_block("https://www.notion.so/sihawn/")

print("The old title is:", page.title)

# Note: You can use Markdown! We convert on-the-fly to Notion's internal formatted text data structure.
#page.title = "The title has now changed, and has *live-updated* in the browser!"
