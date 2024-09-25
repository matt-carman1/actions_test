import dataclasses
import os
import sys
from typing import List

default_compound_structure = ("\n"
                              "  Mrv1808 04222123182D          \n"
                              "\n"
                              "  0  0  0     0  0            999 V3000\n"
                              "M  V30 BEGIN CTAB\n"
                              "M  V30 COUNTS 15 16 0 0 0\n"
                              "M  V30 BEGIN ATOM\n"
                              "M  V30 1 C -4.0001 2.5818 0 0\n"
                              "M  V30 2 C -5.3336 1.8118 0 0\n"
                              "M  V30 3 C -5.3336 0.2716 0 0\n"
                              "M  V30 4 C -4.0001 -0.4984 0 0\n"
                              "M  V30 5 C -2.6664 0.2716 0 0\n"
                              "M  V30 6 C -2.6664 1.8118 0 0\n"
                              "M  V30 7 C -4.0001 4.1218 0 0\n"
                              "M  V30 8 C -1.3327 2.5818 0 0\n"
                              "M  V30 9 C -1.3327 -0.4984 0 0\n"
                              "M  V30 10 C -6.6673 -0.4984 0 0\n"
                              "M  V30 11 C -8.0009 0.2715 0 0\n"
                              "M  V30 12 C -9.3348 -0.4986 0 0\n"
                              "M  V30 13 C -9.3349 -2.0384 0 0\n"
                              "M  V30 14 C -8.0012 -2.8085 0 0\n"
                              "M  V30 15 C -6.6673 -2.0385 0 0\n"
                              "M  V30 END ATOM\n"
                              "M  V30 BEGIN BOND\n"
                              "M  V30 1 2 1 2\n"
                              "M  V30 2 1 2 3\n"
                              "M  V30 3 2 3 4\n"
                              "M  V30 4 1 4 5\n"
                              "M  V30 5 2 5 6\n"
                              "M  V30 6 1 6 1\n"
                              "M  V30 7 1 1 7\n"
                              "M  V30 8 1 6 8\n"
                              "M  V30 9 1 5 9\n"
                              "M  V30 10 2 10 11\n"
                              "M  V30 11 1 11 12\n"
                              "M  V30 12 2 12 13\n"
                              "M  V30 13 1 13 14\n"
                              "M  V30 14 2 14 15\n"
                              "M  V30 15 1 15 10\n"
                              "M  V30 16 1 3 10\n"
                              "M  V30 END BOND\n"
                              "M  V30 END CTAB\n"
                              "M  END\n")

default_scaffold = ('\n'
                    '  Mrv1908 08092119322D          \n'
                    '\n'
                    '  0  0  0     0  0            999 V3000\n'
                    'M  V30 BEGIN CTAB\n'
                    'M  V30 COUNTS 8 8 0 0 0\n'
                    'M  V30 BEGIN ATOM\n'
                    'M  V30 1 C -1.2709 1.3318 0 0\n'
                    'M  V30 2 C -2.6045 0.5618 0 0\n'
                    'M  V30 3 C -2.6045 -0.9784 0 0\n'
                    'M  V30 4 C -1.2709 -1.7484 0 0\n'
                    'M  V30 5 C 0.0628 -0.9784 0 0\n'
                    'M  V30 6 C 0.0628 0.5618 0 0\n'
                    'M  V30 7 R# -3.9382 1.3317 0 0 RGROUPS=(1 1)\n'
                    'M  V30 8 R# -3.9382 -1.7484 0 0 RGROUPS=(1 2)\n'
                    'M  V30 END ATOM\n'
                    'M  V30 BEGIN BOND\n'
                    'M  V30 1 2 1 2\n'
                    'M  V30 2 1 2 3\n'
                    'M  V30 3 2 3 4\n'
                    'M  V30 4 1 4 5\n'
                    'M  V30 5 2 5 6\n'
                    'M  V30 6 1 6 1\n'
                    'M  V30 7 1 2 7\n'
                    'M  V30 8 1 3 8\n'
                    'M  V30 END BOND\n'
                    'M  V30 END CTAB\n'
                    'M  END\n')

