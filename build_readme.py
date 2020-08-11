# Credits to: Simon Willison automatic readme generation idea from https://github.com/simonw
# Thanks!

import feedparser
import pathlib
import re

root = pathlib.Path(__file__).parent.resolve()


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!-- {} starts -->.*<!-- {} ends -->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_blog_entries():
    fetched_entries = feedparser.parse("https://dafonte.dev/feed.xml")["items"]
    return [
        {
            "title": fetched_entry["title"],
            "url": fetched_entry["link"].split("#")[0],
            "published": fetched_entry["published"].replace('00:00:00 +0000', ''),
        }
        for fetched_entry in fetched_entries
    ]


if __name__ == "__main__":
    readme = root / "README.md"

    entries = fetch_blog_entries()[:5]
    entries_md = "\n\n".join(
        ["[{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    readme_contents = readme.open().read()
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    readme.open("w").write(rewritten)
