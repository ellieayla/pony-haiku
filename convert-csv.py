#!/usr/bin/env python

from csv import DictReader
import os
from datetime import datetime, date
from textwrap import indent


OUTPUT_DIR = "/Users/ellie/workspace/respondwithponyhaiku/respond-with-pony-haiku/_posts"
REDDIT = 'https://old.reddit.com'


def parse_date(s) -> datetime:
    # s, like 1/14/2012 0:00:00
    d = datetime.strptime(s, "%m/%d/%Y %H:%M:%S")
    return d


def export_row(row):
    assert(row['threadid'][0:3] == 't3_')
    assert(row['id'])

    row['threadid'] = row['threadid'][3:]
    published = parse_date(row['created_utc'])

    output_file = f"{OUTPUT_DIR}/{published.date().isoformat()}-{row['id']}.md"

    print(output_file)


    with open(output_file, 'w') as f:
        f.write("---\n")
        f.write("layout: haiku\n")
        for field in ('subreddit', 'threadid', 'id'):
            f.write(f"{field}: {row[field]}\n")

        f.write(f"date: {published.isoformat()} +0000\n")

        permalink = f"{REDDIT}/r/{row['subreddit']}/comments/{row['threadid']}/_/{row['id']}"
        f.write(f"reddit: {permalink}\n")  # http://www.reddit.com/r/mylittleonions/comments/od8mb/_/c3gx5el
        f.write(f"reddit_context: {permalink}?context=3\n")  # http://www.reddit.com/r/mylittleonions/comments/od8mb/_/c3gx5el?context=3

        f.write("html: |\n")
        f.write(indent(row['body_html'], "   "))
        f.write("\n")

        f.write("---\n\n")

        f.write(row['body'])


def main():

    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    with open('Untitled spreadsheet - Extract 1.csv') as f:
        csv = DictReader(f)

        for row in csv:
            export_row(row)



if __name__ == '__main__':
    main()