default_molecule_for_search_warmup = ('CRA-042755\n'
                                      '  Mrv1908 08092119202D          \n'
                                      '\n'
                                      '  0  0  0     0  0            999 V3000\n'
                                      'M  V30 BEGIN CTAB\n'
                                      'M  V30 COUNTS 21 23 0 0 0\n'
                                      'M  V30 BEGIN ATOM\n'
                                      'M  V30 1 C -1.8604 -3.7571 0 0\n'
                                      'M  V30 2 C -1.3337 -2.31 0 0\n'
                                      'M  V30 3 C -2.8503 -2.0426 0 0\n'
                                      'M  V30 4 O 0 -3.08 0 0\n'
                                      'M  V30 5 C 1.3337 -2.31 0 0\n'
                                      'M  V30 6 C 1.3337 -0.77 0 0\n'
                                      'M  V30 7 C 2.6674 -0 0 0\n'
                                      'M  V30 8 C 4.001 -0.77 0 0\n'
                                      'M  V30 9 C 4.001 -2.31 0 0\n'
                                      'M  V30 10 C 2.6674 -3.08 0 0\n'
                                      'M  V30 11 C 5.3347 -0 0 0\n'
                                      'M  V30 12 N 6.6684 0.77 0 0\n'
                                      'M  V30 13 C 0 -0 0 0\n'
                                      'M  V30 14 C -1.3337 -0.77 0 0\n'
                                      'M  V30 15 O -2.6674 0 0 0\n'
                                      'M  V30 16 N 0 1.54 0 0\n'
                                      'M  V30 17 C -1.2459 2.4452 0 0\n'
                                      'M  V30 18 C -0.77 3.9098 0 0\n'
                                      'M  V30 19 C 0.77 3.9098 0 0\n'
                                      'M  V30 20 C 1.2459 2.4452 0 0\n'
                                      'M  V30 21 O 2.7105 1.9693 0 0\n'
                                      'M  V30 END ATOM\n'
                                      'M  V30 BEGIN BOND\n'
                                      'M  V30 1 1 1 2\n'
                                      'M  V30 2 1 2 3\n'
                                      'M  V30 3 1 2 4\n'
                                      'M  V30 4 1 4 5\n'
                                      'M  V30 5 2 5 6\n'
                                      'M  V30 6 1 6 7\n'
                                      'M  V30 7 2 7 8\n'
                                      'M  V30 8 1 8 9\n'
                                      'M  V30 9 2 9 10\n'
                                      'M  V30 10 1 5 10\n'
                                      'M  V30 11 1 8 11\n'
                                      'M  V30 12 3 11 12\n'
                                      'M  V30 13 1 6 13\n'
                                      'M  V30 14 1 13 14\n'
                                      'M  V30 15 1 2 14\n'
                                      'M  V30 16 1 14 15\n'
                                      'M  V30 17 1 13 16\n'
                                      'M  V30 18 1 16 17\n'
                                      'M  V30 19 1 17 18\n'
                                      'M  V30 20 1 18 19\n'
                                      'M  V30 21 1 19 20\n'
                                      'M  V30 22 1 16 20\n'
                                      'M  V30 23 2 20 21\n'
                                      'M  V30 END BOND\n'
                                      'M  V30 END CTAB\n'
                                      'M  END\n')

default_molecule_for_substructure_search = ('\n'
                                            '  Mrv1908 08092119272D          \n'
                                            '\n'
                                            '  0  0  0     0  0            999 V3000\n'
                                            'M  V30 BEGIN CTAB\n'
                                            'M  V30 COUNTS 5 5 0 0 0\n'
                                            'M  V30 BEGIN ATOM\n'
                                            'M  V30 1 C -0.875 2.06 0 0\n'
                                            'M  V30 2 C -2.1208 1.1546 0 0\n'
                                            'M  V30 3 C -1.645 -0.31 0 0\n'
                                            'M  V30 4 C -0.105 -0.31 0 0\n'
                                            'M  V30 5 C 0.3708 1.1546 0 0\n'
                                            'M  V30 END ATOM\n'
                                            'M  V30 BEGIN BOND\n'
                                            'M  V30 1 1 1 2\n'
                                            'M  V30 2 1 1 5\n'
                                            'M  V30 3 1 2 3\n'
                                            'M  V30 4 1 3 4\n'
                                            'M  V30 5 1 4 5\n'
                                            'M  V30 END BOND\n'
                                            'M  V30 END CTAB\n'
                                            'M  END\n')

