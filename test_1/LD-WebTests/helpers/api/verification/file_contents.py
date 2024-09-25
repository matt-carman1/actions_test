import csv
import re

from library.api.exceptions import LiveDesignAPIException

COMPOUND_STRUCTURE_COLUMN_NAME = 'Compound Structure'


def verify_csv_column_names_and_compound_ids(csv_bytes,
                                             expected_column_names,
                                             unexpected_column_names=None,
                                             expected_corporate_ids=None):
    """
    Verifies
    1. If expected corporate ids are provided, the CSV contains these ids
    2. CSV contains expected column names
    3. CSV does not contain unexpected column names
    :param csv_bytes: bytes, the exported Live Report.
    :param expected_column_names: list, expected column names in the exported csv
    :param unexpected_column_names:list, column names not expected in the exported csv
    :param expected_corporate_ids: list: expected corporate IDs in the exported csv.
    """
    csv_file = csv.DictReader(csv_bytes.decode("utf-8").splitlines())
    exported_corporate_ids = set()
    exported_column_names = set(csv_file.fieldnames)

    # Verify expected column names in the csv
    assert (set(expected_column_names).issubset(exported_column_names)), \
        "Expected these columns to be exported but they were not: {}".format(
            set(expected_column_names).difference(exported_column_names))

    # Verify unexpected column names are not present in the csv
    if unexpected_column_names:
        assert set(unexpected_column_names).isdisjoint(exported_column_names), \
            "Expected these columns not to be exported but they were: {}".format(
                set(unexpected_column_names).intersection(exported_column_names))

    # Verify expected corporate IDs in the csv
    if expected_corporate_ids:
        for row in csv_file:
            exported_corporate_ids.add(row["ID"])
        assert set(expected_corporate_ids) == exported_corporate_ids


def verify_csv_contents(csv_bytes, expected_csv_data, inexact_match_columns=[COMPOUND_STRUCTURE_COLUMN_NAME]):
    """
    Verifies csv contents which includes column and compound data

    :param csv_bytes: bytes, the exported Live Report
    :param expected_csv_data: dict, expected data for different columns in dict form
                            ex: {'Column1':['val1', 'val2'],
                                'Column2':['val1', 'val2']}
    :param inexact_match_columns: List of column names to NOT test content
        equality on. For the specified columns, we only verify that the cells are
        non-empty.
        NOTE(badlato): The intended use case here is to NOT test if Compound
         structures, etc. are scientifically valid. We leave scientific testing
         to the underlying libraries, and just verify that LD is passing
         *something* along
    """
    csv_file = csv.DictReader(csv_bytes.decode("utf-8").splitlines())
    exported_column_names = csv_file.fieldnames
    expected_columns = list(expected_csv_data.keys())
    assert expected_columns == exported_column_names, \
        "Exported column names:{}, Expected column names:{}".format(exported_column_names, expected_columns)

    # verify data of each column cell in the csv
    for column_name in expected_csv_data:
        expected_content = expected_csv_data[column_name]
        exact_match = column_name not in inexact_match_columns
        verify_csv_column_contents(csv_bytes, column_name, expected_content, exact_match=exact_match)


def verify_csv_column_contents(csv_bytes, column_name, expected_column_values, exact_match=True):
    """
    verify column values in exported livereport.

    :param csv_bytes: bytes, the exported livereport
    :param column_name: str, column name which you want to verify the values for
    :param expected_column_values: list, list of expected column values
    :param exact_match: True if cell contents should match exactly.
        False if cell contents only need to exist, but not match.
        NOTE(badlato): The intended use case here is to not test if SMILES
         strings, etc. are scientifically valid. We leave scientific testing
         to the underlying libraries, and just verify that LD is passing
         *something* along
    """
    csv_file_contents = csv.DictReader(csv_bytes.decode("utf-8").splitlines())
    actual_column_values = []

    if column_name in csv_file_contents.fieldnames:
        for row in csv_file_contents:
            actual_column_values.append(row[column_name])
    else:
        # If the specified column not there in exported livereport
        raise LiveDesignAPIException("There is no column: {} exists in Exported Livereport".format(column_name))
    if exact_match:
        assert expected_column_values == actual_column_values, \
            "Expected column values:{}, Actual column values:{} for column: {}".format(expected_column_values,
                                                                                       actual_column_values, column_name)
    else:
        assert len(expected_column_values) == len(actual_column_values)


def verify_sdf_contents(columns, expected_data, sdf_data):
    """
    Verifies sdf contents.

    :param columns: list, list of column values to verify
    :param expected_data: dict, expected Livereport data
    :param sdf_data: bytes, sdf data
    """
    # converting bytes to string
    sdf_data = sdf_data.decode("utf-8")

    # each row may have different number of columns, as empty cells are omitted after SS-40762
    exported_columns = set(re.findall("<(.*?)>", sdf_data))
    # validating whether expected columns match with actual columns
    assert exported_columns == set(columns), f'expected {columns}, got {exported_columns}'

    # verifying each column contents
    for column in columns:
        expected_column_value = expected_data.get(column)
        # Regular expression for getting values of specified column
        regexp = r"(?<=<{}>  \n)(.*?)(?=>|\$\$\$\$)".format(re.escape(column))
        actual_column_value = [value.rstrip() for value in re.findall(regexp, sdf_data, re.S)]

        # verifying column values
        assert actual_column_value == expected_column_value, "{} column value didn't match, Expected value: {}, " \
                                                             "But got:{}".format(column, expected_column_value,
                                                                                 actual_column_value)
