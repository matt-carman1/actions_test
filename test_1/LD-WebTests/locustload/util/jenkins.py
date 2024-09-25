"""
Module/script for converting Locust raw results for Jenkins JTL results for the performance plugin.
"""
import csv
import sys

_prefixes_to_ignore = {"[poll", "[ignore]", "/livedesign/api/"}


def convert_data_to_jtl(input_file_path, output_file_path, ignore_certain_prefixes=True):
    with open(input_file_path, "r") as input_f:
        with open(output_file_path, "w") as output_f:
            input_csv = csv.DictReader(input_f)
            output_csv = csv.DictWriter(
                output_f,
                ["timeStamp", "elapsed", "label", "success", "bytes", "responseCode"],
            )
            output_csv.writeheader()
            for row in input_csv:
                name = row["name"]
                if ignore_certain_prefixes and any(
                        name[:len(prefix_to_ignore)] == prefix_to_ignore for prefix_to_ignore in _prefixes_to_ignore):
                    continue
                # NOTE(fennell): the Jenkins performance plugin is SUPER choosy about the type
                # of data the appears in the JTL file. If you put a float for elapsed, it will
                # crash, for example.
                output_csv.writerow({
                    "timeStamp": int(float(row["timestamp"])),
                    "elapsed": int(float(row["response_time"])),
                    "label": "{} ({})".format(row["name"], row["http_method"]),
                    "success": row["success"].lower(),
                    "bytes": "0",
                    "responseCode": "200",
                })


if __name__ == "__main__":
    results_prefix = sys.argv[1]
    test_prefix = sys.argv[2]
    convert_data_to_jtl(
        results_prefix + test_prefix + "_all_data.csv",
        results_prefix + "_1" + test_prefix + "_main_data.jtl",
    )
    convert_data_to_jtl(
        results_prefix + test_prefix + "_all_data.csv",
        results_prefix + "_2" + test_prefix + "_all_data.jtl",
        ignore_certain_prefixes=False,
    )