default_molecule_for_similarity_search = ('\n'
                                          '  Mrv1908 08092119292D          \n'
                                          '\n'
                                          '  0  0  0     0  0            999 V3000\n'
                                          'M  V30 BEGIN CTAB\n'
                                          'M  V30 COUNTS 6 6 0 0 0\n'
                                          'M  V30 BEGIN ATOM\n'
                                          'M  V30 1 C -0.5833 3.0183 0 0\n'
                                          'M  V30 2 C -1.8291 2.113 0 0\n'
                                          'M  V30 3 C -1.3533 0.6484 0 0\n'
                                          'M  V30 4 C 0.1867 0.6484 0 0\n'
                                          'M  V30 5 C 0.6625 2.113 0 0\n'
                                          'M  V30 6 C -0.5833 4.5583 0 0\n'
                                          'M  V30 END ATOM\n'
                                          'M  V30 BEGIN BOND\n'
                                          'M  V30 1 1 1 2\n'
                                          'M  V30 2 1 1 5\n'
                                          'M  V30 3 1 2 3\n'
                                          'M  V30 4 1 3 4\n'
                                          'M  V30 5 1 4 5\n'
                                          'M  V30 6 1 1 6\n'
                                          'M  V30 END BOND\n'
                                          'M  V30 END CTAB\n'
                                          'M  END\n')


@dataclasses.dataclass
class CommonDbProfile:
    username: str
    password: str
    project_id: str
    add_column_ids: list
    compound_id_search_query: str
    compound_id_search_num: int
    max_search_return: int
    default_wait_interval: int  # (ms)
    default_retries: int


@dataclasses.dataclass
class CoincidentDbProfile:
    coincident_live_report_title: str
    coincident_freeform_columns_name: List[str]


@dataclasses.dataclass
class BasicUserDbProfile:
    compound_structure: str
    column_id_for_subtask_sort: int
    column_id_for_subtask_remove_column: int
    column_id_for_subtask_filter: int
    scaffold: str
    scaffold_name_column: int
    new_scaffold_name: str


@dataclasses.dataclass
class BasicAdvancedSearchUserDbProfile:
    numeric_range_column: int
    numeric_range_value_low: int
    numeric_range_value_high: int
    numeric_defined_column: int
    text_exact_column: int
    text_exact_value: str
    text_defined_column: int
    expected_numeric_range_result: int
    expected_numeric_defined_result: int
    expected_text_exact_result: int
    expected_text_defined_result: int


@dataclasses.dataclass
class AdvancedUserDbProfile:
    filename_csv_import: str
    filename_3d_import: str
    compound_id_search_num: int
    compound_search_by_id_query: str
    compound_search_by_id_expected_number: int
    molecule_for_search_warmup: str
    molecule_for_substructure_search: str
    molecule_for_similarity_search: str
    quick_properties_column_ids: list
    three_d_column_id: str
    three_d_column_name: str
    compound_id_for_three_d_column: str


@dataclasses.dataclass
class ServiceResponseDbProfile:
    project_id: str


@dataclasses.dataclass
class ExecutionDbProfile:
    extra_column_ids: list
    extra_compound_queries: list


@dataclasses.dataclass
class DbProfile:
    common: CommonDbProfile
    coincident: CoincidentDbProfile
    basic: BasicUserDbProfile
    basic_adv_search: BasicAdvancedSearchUserDbProfile
    advanced: AdvancedUserDbProfile
    service_response: ServiceResponseDbProfile
    execution: ExecutionDbProfile


# Starter data DB profile

