import pytest
from helpers.api.actions import compound, row, column, livereport
from ldclient.models import Observation
from library.api.wait import wait_until_condition_met


@pytest.mark.app_defect(reason='SS-33569: flaky test')
def test_compound_link__search(ld_client, real_compound, virtual_compound):
    """
    Link two compounds, check that link is searchable, unlink, check that link is gone
    """
    compound.link_compounds(ld_client, real_compound, virtual_compound)
    compound_links = compound.search_compound_links(ld_client, [real_compound])
    assert len(compound_links) == 1
    compound.unlink_compounds(ld_client, compound_links[0].id)
    compound_links_2 = compound.search_compound_links(ld_client, [real_compound])
    assert len(compound_links_2) == 0


@pytest.mark.app_defect(reason='SS-33569: flaky test')
def test_compound_link__live_report_rows(ld_client, new_live_report, real_compound, virtual_compound):
    """
    Link two compounds in live report, check that rows are collapsed
    """

    def condition_row_count_2():
        assert_row_count_equals(ld_client, new_live_report, 2)

    def condition_row_count_1():
        assert_row_count_equals(ld_client, new_live_report, 1)

    row.add_rows_to_live_report(ld_client, new_live_report.id, [real_compound, virtual_compound])

    wait_until_condition_met(condition_row_count_2)

    compound.link_compounds(ld_client, real_compound, virtual_compound)
    wait_until_condition_met(condition_row_count_1)

    compound_links = compound.search_compound_links(ld_client, [real_compound])
    compound.unlink_compounds(ld_client, compound_links[0].id)
    wait_until_condition_met(condition_row_count_1)  # Virtual should not reappear when unlinked


REAL_COMPOUND_FFC_VALUE = "Real Compound FFC value"
VIRTUAL_COMPOUND_FFC_VALUE = "Virtual Compound FFC value"
ffc_test_cases = [
    (None, VIRTUAL_COMPOUND_FFC_VALUE, VIRTUAL_COMPOUND_FFC_VALUE),
    (REAL_COMPOUND_FFC_VALUE, None, REAL_COMPOUND_FFC_VALUE),
    (REAL_COMPOUND_FFC_VALUE, VIRTUAL_COMPOUND_FFC_VALUE, REAL_COMPOUND_FFC_VALUE),
]


@pytest.mark.app_defect(reason="SS-34767: Flaky test")
@pytest.mark.parametrize("real_compound_ffc_value, virtual_compound_ffc_value, expected_after_link", ffc_test_cases)
def test_compound_link__virtual_with_freeform_column(ld_client, new_live_report, real_compound, virtual_compound,
                                                     real_compound_ffc_value, virtual_compound_ffc_value,
                                                     expected_after_link):
    """
    Real has no FFC value but its new linked virtual does; after linking FFC appears on the real row
    """
    row.add_rows_to_live_report(ld_client, new_live_report.id, [real_compound, virtual_compound])
    freeform_column = column.create_freeform_column(ld_client, new_live_report)
    observations_to_upload = []
    if virtual_compound_ffc_value is not None:
        observations_to_upload.append(
            Observation(project_id=new_live_report.project_id,
                        addable_column_id=freeform_column.id,
                        entity_id=virtual_compound,
                        live_report_id=new_live_report.id,
                        value=virtual_compound_ffc_value))
    if real_compound_ffc_value is not None:
        observations_to_upload.append(
            Observation(project_id=new_live_report.project_id,
                        addable_column_id=freeform_column.id,
                        entity_id=real_compound,
                        live_report_id=new_live_report.id,
                        value=real_compound_ffc_value))
    column.add_freeform_values(ld_client, observations_to_upload)

    def check_prelink_ffc_values():
        prelink_lr_csv = livereport.get_live_report_as_csv(ld_client, new_live_report)
        rowlist = list(prelink_lr_csv)
        assert len(rowlist) == 2
        for lr_row in rowlist:
            all_ids = lr_row['All IDs'].split(';')
            assert not set(all_ids).isdisjoint([real_compound, virtual_compound])
            if real_compound in all_ids:
                assert lr_row[freeform_column.name] == (real_compound_ffc_value
                                                        if real_compound_ffc_value is not None else '')
            elif virtual_compound in all_ids:
                assert lr_row[freeform_column.name] == (virtual_compound_ffc_value
                                                        if virtual_compound_ffc_value is not None else '')

    wait_until_condition_met(check_prelink_ffc_values)

    compound.link_compounds(ld_client, real_compound, virtual_compound)
    # NOTE(badlato): Remove this refresh once bug SS-29442 is fixed
    livereport.refresh_live_report(ld_client, new_live_report)

    def check_real_ffc_value():
        postlink_lr_csv = livereport.get_live_report_as_csv(ld_client, new_live_report)
        rowlist = list(postlink_lr_csv)
        assert len(rowlist) == 1
        for lr_row in rowlist:
            all_ids = lr_row['All IDs'].split(';')
            assert real_compound in all_ids
            assert lr_row[freeform_column.name] == expected_after_link

    wait_until_condition_met(check_real_ffc_value)


