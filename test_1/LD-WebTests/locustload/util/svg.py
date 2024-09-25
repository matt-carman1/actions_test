import sys
import csv
import typing
import math
from functools import reduce
"""
Generates an SVG visualization of all timed actions recorded by a Locust test run.
Requires "*_all_data.csv" file as its input, which is produced by Locust (when executed with make). 

Usage:

    $ svg.py input.csv output.svg 

"""


class Record(typing.NamedTuple):
    name: str
    start: float  # seconds since epoch
    end: float  # seconds since epoch
    success: bool


def build_action_forests(input_csv_filename):
    with open(input_csv_filename, "r") as input_file:
        # Read timed actions
        records = {}
        for row in csv.DictReader(input_file):
            if row['http_method'] == 'action':
                locust_user_id = int(row['locust_user_id'])
                if locust_user_id not in records:
                    records[locust_user_id] = []
                rec = Record(
                    row['name'],
                    float(row['start']),
                    float(row['end']),
                    float(row['success'] == 'True'),
                )
                records[locust_user_id].append(rec)

        forests = {}
        for user_id in records:
            # Sort by starting time ascending; if equal, sort by the event duration (end-start) descending
            records[user_id].sort(key=lambda r: [r.start, -r.end])

            # Build a tree of records for this Locust user
            # Assuming all recorded times are monotonic and child actions are correctly nested within their parents:
            # parent start <= child start <= child end <= parent end
            recs = records[user_id]

            # The lists and dicts below are keeping track of the indexes in list recs
            roots = []
            children = {i: [] for i in range(len(recs))}
            stack = []
            i = 0
            while i <= len(recs):
                its_the_end = (i == len(recs))
                # Pop from the stack the actions that are not ancestors of i
                while len(stack) > 0 and (its_the_end or recs[stack[-1]].end < recs[i].end):
                    i_top = stack.pop()
                    if len(stack) > 0:
                        i_parent_of_top = stack[-1]
                        children[i_parent_of_top].append(i_top)
                    else:
                        roots.append(i_top)
                if not its_the_end:
                    stack.append(i)
                i += 1

            forests[user_id] = (recs, roots, children)

        return forests


def uid():
    if not hasattr(uid, "counter"):
        uid.counter = 0
    uid.counter += 1
    return uid.counter


def human_time(seconds):
    if seconds >= 10:
        return f'{round(seconds)} s'
    else:
        return f'{round(seconds*1000)} ms'


def tree_height(children, root):

    def height(node):
        return 1 + reduce(max, map(height, children[node]), 0)

    return height(root)


def forest_height(children):
    return max([tree_height(children, root) for root in children])


def generate_svg(input_csv_filename, output_svg_filename):
    with open(output_svg_filename, "w") as output_file:
        forests = build_action_forests(input_csv_filename)

        start = math.inf
        end = -math.inf
        total_height = 0
        for (records, _, children) in forests.values():
            start = min(start, min([rec.start for rec in records]))
            end = max(end, max([rec.end for rec in records]))
            total_height += forest_height(children) + 1

        duration = end - start
        px_per_second = 15
        px_vertical = 15
        image_width = duration * px_per_second
        image_height = total_height * px_vertical

        def box(record, parity, x, y):
            if parity % 2 == 0:
                fill_color = '#bbb' if record.success else '#f80'
                stroke_color = '#888' if record.success else '#a40'
            else:
                fill_color = '#ccc' if record.success else '#ffa000'
                stroke_color = '#999' if record.success else '#a50'

            text_color = '#666' if record.success else '#a40'

            x0 = x * px_per_second
            y0 = y * px_vertical
            w = (record.end - record.start) * px_per_second
            h = px_vertical
            clip_id = f'clip{uid()}'
            message = f'{record.name}, {human_time(record.end-record.start)}'
            return (f'<clipPath id="{clip_id}"> <rect x="{x0}" width="{w}" y="{y0}" height="{h}" /> </clipPath>'
                    f'<rect x="{x0}" width="{w}" y="{y0}" height="{h}" '
                    f'stroke="{stroke_color}" stroke-width="1px" fill="{fill_color}">'
                    f'<title>{message}</title>'
                    '</rect>'
                    f'<text x="{x0}" y="{y0+h*0.75}" class="info" clip-path="url(#{clip_id})" fill="{text_color}">'
                    f'{message}'
                    f'<title>{message}</title>'
                    '</text>')

        print(
            '<svg version="1.1" '
            f'width="{ image_width }" height="{ image_height }" '
            'xmlns="http://www.w3.org/2000/svg">'
            '<style>'
            f'text.info {{ font-family: monospace; cursor: default; font-size: {px_vertical*0.8}px }}'
            '</style>',
            file=output_file)

        user_ids = sorted(forests.keys())
        y_offset = 0
        for i, user_id in enumerate(user_ids):
            user_id = user_ids[i]
            (recs, roots, children) = forests[user_id]

            for j, root in enumerate(roots):

                def traverse(node, parity, y):
                    rec = recs[node]
                    print(box(rec, parity, x=rec.start - start, y=y), file=output_file)
                    for k, child in enumerate(children[node]):
                        traverse(child, parity + k + 1, y + 1)

                traverse(root, j, y_offset)

            y_offset += forest_height(children) + 1

        print('</svg>', file=output_file)


if __name__ == "__main__":
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    generate_svg(input_filename, output_filename)
