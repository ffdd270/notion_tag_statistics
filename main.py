from typing import TextIO
from notion.client import NotionClient
from notion.collection import CollectionView, Collection, CollectionRowBlock
from io import TextIOWrapper


def get_token(io: TextIO) -> str:
    read: str = io.read()

    if read.find("token_v2=") == -1:
        return "err"

    split_result: [str] = read.split("token_v2=")

    if len(split_result) != 2:
        return "err"

    return split_result[1]


def get_tags_count(notion_client: NotionClient, path: str, tag_name: str) -> dict:
    collection_view: CollectionView = notion_client.get_collection_view(path)
    collection: Collection = collection_view.collection

    row_cnt : int = 0
    schema: list = None
    name_to_slug: str = None
    tags_dict: dict = {}

    for row in collection.get_rows():
        collection_row: CollectionRowBlock = row

        if schema is None:
            schema = collection_row.schema

            for schema_item in schema:
                if schema_item['name'] == tag_name:
                    name_to_slug = schema_item['slug']
                    break

            if name_to_slug is None:
                print("Maybe, that is wrong property.")
                return {}

        attr_value = getattr(collection_row, name_to_slug)

        row_cnt += 1

        if attr_value is None:
            continue

        if isinstance(attr_value, list):
            for tag in attr_value:
                if tags_dict.get(tag) is None:
                    tags_dict[tag] = 0
                tags_dict[tag] += 1
        elif isinstance(attr_value, str):
            if tags_dict.get(attr_value) is None:
                tags_dict[attr_value] = 0
            tags_dict[attr_value] += 1

    return tags_dict, row_cnt


account: TextIO = open("notion_account.env", "r")
token = get_token(account)

client = NotionClient(token_v2=token)

tags, cnt = get_tags_count(client,
                      "https://www.notion.so/kuronekolab/d9b2cc36d2d24d28b92c7f4a18741ebd?v=810efb113d8d40ffaa307fe494471217",
                      "상태");
sort_tag: [dict] = []

for k in tags:
    sort_tag.append({'key': k, 'value': tags[k]})

sort_tag.sort(key=lambda v: v['value'], reverse=True)

for v in sort_tag:
    print(v)

print('CNT : ', cnt)