@pytest.mark.app_defect(reason='SS-33569: flaky test')
def test_compound_link__compounds_with_assay_data(ld_client, new_live_report, real_compound, virtual_compound):
    """
    Real and new linked virtual both have assay data. After linking, the assay value appearing on the real row is
    aggregated.
    """
    assay_type_name = "undefined"
    assay_column_display_name = compound.ASSAY_NAME + " (" + assay_type_name + ")"

    row.add_rows_to_live_report(ld_client, new_live_report.id, [real_compound, virtual_compound])

    prelink_lr_csv = livereport.get_live_report_as_csv(ld_client, new_live_report)
    rowlist = list(prelink_lr_csv)
    for lr_row in rowlist:
        all_ids = lr_row['All IDs'].split(';')
        assert not set(all_ids).isdisjoint([real_compound, virtual_compound])
        if real_compound in all_ids:
            real_assay_value = lr_row.get(assay_column_display_name, None)
        elif virtual_compound in all_ids:
            virtual_assay_value = lr_row.get(assay_column_display_name, None)

    compound.link_compounds(ld_client, real_compound, virtual_compound)
    # NOTE(badlato): Remove this refresh once bug SS-29442 is fixed
    livereport.refresh_live_report(ld_client, new_live_report)

    def check_postlink_assay_data():
        postlink_lr_csv = livereport.get_live_report_as_csv(ld_client, new_live_report)
        rowlist = list(postlink_lr_csv)
        assert len(rowlist) == 1
        for postlink_lr_row in rowlist:
            all_ids = postlink_lr_row['All IDs'].split(';')
            assert real_compound in all_ids
            assert assay_column_display_name in postlink_lr_row
            assert int(
                postlink_lr_row[assay_column_display_name]) == (int(virtual_assay_value) + int(real_assay_value)) / 2

    wait_until_condition_met(check_postlink_assay_data)


@pytest.mark.skip(reason='SS-33569')
def test_compound_link__compounds_with_model_data(ld_client, new_live_report, real_compound, virtual_compound):
    """
    Real and virtual both have model results. After linking, only the virtual's model data is shown for models that are
    not column-as-parameter, clustering, or using the original structure. Other models will need to show the real data.
    """
    model = column.create_model_column(ld_client, new_live_report)
    model_column_display_name = model.name + ' (' + model.returns[0].display_name + ') [' + model.returns[0].units + ']'

    row.add_rows_to_live_report(ld_client, new_live_report.id, [real_compound, virtual_compound])

    def check_prelink_model_data():
        prelink_lr_csv = livereport.get_live_report_as_csv(ld_client, new_live_report)
        rowlist = list(prelink_lr_csv)
        assert len(rowlist) == 2
        for lr_row in rowlist:
            all_ids = lr_row['All IDs'].split(';')
            assert not set(all_ids).isdisjoint([real_compound, virtual_compound])
            assert model_column_display_name in lr_row
            if virtual_compound in all_ids:
                assert lr_row[model_column_display_name] == virtual_compound

    wait_until_condition_met(check_prelink_model_data)

    compound.link_compounds(ld_client, real_compound, virtual_compound)
    # NOTE(badlato): Remove this refresh once bug SS-29442 is fixed
    livereport.refresh_live_report(ld_client, new_live_report)

    def check_postlink_model_data():
        postlink_lr_csv = livereport.get_live_report_as_csv(ld_client, new_live_report)
        rowlist = list(postlink_lr_csv)
        assert len(rowlist) == 1
        for lr_row in rowlist:
            all_ids = lr_row['All IDs'].split(';')
            assert real_compound in all_ids
            assert model_column_display_name in lr_row
            assert lr_row[model_column_display_name] == virtual_compound

    wait_until_condition_met(check_postlink_model_data)


def assert_row_count_equals(ld_client, live_report, expected):
    rows = row.get_live_report_rows(ld_client, live_report.id)
    assert len(rows) == expected