_starter_data_molecular_weight_column_id: str = "1274"
starter_data = DbProfile(
    common=CommonDbProfile(
        username=(os.getenv("LOCUST_LD_USERNAME") or "demo"),
        password=(os.getenv("LOCUST_LD_PASSWORD") or "demo"),
        project_id="1",
        add_column_ids=["1273", "1274", "1275", "1276", "1277", "1278", "1279", "1280"],
        compound_id_search_query="V045*",
        compound_id_search_num=1000,
        max_search_return=5000,
        default_wait_interval=int(os.getenv("LOCUST_DEFAULT_WAIT_INTERVAL") or "100"),  # (ms)
        default_retries=int(os.getenv("LOCUST_DEFAULT_RETRIES") or "100"),
    ),
    coincident=CoincidentDbProfile(
        coincident_live_report_title="locustLrSharedBetweenCoincidentUsers",
        coincident_freeform_columns_name=[
            "locustFfcEditedByCoincidentUsers1", "locustFfcEditedByCoincidentUsers2",
            "locustFfcEditedByCoincidentUsers3", "locustFfcEditedByCoincidentUsers4"
        ],
    ),
    basic=BasicUserDbProfile(
        compound_structure=default_compound_structure,
        column_id_for_subtask_sort=_starter_data_molecular_weight_column_id,  # Molecular weight
        column_id_for_subtask_remove_column=_starter_data_molecular_weight_column_id,  # Molecular weight
        column_id_for_subtask_filter="1227",  # All IDs
        scaffold=default_scaffold,
        scaffold_name_column="1232",  # Scaffold Name
        new_scaffold_name="Scaffold 1",
    ),
    basic_adv_search=BasicAdvancedSearchUserDbProfile(
        numeric_range_column=_starter_data_molecular_weight_column_id,  # Molecular weight
        numeric_range_value_low=50,
        numeric_range_value_high=200,
        expected_numeric_range_result=1251,
        numeric_defined_column=_starter_data_molecular_weight_column_id,  # Molecular weight
        expected_numeric_defined_result=5000,  # i.e. max
        text_exact_column="28",  # Lot Scientist
        text_exact_value="demo",
        expected_text_exact_result=5000,  # i.e. max
        text_defined_column="1273",  # Molecular formula
        expected_text_defined_result=5000,  # i.e. max
    ),
    advanced=AdvancedUserDbProfile(
        filename_csv_import="resources/import_compounds.csv",
        filename_3d_import="resources/import-3d.zip",
        compound_id_search_num=2000,
        compound_search_by_id_query="V04200*",
        compound_search_by_id_expected_number=10,
        molecule_for_search_warmup=default_molecule_for_search_warmup,
        molecule_for_substructure_search=default_molecule_for_substructure_search,
        molecule_for_similarity_search=default_molecule_for_similarity_search,
        quick_properties_column_ids=[
            "2899", "2900", "2901", "2902", "2903", "2904", "2905", "2906", "2907", "2908", "2909", "2910"
        ],
        three_d_column_id="2",
        three_d_column_name="A30",
        compound_id_for_three_d_column="CHEMBL104",
    ),
    service_response=ServiceResponseDbProfile(project_id="0",),
    execution=ExecutionDbProfile(
        # select addable_column_id, count(*) as n from ld_addable_columns_observations GROUP BY addable_column_id ORDER BY n DESC;
        extra_column_ids=["327", "813", "590", "763", "578", "809", "321", "36"],  #, "422", "569", "542", "691"],
        # select count(*) from ld_entity where ld_entity.entity_id like 'V036%';
        extra_compound_queries=[
            ["V036*", 1000],
            ["V037*", 1000],
            ["V038*", 1000],
            ["V039*", 1000],
            ["V040*", 1000],
            ["V041*", 1000],
            ["V042*", 1000],
            ["V043*", 1000],
            ["V044*", 1000],
            #["V045*", 1000],  # Skip, b/c these compounds are already added after LR creation,
            # See common.compound_id_search_query
            ["V046*", 1000],
            ["V047*", 1000],
            ["V048*", 1000],
            #["V049*", 1000],
            #["V050*", 1000],
            #["V051*", 1000],
            #["V052*", 1000],
            #["V053*", 1000],
            #["V054*", 1000],
        ],
    ),
)

_load_data_molecular_weight_column_id = "3836"
load_data = dataclasses.replace(
    starter_data,
    common=dataclasses.replace(
        starter_data.common,
        project_id="0",
        add_column_ids=[
            _load_data_molecular_weight_column_id,
            "2001",
            "1309590",
            "1309349",
            "1310978",
            "1310765",
            "1310825",
            "1310387",
            "1309295",
            "1311626",
            "1309424",
            "1311436",
            "1369028",
            "1309827",
            "1309381",
            "1310082",
            "1309279",
            "1309782",
            "1311018",
            "1310836",
            "1309796",
            "1309283",
            "1310970",
            "1309600",
            "1311174",
            "1310375",
            "1311619",
            "1309806",
            "1311691",
            "1311814",
            "1310512",
            "1310074",
            "1311202",
            "1311437",
            "1310619",
            "1311809",
            "1309989",
            "1311045",
            "1311451",
            "1309291",
            "1310752",
            "1311006",
            "1309275",
            "1310767",
            "1311784",
            "1309194",
            "1311783",
            "1310176",
            "1311391",
            "1309544",
            "1311764",
            "1309469",
            "1310472",
            "1310241",
            "1309556",
            "1311506",
            "1310650",
            "1311385",
        ],
        compound_id_search_query="V3*, V4*, V5*, V6*, V7*, V8*, V9*, CRA*, CMEMBL*",
        default_wait_interval=3 * starter_data.common.default_wait_interval,
        default_retries=2 * starter_data.common.default_retries,
    ),
    basic=dataclasses.replace(
        starter_data.basic,
        column_id_for_subtask_sort=_load_data_molecular_weight_column_id,  # Molecular Weight
        column_id_for_subtask_remove_column=_load_data_molecular_weight_column_id,  # Molecular Weight
        column_id_for_subtask_filter="2001",  # All IDs
        scaffold=default_scaffold,
        scaffold_name_column="2006",  # Scaffold Name
        new_scaffold_name="Scaffold 1",
    ),
    basic_adv_search=BasicAdvancedSearchUserDbProfile(
        numeric_range_column=_load_data_molecular_weight_column_id,  # Molecular Weight
        numeric_range_value_low=50,
        numeric_range_value_high=200,
        expected_numeric_range_result=1000,  # i.e. max
        numeric_defined_column=_load_data_molecular_weight_column_id,  # Molecular Weight
        expected_numeric_defined_result=1000,  # i.e. max
        text_exact_column="429",  # Lot Scientist
        text_exact_value="demo",
        expected_text_exact_result=1000,  # i.e. max
        text_defined_column="3835",  # Molecular Formula
        expected_text_defined_result=1000,  # i.e. max
    ),
    advanced=dataclasses.replace(
        starter_data.advanced,
        three_d_column_id="1339801",
        three_d_column_name="3D Maestro (3D)",
        compound_id_for_three_d_column="CRA-049494",
    ),
    execution=dataclasses.replace(
        starter_data.execution,
        extra_column_ids=[
            "1311506",
            "1309556",
            "1310241",
            "1311085",
            "1310971",
            "1339801",
            "1341578",
            "1347332",
            "1351339",
            "1351337",
            "1347331",
            "1309496",
            "1310064",
            "1354903",
            "1310727",
            "1310989",
            "1310345",
            "1311556",
            "1311874",
            "1310622",
            "1311258",
        ],
        # [["V150*", 1000], ["V151*", 1000], ..., ["V159*", 1000]]
        # i.e. 10 searches 1000 compounds each, 10K compounds added in total
        extra_compound_queries=[["V{}*".format(i), 1000] for i in range(150, 160)],
    ),
)

db_profiles = {"starter": starter_data, "load": load_data}

LOCUST_DB_PROFILE = os.getenv("LOCUST_DB_PROFILE")
# Default to 'starter' if the environment variable is undefined
if LOCUST_DB_PROFILE is None:
    LOCUST_DB_PROFILE = "starter"
    print("Assuming default LOCUST_DB_PROFILE={}".format(LOCUST_DB_PROFILE))

db_profile = db_profiles.get(LOCUST_DB_PROFILE)

if db_profile is None:
    print("Unknown value of LOCUST_DB_PROFILE={}. Exit.".format(LOCUST_DB_PROFILE))
    sys.exit(1)


def get() -> DbProfile:
    return db_profile
