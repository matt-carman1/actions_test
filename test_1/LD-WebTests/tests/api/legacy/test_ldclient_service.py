# coding: utf-8
"""
This file contains *LEGACY* API tests that were moved over from LD Client's
service test suite.

A conscious decision was made *not* to invest engineering effort in cleaning these up.

Please only make changes here if you need to make a small tweak to fix a test that
breaks. If you're working on a test here, the better option is to migrate it to be a
regular API test that uses pytest and all of the goodies like fixtures. This will make
it more maintainable and extendable.
"""
import pytest

from library.api.urls import LDCLIENT_HOST
import hashlib
import json
import logging
import os
import random
import unittest
import csv

import time
from datetime import datetime
from requests.exceptions import HTTPError

from ldclient import LDClient
from ldclient.models import (AssayDefaultAggregationRule, Column, ColumnDescriptor, DataSourceAssayFolderRules,
                             FreeformColumn, FreeformColumnPicklistValue, LiveReport, Model, ModelCommand,
                             ModelRecursive, ModelReturn, ModelTemplateVar, Observation, Project, RangeColumnFilter,
                             Rationale, TextColumnFilter)

logger = logging.getLogger(__name__)


def wait_for_data_consistency(interval=100, retries=60):
    """
    Decorator to retry an assertion waiting for the lr results to be consistent

    :param interval: How often to retry, in milliseconds
    :param retries: How many times to retry
    """

    def wait_for_data_consistency_decorator(func):

        def func_wrapper(*args, **kwargs):
            count = 0
            exc = None

            while count < retries:
                try:
                    return func(*args, **kwargs)
                except AssertionError as e:
                    time.sleep(interval / 1000.0)
                    count += 1
                    exc = e
            raise exc

        return func_wrapper

    return wait_for_data_consistency_decorator


class LDClientServiceTests(unittest.TestCase):
    # test instance variables
    lr_id = None
    data_path = os.path.join(os.path.dirname(__file__), "../../../resources/legacy")
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.active_project = os.getenv('LDCLIENT_TEST_PROJECT', '4')
        cls.ldclient = LDClient(LDCLIENT_HOST, "demo", "demo", compatibility_mode=(8, 10))
        cls.rationale = Rationale(description="WSClientIntegrationTest", user_name=None)

    def tearDown(self):
        if self.lr_id:
            self.ldclient.delete_live_report(live_report_id=self.lr_id)
            logger.debug('Deleted LiveReport {}'.format(self.lr_id))

    @property
    def active_project_name(self):
        return [p.name for p in self.ldclient.projects() if p.id == self.active_project][0]

    @pytest.mark.skip
    def test_global_project_filtering(self):
        # Create connection to LiveDesign
        server_url = os.getenv('LDCLIENT_TEST_URL', 'http://localhost:9080')
        api_url = '{}/livedesign/api'.format(server_url)
        user = 'userA'
        password = 'userA'
        non_admin_ldclient = LDClient(api_url, user, password, compatibility_mode=(8, 10))

        non_admin_projects = non_admin_ldclient.projects()
        projects_w_global = non_admin_ldclient._projects_w_global()
        admin_projects = self.ldclient.projects()

        non_admin_global = [p for p in non_admin_projects if int(p.id) == 0]
        projects_w_global_match = [p for p in projects_w_global if int(p.id) == 0]
        admin_global = [p for p in admin_projects if int(p.id) == 0]

        # Because the Global Project (id=0) is filtered out for non-admin users per
        # SS-17014, self.api should see the global project but not non_admin_ldclient
        self.assertEqual(len(admin_global), 1)
        self.assertEqual(len(projects_w_global_match), 1)
        self.assertEqual(len(non_admin_global), 0)

    @pytest.mark.k8s_defect(reason='SS-37881 ConnectionError')
    def test_create_model(self):
        """
        Test the creation of a new model

        Steps:
        1) Create a new protocol
        2) Use the protocol to define a new model version
        3) Use the model version to create a new model
        """

        # Create connection to LiveDesign
        server_url = os.getenv('LDCLIENT_TEST_URL', 'http://localhost:9080')
        api_url = '{}/livedesign/api'.format(server_url)
        user = 'demo'
        password = 'demo'
        non_admin_ldclient = LDClient(api_url, user, password, compatibility_mode=(8, 10))

        # Create the protocol
        pre_command = ModelCommand(command='cp ${python file:FILE-INPUT} input.py', driver_id=1)
        command = ModelCommand(command='$SCHRODINGER/run input.py --input ${INPUT_SDFILE} > '
                               '${temp filename:TEXT-INPUT}',
                               driver_id=1)
        post_command = ModelCommand(command='cat ${temp filename:TEXT-INPUT}', driver_id=1)
        protocol_def = Model(name='Protocol test_create_model %s' % random.random(),
                             commands=[pre_command, command, post_command],
                             description='run a python file that requires the schrodinger python library',
                             archived=False,
                             published=False,
                             folder="Computational Models/User Defined/demo",
                             user="demo",
                             project_ids=['4'],
                             template_vars=[],
                             returns=[],
                             batch_size=ModelRecursive(tag='DEFAULT', value=100),
                             command_type=ModelRecursive(tag='READ_ONLY', value='NORMAL'),
                             command_queue=ModelRecursive(tag='READ_ONLY', value='sync'))

        protocol = self.ldclient.create_protocol(protocol_def)

        # Verify that the resulting protocol object is saved to the server and that the fields
        # match the original definition
        self.assertIsNotNone(protocol.id)
        for field in ['name', 'description', 'batch_size', 'command_type', 'command_queue', 'project_ids', 'folder']:
            expected = getattr(protocol_def, field)
            actual = getattr(protocol, field)
            if isinstance(expected, ModelRecursive) and isinstance(expected, ModelRecursive):
                self.assertEqual(expected.as_dict(), actual.as_dict())
                continue
            self.assertEqual(getattr(protocol_def, field), getattr(protocol, field))

        # Verify that the protocol is found when searching protocols
        # This doubles to test we include protocols on the global project
        self.assertEqual(int(protocol.id), non_admin_ldclient.get_protocol_id_by_name(protocol.name),
                         'Could not find a protocol with the expected name and id')

        # Define a model version
        # with open(, 'rb') as solubility_file:
        attachment = self.ldclient.get_or_create_attachment('{0}/solubility.py'.format(self.data_path), 'ATTACHMENT',
                                                            ['0'])
        logger.info('attachment = ' + str(attachment))
        template_vars = [
            ModelTemplateVar(name='temp filename', type='STRING', data='out.csv', tag='READ_ONLY'),
            ModelTemplateVar(name='python file', type='FILE', data=attachment['id'], tag='READ_ONLY')
        ]
        returns = [
            ModelReturn(
                key="Result",
                type="REAL",
                units="mol/L",
                precision=1,
                tag='DEFAULT',
                # The name displayed to the user in parenthesis,
                # e.g. Solubility (ph 7.4)
                display_name="pH 7.4")
        ]

        model_def = Model(name="Model test_create_model %s" % random.random(),
                          description="A fake solubility model user for "
                          "demonstrating the python api",
                          folder="Computational Models/ADME/Samples",
                          archived=False,
                          published=True,
                          user='demo',
                          returns=returns,
                          parent=protocol.id,
                          template_vars=template_vars,
                          project_ids=['4'],
                          batch_size=ModelRecursive(tag='DEFAULT', value=20),
                          command_type=ModelRecursive(tag='DEFAULT', value='NORMAL'),
                          command_queue=ModelRecursive(tag='DEFAULT', value='FAST'))

        model = self.ldclient.create_model(model_def)

        # Verify that the resulting model object is saved to the server and that the fields
        # match the original definition
        self.assertIsNotNone(model.id)
        for field in ['name', 'archived', 'folder', 'published']:
            self.assertEqual(getattr(model_def, field), getattr(model, field))

        # Verify that the model is found when searching models
        # This doubles to test we include models on the global project
        self.assertEqual(int(model.id), non_admin_ldclient.get_model_id_by_name(model.name),
                         'Could not find a model with the expected name and id')

    def get_new_live_report(self, title='integration test', project_id=None):
        live_report = LiveReport(title=title,
                                 description='some',
                                 update_policy='by_cachebuilder',
                                 default_rationale='Default rationale description',
                                 owner='demo',
                                 template=False,
                                 shared_editable=True,
                                 active=True,
                                 project_id=project_id if project_id is not None else self.active_project)
        return live_report

    def test_ping(self):
        """
        Tests contacting the /about endpoint
        """
        logger.debug('Contacting LiveDesign server')
        self.assertTrue(self.ldclient.ping())

    def test_get_subfolders(self):
        """
        Tests get_subfolders() returns proper subfolder names and data
        """
        data_file = os.path.join(self.data_path, "folder_tree_data.json")
        with open(data_file, 'r') as dataf:
            data = json.load(dataf)
        subfolders = self.ldclient.get_subfolders("Computational Models", data)
        self.assertTrue("Enzyme" in subfolders)
        enzyme_subfolders = self.ldclient.get_subfolders("Enzyme", subfolders["Enzyme"])
        self.assertTrue("Old" in enzyme_subfolders)
        old_subfolders = self.ldclient.get_subfolders("Old", enzyme_subfolders["Old"])
        self.assertTrue("Ertl PSA (Ertl PSA)" in old_subfolders)
        self.assertTrue("Glide_Gscore" in old_subfolders)
        gscore_subfolders = self.ldclient.get_subfolders("Glide_Gscore", old_subfolders["Glide_Gscore"])
        self.assertEqual(len(gscore_subfolders.keys()), 2)
        self.assertTrue("Glide_Gscore (3D)" in gscore_subfolders)
        self.assertTrue("Glide_Gscore (MaeProp)" in gscore_subfolders)

    def test_maestro_export_no_poses(self):
        """
        Tests exporting data from Maestro to LD without poses in SDF mode.
        """
        project_name = self.active_project_name
        data_file_name = os.path.join(self.data_path, "test_export_ld.sdf")
        mapping_file_name = os.path.join(self.data_path, "test_export_mapping.tsv")
        live_report_name = 'Service Test: test_maestro_export_no_poses'
        with open(data_file_name, 'rb') as f:
            sha1 = hashlib.sha1(f.read()).hexdigest()
        properties = [{"units": "", "name": "r_pdb_PDB_RESOLUTION", "endpoint": "PDBProp", "model": "PDB RES"}]
        # the model field in properties must match "model" field in the mapping file.
        task_id = self.ldclient.start_export_assay_and_pose_data(project=project_name,
                                                                 mapping_file_name=mapping_file_name,
                                                                 data_file_name=data_file_name,
                                                                 sha1=sha1,
                                                                 corporate_id_column='Corporate ID',
                                                                 live_report_name=live_report_name,
                                                                 published=True,
                                                                 properties=properties,
                                                                 export_type='SDF')
        result_url = self.ldclient.wait_and_get_result_url(task_id)
        response = self.ldclient.get_task_result(result_url)

        for compound in response['import_responses']:
            self.assertTrue(compound['success'])

    @pytest.mark.skip
    def test_load_assay_and_pose_data_no_poses(self):
        """
        Tests exporting data from Maestro to LD without poses in SDF mode
        using the new import endpoint.
        """
        project_name = self.active_project_name
        data_file_name = os.path.join(self.data_path, "test_export_ld.sdf")
        live_report_name = 'Service Test: test_maestro_export_no_poses (new endpoint)'
        with open(data_file_name, 'rb') as f:
            sha1 = hashlib.sha1(f.read()).hexdigest()
        properties = [{"units": "", "name": "r_pdb_PDB_RESOLUTION", "endpoint": "PDBProp", "model": "PDB RES"}]
        # the model field in properties must match "model" field in the mapping file.
        task_id = self.ldclient.load_assay_and_pose_data(sdf_file_name=data_file_name,
                                                         sdf_file_sha1=sha1,
                                                         mapping_file_name=None,
                                                         mapping_file_sha1=None,
                                                         three_d_file_name=None,
                                                         three_d_file_sha1=None,
                                                         project=project_name,
                                                         corporate_id_column='Corporate ID',
                                                         live_report_name=live_report_name,
                                                         published=True,
                                                         properties=properties,
                                                         export_type='SDF')
        result_url = self.ldclient.wait_and_get_result_url(task_id)
        response = self.ldclient.get_task_result(result_url)

        for compound in response['import_responses']:
            self.assertTrue(compound['success'])

    @pytest.mark.skip
    def test_load_assay_and_pose_data_with_poses(self):
        """
        Tests exporting data from Maestro to LD with poses in MAESTRO_SDF mode
        using the new import endpoint.
        """
        project_name = self.active_project_name
        sdf_file_name = os.path.join(self.data_path, "maestro_sdf_import_sdf_file.sdf")
        mapping_file_name = os.path.join(self.data_path, "maestro_sdf_import_mapping_file.tsv")
        three_d_file_name = os.path.join(self.data_path, "maestro_sdf_import_three_d_data.zip")
        live_report_name = 'Service Test: test_maestro_export_poses (new endpoint)'
        with open(sdf_file_name, 'rb') as f:
            sdf_sha1 = hashlib.sha1(f.read()).hexdigest()
        properties = [{"units": "", "name": "r_i_glide_gscore", "endpoint": "glide gscore", "model": "sF_Sum"}]
        task_id = self.ldclient.load_assay_and_pose_data(sdf_file_name=sdf_file_name,
                                                         sdf_file_sha1=sdf_sha1,
                                                         mapping_file_name=mapping_file_name,
                                                         mapping_file_sha1=None,
                                                         three_d_file_name=three_d_file_name,
                                                         three_d_file_sha1=None,
                                                         project=project_name,
                                                         corporate_id_column='Corporate ID',
                                                         live_report_name=live_report_name,
                                                         published=True,
                                                         properties=properties,
                                                         export_type='MAESTRO_SDF')
        result_url = self.ldclient.wait_and_get_result_url(task_id)
        response = self.ldclient.get_task_result(result_url)

        self.lr_id = response['live_report_id']
        print(response)
        for compound in response['import_responses']:
            self.assertTrue(compound['success'])
            self.assertEqual(compound['observations_imported'], 1)

    def test_maestro_registration(self):
        project_name = self.active_project_name
        with open('{0}/registration.sd'.format(self.data_path), 'rb') as f:
            response = self.ldclient.register_compounds_sdf(project_name, f.read(), 'test')
        self.assertEqual(len(response), 4)
        self.assertTrue(all([compound['success'] for compound in response]))

    def test_create_live_report(self):
        logger.debug('Test creating a Live Report')
        live_report = self.get_new_live_report(title='integration test: test_create_live_report')
        response = self.ldclient.create_live_report(live_report)
        self.lr_id = int(response.id)
        self.assertEqual(response.title, 'integration test: test_create_live_report')

    @pytest.mark.skip(reason="Skipping as this test was already covered by other test.")
    def test_execute_live_report(self):
        live_report = self.get_new_live_report(title='integration test: test_execute_live_report')
        lr = self.ldclient.create_live_report(live_report)
        # the following call blocks until we get a valid LR results from the server
        self.ldclient.execute_live_report(lr.id)

        metadata = self.ldclient.live_report_results_metadata(lr.id)
        self.assertNotEqual(metadata['version'], 0)

    def test_assays(self):
        logger.debug('Test retrieving all assays from Api.assays():')
        response = self.ldclient.assays()
        assert (len(response) > 10)

        logger.debug('Test retrieving retrieving assays and specifying database and project')
        response = self.ldclient.assays(database_name='pri', project_ids=[0])
        assert (len(response) > 10)

        logger.debug('Test projects specified as csv')
        response = self.ldclient.assays(project_ids='0,1')
        assert (len(response) > 10)

        logger.debug('Test retrieving assay by name:')

        # get an assay name from all assays first
        response = self.ldclient.assays(database_name='pri')
        assay_name = response[0].name
        response = self.ldclient.assay(assay_name=assay_name)
        self.assertEqual(response.name, assay_name)
        logger.debug('Test a RuntimeError is received on a dud assay request')
        with self.assertRaises(RuntimeError):
            self.ldclient.assay('fake_assay')

    def test_load_compounds_from_sdf(self):
        lr_def = self.get_new_live_report(title='Service test: test_load_compounds_from_sdf')
        live_report = self.ldclient.create_live_report(lr_def)
        self.lr_id = live_report.id
        resp = self.ldclient.load_sdf(live_report.id, '{0}/load_sdf.sdf'.format(self.data_path))

        @wait_for_data_consistency()
        def test(lr):
            live_report_additional_rows = self.ldclient.live_report_rows(lr.id)
            for compound in resp:
                self.assertIn(compound['corporate_id'], live_report_additional_rows)

        test(live_report)

    def test_column_descriptor(self):
        live_report = self.get_new_live_report(title='service test: test_column_descriptor')
        live_report = self.ldclient.create_live_report(live_report)
        self.lr_id = live_report.id

        column_descriptor = self.ldclient.column_descriptors(live_report.id)[0]
        column_descriptor.width = 1000

        self.ldclient.add_column_descriptor(live_report.id, column_descriptor)

        @wait_for_data_consistency()
        def test():
            updated_column_descriptor_by_name = self.ldclient.column_descriptors(live_report.id,
                                                                                 column_descriptor.column_id)[0]
            self.assertEqual(column_descriptor.width, updated_column_descriptor_by_name.width)

        test()

        second_column_descriptor = ColumnDescriptor('Compound Structure Date')
        second_column_descriptor.addable_column_id = 1275
        self.ldclient.add_column_descriptor(live_report.id, second_column_descriptor)

        @wait_for_data_consistency()
        def test(lr, column_id, addable_column_id):
            new_column_descriptor = self.ldclient.column_descriptors(lr.id, column_id)[0]
            print(new_column_descriptor)
            self.assertEqual(new_column_descriptor.live_report_id, lr.id)
            self.assertEqual(new_column_descriptor.display_name, 'Compound Structure Date')

        test(live_report, second_column_descriptor.column_id, second_column_descriptor.addable_column_id)

        def test(lr, addable_column_id):
            column_descriptor_by_addable_column_id = self.ldclient.column_descriptor(lr.id, addable_column_id)
            self.assertEqual(column_descriptor_by_addable_column_id.live_report_id, lr.id)
            self.assertEqual(column_descriptor_by_addable_column_id.display_name, 'Compound Structure Date')

        test(live_report, second_column_descriptor.addable_column_id)

    def test_column_filters(self):
        live_report = self.get_new_live_report(title='service test: test_column_filters')
        live_report = self.ldclient.create_live_report(live_report)
        self.lr_id = live_report.id
        ID_COLUMN_ADDABLE_COLUMN_ID = 1226
        LOT_NUMBER_ADDABLE_COLUMN_ID = 1281
        COMPOUND_STRUCTURE_DATE_ADDABLE_COLUMN_ID = 1275
        self.ldclient.add_columns(
            live_report.id,
            [ID_COLUMN_ADDABLE_COLUMN_ID, LOT_NUMBER_ADDABLE_COLUMN_ID, COMPOUND_STRUCTURE_DATE_ADDABLE_COLUMN_ID])

        # Confirm there are zero filters
        @wait_for_data_consistency()
        def test(lr):
            current_filters = self.ldclient.column_filters(lr.id)
            self.assertEqual(len(current_filters), 0)

        test(live_report)

        # Add single filter (text)
        text_filter = TextColumnFilter(value='V12345', addable_column_id=ID_COLUMN_ADDABLE_COLUMN_ID)
        self.ldclient.set_column_filter(live_report.id, text_filter)

        @wait_for_data_consistency()
        def test(lr, addable_column_id):
            current_filters = self.ldclient.column_filters(lr.id)
            self.assertEqual(len(current_filters), 1)
            specific_filter = self.ldclient.column_filter(lr.id, addable_column_id)
            self.assertEqual(specific_filter.filter_type, 'text')
            self.assertEqual(specific_filter.text_match_type, 'exactly')
            self.assertEqual(specific_filter.value, 'V12345')
            self.assertEqual(str(specific_filter.addable_column_id), str(addable_column_id))

        test(live_report, text_filter.addable_column_id)

        # Test updating a filter
        text_filter.value = 'V23456'
        self.ldclient.set_column_filter(live_report.id, text_filter)

        @wait_for_data_consistency()
        def test(lr, addable_column_id):
            current_filters = self.ldclient.column_filters(lr.id)
            self.assertEqual(len(current_filters), 1)
            specific_filter = self.ldclient.column_filter(lr.id, addable_column_id)
            self.assertEqual(specific_filter.filter_type, 'text')
            self.assertEqual(specific_filter.text_match_type, 'exactly')
            self.assertEqual(specific_filter.value, 'V23456')
            self.assertEqual(str(specific_filter.addable_column_id), str(addable_column_id))

        test(live_report, text_filter.addable_column_id)

        # Test adding a single filter (range)
        range_filter = RangeColumnFilter(range_low=1, range_high=5, addable_column_id=LOT_NUMBER_ADDABLE_COLUMN_ID)
        self.ldclient.set_column_filter(live_report.id, range_filter)

        @wait_for_data_consistency()
        def test(lr, addable_column_id):
            current_filters = self.ldclient.column_filters(lr.id)
            self.assertEqual(len(current_filters), 2)
            specific_filter = self.ldclient.column_filter(lr.id, addable_column_id)
            self.assertEqual(specific_filter.filter_type, 'range')
            self.assertEqual(specific_filter.range_low, 1)
            self.assertEqual(specific_filter.range_high, 5)
            self.assertEqual(str(specific_filter.addable_column_id), str(addable_column_id))

        test(live_report, range_filter.addable_column_id)

        # Test adding a date range filter
        date_range_filter = RangeColumnFilter(date=True,
                                              range_low=1497300362834,
                                              range_high=1547767385469,
                                              addable_column_id=COMPOUND_STRUCTURE_DATE_ADDABLE_COLUMN_ID)
        self.ldclient.set_column_filter(live_report.id, date_range_filter)

        @wait_for_data_consistency()
        def test(lr, addable_column_id):
            current_filters = self.ldclient.column_filters(lr.id)
            self.assertEqual(len(current_filters), 3)
            specific_filter = self.ldclient.column_filter(lr.id, addable_column_id)
            self.assertEqual(specific_filter.filter_type, 'range')
            self.assertEqual(specific_filter.date, True)
            self.assertEqual(specific_filter.range_low, 1497300362834)
            self.assertEqual(specific_filter.range_high, 1547767385469)
            self.assertEqual(str(specific_filter.addable_column_id), str(addable_column_id))

        test(live_report, date_range_filter.addable_column_id)

        # Remove a filter
        self.ldclient.remove_column_filter(live_report.id, LOT_NUMBER_ADDABLE_COLUMN_ID)

        @wait_for_data_consistency()
        def test(lr, absent_addable_column_id):
            current_filters = self.ldclient.column_filters(lr.id)
            self.assertEqual(len(current_filters), 2)
            for filt in current_filters:
                self.assertNotEqual(str(filt.addable_column_id), str(absent_addable_column_id))

        test(live_report, LOT_NUMBER_ADDABLE_COLUMN_ID)

        # Test removing all filters
        self.ldclient.remove_all_column_filters(live_report.id)

        @wait_for_data_consistency()
        def test(lr):
            current_filters = self.ldclient.column_filters(lr.id)
            self.assertEqual(len(current_filters), 0)

        test(live_report)

    def test_register_compounds_via_csv(self):
        project_name = self.active_project_name
        live_report = self.get_new_live_report(title='Service Test: register_compounds_via_csv')
        live_report = self.ldclient.create_live_report(live_report)
        self.lr_id = live_report.id

        with open('{0}/registration.csv'.format(self.data_path), 'rb') as f:
            csvdata = f.read()

        response = self.ldclient.register_compounds_via_csv(project_name,
                                                            csvdata,
                                                            column_identifier='input_smiles',
                                                            compound_identifier_type='CSV_SMILES',
                                                            file_name='test_import_assay.csv',
                                                            published=False,
                                                            import_assay_data=True,
                                                            live_report_id=live_report.id)
        self.assertEqual(len(response), 2)

    def test_create_attachment(self):
        data_file_name = '{0}/ligand0.pse'.format(self.data_path)

        response = self.ldclient.get_or_create_attachment(attachment_file_name=data_file_name,
                                                          file_type="THREE_D",
                                                          project_ids=["0", "1", "2"])
        self.assertGreater(len(response), 0)
        self.assertEqual(response['file_name'], data_file_name)
        self.assertFalse(response['id'] is None)

        get_response = self.ldclient.get_attachment(alternate_id=response['id'])
        self.assertIsInstance(get_response, bytes)

    def test_infer_shared_file_type_from_attachments_1(self):
        attachment_id_1 = self._create_and_persist_attachment("ligand0.pse")
        ext = self.ldclient._infer_shared_file_type_from_attachments([attachment_id_1])
        self.assertEqual(ext, "pse")

    def test_infer_shared_file_type_from_attachments_2(self):
        attachment_id_1 = self._create_and_persist_attachment("ligand0.pse")
        attachment_id_2 = self._create_and_persist_attachment("ligand2.mae")
        ext = self.ldclient._infer_shared_file_type_from_attachments([attachment_id_1, attachment_id_2])
        self.assertEqual(ext, None)

    def test_infer_shared_file_type_from_attachments_3(self):
        attachment_id_1 = self._create_and_persist_attachment("ligand0.pse")
        attachment_id_2 = self._create_and_persist_attachment("ligand1")
        ext = self.ldclient._infer_shared_file_type_from_attachments([attachment_id_1, attachment_id_2])
        self.assertEqual(ext, "pse")

    def _create_and_persist_attachment(self, file_name):
        data_file_name = '{0}/{1}'.format(self.data_path, file_name)
        response = self.ldclient.get_or_create_attachment(attachment_file_name=data_file_name,
                                                          file_type="THREE_D",
                                                          project_ids=["0", "1", "2"],
                                                          remote_file_name=file_name)
        return response['id']

    def test_update_columns(self):
        project_ids = [0]
        assays = self.ldclient.assays(database_name='pri', project_ids=project_ids)
        assay_column_to_update = assays[0].types[0]
        # create column to be updated from assay
        columns = [
            Column(id=assay_column_to_update.addable_column_id,
                   name=assay_column_to_update.name,
                   column_type='assay',
                   value_type=assay_column_to_update.value_type,
                   log_scale='false',
                   project_ids=project_ids,
                   folder_name='experimental_assays')
        ]
        response = self.ldclient.update_columns(columns)
        print(response)
        self.assertEqual(response[0]['folder_name'], 'experimental_assays')

    def test_add_remove_rows(self):
        live_report = self.get_new_live_report(title='Service test: test_update_live_report')
        live_report.additional_rows = ["CRA-031925"]

        live_report = self.ldclient.create_live_report(live_report)
        rows = ["CRA-031137", "CRA-031437"]
        additional_rows = self.ldclient.add_rows(live_report.id, rows)
        self.assertIn(rows[0], additional_rows)
        self.assertIn(rows[1], additional_rows)
        additional_rows = self.ldclient.remove_rows(live_report.id, rows)
        self.assertNotIn(rows[0], additional_rows)
        self.assertNotIn(rows[1], additional_rows)

    @pytest.mark.skip
    def test_create_folders(self):
        folder_name = "LR folder" + str(datetime.now())
        folder = self.ldclient.create_folder(folder_name, "5")
        self.assertNotEqual(folder.id, 0)
        self.assertEqual(folder.name, folder_name)
        self.assertEqual(folder.project_id, '5')

    @pytest.mark.skip
    def test_list_folders(self):
        folder1 = self.ldclient.create_folder("LR folder" + str(datetime.now()), "5")
        folders_in_project1 = self.ldclient.list_folders(project_ids="1")
        self.assertNotIn(folder1.project_id, {f.project_id for f in folders_in_project1})

        folders_in_project5 = self.ldclient.list_folders(project_ids="5")
        folder_ids = {f.id for f in folders_in_project5}
        self.assertIn(folder1.id, folder_ids)
        self.assertEqual({f.project_id for f in folders_in_project5}, {'5'})

    def test_database_columns(self):
        response = self.ldclient.database_columns()
        self.assertTrue(len(response) > 10)

        folder_path = "folderA/folderB"
        database_column_1 = response[0]
        database_column_1.folder_path = folder_path
        update_response = self.ldclient.update_database_column(database_column_1)

        self.assertIsNotNone(update_response)
        self.assertEqual(folder_path, update_response.folder_path)

        empty_folder_path = ""

        database_column_1 = update_response
        database_column_1.folder_path = empty_folder_path
        update_response_2 = self.ldclient.update_database_column(database_column_1)

        self.assertIsNotNone(update_response_2)
        self.assertEqual(empty_folder_path, update_response_2.folder_path)

    def test_freeform_columns(self):
        live_report = self.get_new_live_report(title='service test: test_freeform_columns')
        live_report = self.ldclient.create_live_report(live_report)
        self.lr_id = live_report.id

        freeform_columns = self.ldclient.freeform_columns('0')

        self.assertIsNotNone(freeform_columns)

    def test_add_then_get_freeform_column_by_id(self):
        live_report = self.get_new_live_report(title='service test: test_add_freeform_column')
        live_report = self.ldclient.create_live_report(live_report)
        self.lr_id = live_report.id

        freeform_column = self.ldclient.create_freeform_column(
            FreeformColumn(
                name='An FFC',
                type=FreeformColumn.COLUMN_TEXT,
                description='I am a freeform column',
                project_id=live_report.project_id,
                live_report_id=self.lr_id,
                published=True,
            ))

        same_freeform_column = self.ldclient.get_freeform_column_by_id(freeform_column.id)

        self.assertEqual(freeform_column.name, same_freeform_column.name)

    def test_add_freeform_column_to_live_report(self):
        live_report = self.get_new_live_report(title='service test: test_add_freeform_column')
        live_report = self.ldclient.create_live_report(live_report)
        self.lr_id = live_report.id

        freeform_column = self.ldclient.create_freeform_column(
            FreeformColumn(
                name='An FFC',
                type=FreeformColumn.COLUMN_TEXT,
                description='I am a freeform column',
                project_id=live_report.project_id,
                live_report_id=self.lr_id,
                published=True,
            ))

        self.assertIsNotNone(freeform_column.id, 'FFC should have an ID')

    def test_add_freeform_column_with_picklist_to_live_report(self):
        live_report = self.get_new_live_report(title='service test: test_add_freeform_column')
        live_report = self.ldclient.create_live_report(live_report)
        self.lr_id = live_report.id

        freeform_column = self.ldclient.create_freeform_column(
            FreeformColumn(name='An FFC',
                           type=FreeformColumn.COLUMN_TEXT,
                           description='I am a freeform column',
                           project_id=live_report.project_id,
                           live_report_id=self.lr_id,
                           published=True,
                           picklist=True,
                           values=(
                               'foo',
                               'bar',
                           )))

        self.assertIsNotNone(freeform_column.id, 'FFC should have an ID')
        self.assertEqual(type(freeform_column), FreeformColumn)
        self.assertEqual(type(freeform_column.values[0]), FreeformColumnPicklistValue)

    def test_create_observations(self):
        live_report = self.get_new_live_report(title='service test: test_set_ffc_value_batch')
        live_report = self.ldclient.create_live_report(live_report)
        self.lr_id = live_report.id

        first_data_file_name = '{0}/ligand0.pse'.format(self.data_path)

        first_file = self.ldclient.get_or_create_attachment(attachment_file_name=first_data_file_name,
                                                            file_type="THREE_D",
                                                            project_ids=[live_report.project_id])

        second_data_file_name = '{0}/snowman.jpg'.format(self.data_path)

        second_file = self.ldclient.get_or_create_attachment(attachment_file_name=second_data_file_name,
                                                             file_type="IMAGE",
                                                             project_ids=[live_report.project_id])

        freeform_column = self.ldclient.create_freeform_column(
            FreeformColumn(
                name='An FFC',
                type=FreeformColumn.COLUMN_ATTACHMENT,
                description='I am a freeform column for attachments',
                project_id=live_report.project_id,
                live_report_id=live_report.id,
                published=True,
            ))

        observations_to_upload = (
            Observation(project_id=live_report.project_id,
                        addable_column_id=freeform_column.id,
                        entity_id='CRA-032662',
                        live_report_id=live_report.id,
                        value=first_file.get('id')),
            Observation(project_id=live_report.project_id,
                        addable_column_id=freeform_column.id,
                        entity_id='CRA-032664',
                        live_report_id=live_report.id,
                        value=second_file.get('id')),
        )

        observations = self.ldclient.add_freeform_column_values(observations_to_upload)
        sorted_observations = sorted(observations, key=lambda observation: observation.entity_id)
        self.assertEqual(len(observations), 2)
        self.assertIsNotNone(observations[0].id)
        self.assertIsNotNone(observations[1].id)
        self.assertSequenceEqual(sorted_observations[0].value, observations_to_upload[0].value)
        self.assertSequenceEqual(sorted_observations[1].value, observations_to_upload[1].value)

    def test_observations(self):
        live_report = self.get_new_live_report(title='service test: test_set_ffc_value_batch')
        live_report = self.ldclient.create_live_report(live_report)
        self.lr_id = live_report.id

        first_data_file_name = '{0}/ligand0.pse'.format(self.data_path)

        first_file = self.ldclient.get_or_create_attachment(attachment_file_name=first_data_file_name,
                                                            file_type="THREE_D",
                                                            project_ids=[live_report.project_id])

        second_data_file_name = '{0}/snowman.jpg'.format(self.data_path)

        second_file = self.ldclient.get_or_create_attachment(attachment_file_name=second_data_file_name,
                                                             file_type="IMAGE",
                                                             project_ids=[live_report.project_id])

        freeform_column = self.ldclient.create_freeform_column(
            FreeformColumn(
                name='An FFC',
                type=FreeformColumn.COLUMN_ATTACHMENT,
                description='I am a freeform column for attachments',
                project_id=live_report.project_id,
                live_report_id=live_report.id,
                published=True,
            ))

        observations_to_upload = (
            Observation(project_id=live_report.project_id,
                        addable_column_id=freeform_column.id,
                        entity_id='CRA-032662',
                        live_report_id=live_report.id,
                        value=first_file.get('id')),
            Observation(project_id=live_report.project_id,
                        addable_column_id=freeform_column.id,
                        entity_id='CRA-032664',
                        live_report_id=live_report.id,
                        value=second_file.get('id')),
        )

        uploaded_observations = self.ldclient.add_freeform_column_values(observations_to_upload)

        observations = self.ldclient.get_observations_by_entity_ids_and_column_ids(
            project_id=live_report.project_id,
            addable_column_ids=[freeform_column.id],
            entity_ids=('CRA-032662', 'CRA-032664'))
        sorted_observations = sorted(observations, key=lambda observation: observation.id)
        sorted_uploaded_observations = sorted(uploaded_observations, key=lambda observation: observation.id)

        self.assertEqual(len(observations), 2)
        self.assertSequenceEqual(sorted_observations[0].id, sorted_uploaded_observations[0].id)
        self.assertSequenceEqual(sorted_observations[1].id, sorted_uploaded_observations[1].id)
        self.assertSequenceEqual(sorted_observations[0].value, sorted_uploaded_observations[0].value)
        self.assertSequenceEqual(sorted_observations[1].value, sorted_uploaded_observations[1].value)

    def test_create_project(self):
        prefix = "A Test Add Project"
        project = self._create_unique_project(prefix)
        self.assertTrue(project is not None)
        self.assertIn(prefix, project.name)

    def _create_unique_project(self, prefix_name):
        project_name = prefix_name + " " + str(time.time())
        project_dict = {
            "name": project_name,
            "description": "project created just for testing",
            "alternate_id": project_name,
            "restricted": True
        }
        project = Project.from_dict(project_dict)
        return self.ldclient.create_or_update_project(project)

    def test_create_assay(self):
        response = self.ldclient.get_or_create_assay(assay_name="test_assay",
                                                     assay_type_name="3D",
                                                     column_type="THREE_D",
                                                     project_ids=["0", "1", "2"])
        self.assertGreater(len(response), 0)
        self.assertEqual(response['assay_name'], "test_assay")
        self.assertFalse(response['addable_column_id'] is None)

    @pytest.mark.app_defect(
        reason="SS-29145: 400 http error when test executes create_or_update_data_source_assay_folder_rules()")
    def test_create_or_update_data_source_assay_folder_rules(self):
        rules = [{
            "id": None,
            "match_type": "STRING",
            "comparison_type": "STARTS_WITH",
            "match_operand": "Rat",
            "folder": "PK/Rat"
        }, {
            "id": None,
            "match_type": "STRING",
            "comparison_type": "STARTS_WITH",
            "match_operand": "Mouse",
            "folder": "PK/Mouse"
        }]
        data_source_id = "1"
        data_source_assay_folder_rules = {"id": None, "data_source_id": data_source_id, "rules": rules}
        existing_data_source_assay_folder_rules = self.ldclient.data_source_assay_folder_rules_search(data_source_id)
        if existing_data_source_assay_folder_rules is not None:
            data_source_assay_folder_rules['id'] = existing_data_source_assay_folder_rules.id
        response = self.ldclient.create_or_update_data_source_assay_folder_rules(
            DataSourceAssayFolderRules.from_dict(data_source_assay_folder_rules))
        self.assertTrue(response is not None)
        self.assertTrue(response.id is not None)
        self.assertEqual(data_source_id, response.data_source_id)
        for rule in rules:
            del rule['id']
        for rule in response.rules:
            del rule['id']
        self.assertEqual(rules, response.rules)

    @pytest.mark.app_defect(
        reason="SS-29145: 400 http error when test executes create_or_update_data_source_assay_folder_rules()")
    def test_data_source_assay_folder_rules_search(self):
        rules = [{
            "id": None,
            "match_type": "STRING",
            "comparison_type": "STARTS_WITH",
            "match_operand": "Rat",
            "folder": "PK/Rat"
        }, {
            "id": None,
            "match_type": "STRING",
            "comparison_type": "STARTS_WITH",
            "match_operand": "Mouse",
            "folder": "PK/Mouse"
        }]
        data_source_id = "3"
        data_source_assay_folder_rules = {"id": None, "data_source_id": data_source_id, "rules": rules}
        existing_data_source_assay_folder_rules = self.ldclient.data_source_assay_folder_rules_search(data_source_id)
        if existing_data_source_assay_folder_rules is not None:
            data_source_assay_folder_rules['id'] = existing_data_source_assay_folder_rules.id
        data_source_assay_folder_rules_created = self.ldclient.create_or_update_data_source_assay_folder_rules(
            DataSourceAssayFolderRules.from_dict(data_source_assay_folder_rules))
        data_source_assay_folder_rules_retrieved = self.ldclient.data_source_assay_folder_rules_search(data_source_id)
        self.assertTrue(data_source_assay_folder_rules_retrieved is not None)
        self.assertTrue(data_source_assay_folder_rules_retrieved.id is not None)
        self.assertEqual(data_source_assay_folder_rules_retrieved.data_source_id,
                         data_source_assay_folder_rules_retrieved.data_source_id)
        self.assertEqual(data_source_assay_folder_rules_created.rules, data_source_assay_folder_rules_retrieved.rules)

    @pytest.mark.skip(reason="QA-4476: Update compound search related unit tests as py.test")
    def test_stereoagnostic_compound_search(self):
        """
        Test exact compound search w/ and w/o ignoring stereo information.
        """
        lr_def = self.get_new_live_report(title='Service test: compound search ignoring stereochemistry')
        live_report = self.ldclient.create_live_report(lr_def)
        self.lr_id = live_report.id
        compounds = self.ldclient.load_sdf(live_report.id,
                                           '{0}/stereo_reals.sdf'.format(self.data_path),
                                           compound_source="non_pri")
        self.assertEqual(len(compounds), 4)
        compounds = self.ldclient.load_sdf(live_report.id,
                                           '{0}/stereo_virtuals.sdf'.format(self.data_path),
                                           compound_source="pri")
        self.assertEqual(len(compounds), 2)
        virtual_ids = [compound['corporate_id'] for compound in compounds]
        molecule = "CN[C@H]1CCNC[C@H]1OC"
        # Search molecule ignoring its stereo information.
        matching_ids = self.ldclient.compound_search(molecule=molecule, ignore_stereospecific=True)
        self.assertEqual(set(['SCHRO55827', virtual_ids[0], virtual_ids[1], 'SCHRO55825', 'SCHRO55826', 'SCHRO55824']),
                         set(matching_ids))
        # Search molecule considering its stereo information.
        matching_ids = self.ldclient.compound_search(molecule=molecule, ignore_stereospecific=False)
        self.assertEqual([virtual_ids[1]], matching_ids)

    @pytest.mark.skip(reason="QA-4560: API test for compound link service")
    def test_compounds_linkservice(self):
        """
        Test compound link service APIs:
        1. Compounds linking.
        2. Search for compounds link.
        3. Search for compounds unlinking.
        """
        lr_def = self.get_new_live_report(title='Service test: compound linking service test')
        live_report = self.ldclient.create_live_report(lr_def)
        self.lr_id = live_report.id
        compounds = self.ldclient.load_sdf(live_report.id,
                                           '{0}/stereo_1real.sdf'.format(self.data_path),
                                           compound_source="non_pri")
        self.assertEqual(len(compounds), 1)
        real_entity_id = compounds[0]['corporate_id']
        compounds = self.ldclient.load_sdf(live_report.id,
                                           '{0}/stereo_1virtual.sdf'.format(self.data_path),
                                           compound_source="pri")
        self.assertEqual(len(compounds), 1)
        virtual_entity_id = compounds[0]['corporate_id']
        # There should not be any link present as of now.
        find_link_obsv = self.ldclient.get_compound_links_by_real_entity_ids([real_entity_id])
        # In case if there is any existing link, lets remove it, so we start with clean state.
        for obsv in find_link_obsv:
            self.ldclient.delete_compound_link(obsv.id)
        link_obsv = self.ldclient.create_compound_link(real_entity_id=real_entity_id,
                                                       virtual_entity_id=virtual_entity_id)
        # Link should have created now.
        self.assertEqual(link_obsv.real_entity_id, real_entity_id)
        self.assertEqual(link_obsv.virtual_entity_id, virtual_entity_id)
        self.assertNotEqual(link_obsv.id, None)
        # Search should return valid link.
        find_link_obsv = self.ldclient.get_compound_links_by_real_entity_ids([real_entity_id])
        self.assertEqual(len(find_link_obsv), 1)
        self.assertEqual(find_link_obsv[0].real_entity_id, real_entity_id)
        self.assertEqual(find_link_obsv[0].virtual_entity_id, virtual_entity_id)
        # Remove compounds link.
        self.ldclient.delete_compound_link(link_obsv.id)
        # Search should return no link.
        find_link_obsv = self.ldclient.get_compound_links_by_real_entity_ids([real_entity_id])
        self.assertEqual(find_link_obsv, [])

    @pytest.mark.skip(reason='QA-4478')
    def test_list_users(self):
        users = self.ldclient.list_users(include_permissions=True)
        self.assertTrue(type(users), 'list')
        self.assertGreater(len(users), 0)
        self.assertIn('username', users[0])
        self.assertIn('id', users[0])
        self.assertIn('can_use_admin_panel', users[0])
        self.assertIn('can_build_protocols', users[0])
        self.assertIn('is_admin', users[0])

        users = self.ldclient.list_users(include_permissions=False)
        self.assertTrue(type(users), 'list')
        self.assertGreater(len(users), 0)
        self.assertIn('username', users[0])
        self.assertIn('id', users[0])
        # verify that user permissions aren't included in the response since include_permissions is false
        self.assertNotIn('can_use_admin_panel', users[0])
        self.assertNotIn('can_build_protocols', users[0])
        self.assertNotIn('is_admin', users[0])

        # a non-admin user shouldn't be able to access the list users end point
        server_url = os.getenv('LDCLIENT_TEST_URL', 'http://localhost:9080')
        api_url = '{}/livedesign/api'.format(server_url)
        non_admin_ldclient = LDClient(api_url, 'userB', 'userB', compatibility_mode=(8, 10))
        try:
            non_admin_ldclient.list_users()
        except Exception as e:
            # should raise a Forbidden Error
            self.assertEqual(e.response.status_code, 403)
            pass

    @pytest.mark.skip(reason='QA-4478')
    def test_current_user(self):
        user = self.ldclient.get_privileges()
        self.assertTrue(type(user), 'dict')
        self.assertIn('username', user)
        self.assertIn('id', user)
        self.assertIn('can_use_admin_panel', user)
        self.assertIn('can_build_protocols', user)
        self.assertIn('is_admin', user)
        self.assertIn('can_use_admin_panel', user)
        self.assertIn('can_build_protocols', user)
        self.assertIn('is_admin', user)

    @pytest.mark.skip(reason='QA-4478')
    def test_get_user(self):
        user = self.ldclient.get_user("demo")
        self.assertTrue(type(user), 'dict')
        self.assertIn('username', user)
        self.assertIn('id', user)

    @pytest.mark.skip(reason='QA-4478')
    def test_list_memberships(self):
        memberships = self.ldclient.list_memberships()
        self.assertTrue(type(memberships), 'list')
        self.assertGreater(len(memberships), 0)
        self.assertIn('group_id', memberships[0])
        self.assertIn('user_id', memberships[0])
        self.assertIn('id', memberships[0])

    @pytest.mark.skip(reason='QA-4478')
    def test_list_permissions(self):
        permissions = self.ldclient.list_permissions()
        self.assertTrue(type(permissions), 'list')
        self.assertGreater(len(permissions), 0)
        self.assertIn('project_id', permissions[0])
        self.assertIn('group_id', permissions[0])

    @wait_for_data_consistency()
    def assert_row_count(self, live_report_id, row_count):
        inserted_row_count = len(self.ldclient.live_report_rows(live_report_id))
        self.assertEqual(row_count, inserted_row_count)

    @wait_for_data_consistency()
    def assert_compound_ids(self, live_report_id, expected_ids):
        inserted_rows = self.ldclient.live_report_rows(live_report_id)
        for compound in expected_ids:
            self.assertIn(compound, inserted_rows)

    @wait_for_data_consistency()
    def assert_compound_structures(self, live_report_id, expected_structures):
        inserted_rows = self.ldclient.live_report_rows(live_report_id)
        for compound in expected_structures:
            self.assertIn(compound, inserted_rows)

    @wait_for_data_consistency()
    def assert_columns_added(self, live_report_id, expected_headers):
        column_descriptors = self.ldclient.column_descriptors(live_report_id)
        actual_headers = [column.display_name for column in column_descriptors]

        for name in expected_headers:
            self.assertIn(name, actual_headers)

    @wait_for_data_consistency()
    def assert_published_status(self, live_report_id, column_headers, publish_status):
        columns = self.ldclient.live_report_results_metadata(live_report_id).get('columns')
        columns_matching_publish_status = [
            col.get('name') for idx, col in columns.items() if col.get('published') == publish_status
        ]

        for name in column_headers:
            self.assertIn(name, columns_matching_publish_status)

    def get_json_values(self, data):
        if isinstance(data, list):
            for element in data:
                yield from self.get_json_values(element)
        elif isinstance(data, dict):
            for element in data.values():
                yield from self.get_json_values(element)
        else:
            yield data

    @wait_for_data_consistency()
    def assert_cell_values_present(self, live_report_id, expected_cells):
        result = self.ldclient.execute_live_report(live_report_id)
        self.assertGreater(len(result.get('rows')), 0)

        cell_values = set(self.get_json_values(result.get('rows', {})))

        for cell in expected_cells:
            self.assertIn(cell, cell_values)

    def load_csv(self,
                 project_name='JS Testing',
                 identifier='Compound Structure',
                 compounds_only=True,
                 published=False,
                 filename='load.csv'):
        csv_filename = '{path}/{filename}'.format(path=self.data_path, filename=filename)

        if project_name is None:
            project_name = self._create_unique_project("Test Load CSV").name

        # Load csv into a collection of dicts
        with open(csv_filename, 'r') as csv_file:
            csv_data = []
            file = csv.reader(csv_file, delimiter=',')
            for data in file:
                if file.line_num == 1:
                    csv_headers = data
                    continue

                row = {}
                for key, cell in enumerate(data):
                    header = csv_headers[key]
                    row[header] = cell
                csv_data.append(row)

        # Create a new live report to import into
        project_id = self.ldclient.get_project_id_by_name(project_name)
        definition = self.get_new_live_report(title='Service test: test_csv_load', project_id=project_id)
        live_report = self.ldclient.create_live_report(definition)
        self.lr_id = live_report.id

        # Import
        response = self.ldclient.load_csv(live_report_id=live_report.id,
                                          filename=csv_filename,
                                          project_name=project_name,
                                          published=published,
                                          compounds_only=compounds_only,
                                          identifier=identifier)

        return (live_report, response, csv_data, csv_headers)

    @unittest.skip(reason="replaced with test_load_csv API test")
    def test_csv_load_by_corporate_id(self):
        live_report, response, csv_data, csv_headers = self.load_csv(identifier='ID')

        expected_ids = [row.get('ID') for row in csv_data]
        expected_structures = [row.get('Compound Structure') for row in csv_data]

        self.assert_row_count(live_report.id, 3)
        self.assert_compound_ids(live_report.id, expected_ids)
        self.assert_cell_values_present(live_report.id, expected_ids + expected_structures)

    @unittest.skip(reason="replaced with test_load_csv API test")
    def test_csv_load_by_smiles(self):
        live_report, response, csv_data, csv_headers = self.load_csv(identifier='Compound Structure')

        expected_ids = [row.get('ID') for row in csv_data]
        expected_structures = [row.get('Compound Structure') for row in csv_data]

        self.assert_row_count(live_report.id, 3)
        self.assert_compound_ids(live_report.id, expected_ids)
        self.assert_cell_values_present(live_report.id, expected_ids + expected_structures)

        live_report, response, csv_data, csv_headers = self.load_csv(filename='load_structures.csv',
                                                                     identifier='Compound Structure')
        expected_ids = [r.get('corporate_id') for r in response]
        expected_structures = [row.get('Compound Structure') for row in csv_data]

        self.assert_row_count(live_report.id, 1)
        self.assert_cell_values_present(live_report.id, expected_ids + expected_structures)

    @unittest.skip(reason="replaced with test_load_csv API test")
    def test_csv_load_and_import_columns(self):
        live_report, response, csv_data, csv_headers = self.load_csv(compounds_only=False)

        expected_ids = [row.get('ID') for row in csv_data]
        expected_structures = [row.get('Compound Structure') for row in csv_data]
        expected_values = [
            "Imported Assay Value 1",
            "Imported Assay Value 2",
            "Imported Assay Value 3",
        ]
        expected_cells = expected_ids + expected_structures + expected_values
        expected_headers = [h + ' (undefined)' for h in csv_headers if h != 'Compound Structure']

        self.assert_row_count(live_report.id, 3)
        self.assert_compound_ids(live_report.id, expected_ids)
        self.assert_columns_added(live_report.id, expected_headers)
        # NOTE(zou) ASSAY columns are always published in the metadata endpoint due to a technical
        # limitation on the LD BE.
        # publish_status should be changed to False after that limitation has been lifted
        self.assert_published_status(live_report.id, expected_headers, publish_status=True)
        self.assert_cell_values_present(live_report.id, expected_cells)

    @unittest.skip(reason="replaced with test_load_csv API test")
    def test_csv_load_with_published_columns(self):
        live_report, response, csv_data, csv_headers = self.load_csv(compounds_only=False, published=True)

        expected_ids = [row.get('ID') for row in csv_data]
        expected_structures = [row.get('Compound Structure') for row in csv_data]
        expected_values = [
            "Imported Assay Value 1",
            "Imported Assay Value 2",
            "Imported Assay Value 3",
        ]
        expected_cells = expected_ids + expected_structures + expected_values
        expected_headers = [h + ' (undefined)' for h in csv_headers if h != 'Compound Structure']

        self.assert_row_count(live_report.id, 3)
        self.assert_compound_ids(live_report.id, expected_ids)
        self.assert_columns_added(live_report.id, expected_headers)
        self.assert_published_status(live_report.id, expected_headers, publish_status=True)
        self.assert_cell_values_present(live_report.id, expected_cells)

    @unittest.skip(reason="replaced with test_load_csv API test")
    def test_csv_load_in_global_project(self):
        live_report, response, csv_data, csv_headers = self.load_csv(project_name='Global')
        self.assert_row_count(live_report.id, 3)
        self.assertEqual(live_report.project_id, '0')

    # TODO(fennell): re-enable after figuring out why it works locally but not on
    # Jenkins
    def _export_to_maestro(self):
        live_report_id = "883"
        entity_ids = [
            "CRA-035000",
            "CRA-035001",
        ]

        self.ldclient.execute_live_report(live_report_id=int(live_report_id))

        result = self.ldclient.export_to_maestro(live_report_id, entity_ids=entity_ids)

        self.assertIsInstance(result, bytes)
        self.assertGreater(len(result), 0)

    def test_column_aliases(self):
        lr_def = self.get_new_live_report(title='Service test: Column aliases retrieval test')
        live_report = self.ldclient.create_live_report(lr_def)

        result = self.ldclient.column_aliases(live_report.project_id, live_report.id)
        self.assertEqual(0, len(result))

        result = self.ldclient.column_aliases(live_report.project_id)
        self.assertEqual(0, len(result))

    def test_export_live_report(self):
        corporate_id_1 = 'CRA-032662'
        corporate_id_2 = 'CRA-032664'
        corporate_id_3 = 'CRA-032703'
        column_1_id = 112
        column_1_name = 'STABILITY-PB-PH 7.4 (%Rem@2hr) [%]'
        column_2_id = 923
        column_2_name = 'CYP450 2C19-LCMS (%INH) [%]'
        column_3_id = 1226
        column_3_name = 'ID'

        live_report = self.get_new_live_report(title='service test: test_export_live_report')
        live_report = self.ldclient.create_live_report(live_report)
        self.ldclient.add_rows(live_report.id, [corporate_id_1, corporate_id_2, corporate_id_3])
        self.ldclient.add_columns(live_report.id, [column_1_id, column_2_id])

        @wait_for_data_consistency(interval=200, retries=20)
        def helper(live_report_id, function_parameters, expected_corporate_ids, expected_column_names,
                   unexpected_column_names):

            exported_live_report = self.ldclient.export_live_report(live_report_id=live_report_id,
                                                                    export_type='csv',
                                                                    **function_parameters).decode('utf-8')

            exported_corporate_ids = set()
            exported_column_names = set()
            csv_file = csv.DictReader(exported_live_report.splitlines())
            for row in csv_file:
                exported_corporate_ids.add(row['ID'])
                exported_column_names = set(row.keys())
            print(exported_live_report)
            self.assertSetEqual(
                set(expected_corporate_ids), exported_corporate_ids,
                "Expected IDs ({}) != exported IDs ({})".format(set(expected_corporate_ids), exported_live_report))
            for expected_column_name in expected_column_names:
                self.assertIn(expected_column_name, exported_column_names,
                              "Expected column '{}' but did not find it".format(expected_column_name))
            for unexpected_column_name in unexpected_column_names:
                self.assertNotIn(unexpected_column_name, exported_column_names,
                                 "Found column '{}' but did not expect it".format(unexpected_column_name))

        # Export the whole LiveReport
        helper(live_report.id, {}, [corporate_id_1, corporate_id_2, corporate_id_3], [column_1_name, column_2_name], [])

        # Export only some compounds
        helper(live_report.id, {"corporate_ids_list": [corporate_id_1, corporate_id_2]},
               [corporate_id_1, corporate_id_2], [column_1_name, column_2_name], [])

        # Export only some compounds using the deprecated API
        helper(live_report.id, {"corporate_ids": ",".join([corporate_id_1, corporate_id_2])},
               [corporate_id_1, corporate_id_2], [column_1_name, column_2_name], [])

        # Export only some columns
        helper(live_report.id, {"projection": [column_1_id, column_3_id]},
               [corporate_id_1, corporate_id_2, corporate_id_3], [column_1_name, column_3_name], [column_2_name])

    def test_set_assay_default_aggregation_rules(self):
        rules = [{
            "id": 1,
            "match_target": "ASSAY_RESULT_TYPE",
            "match_operator": "EQUALS",
            "match_operand": "Ki",
            "method": "min",
            "exclude_operators": True,
        }, {
            "id": 2,
            "match_target": "ASSAY_RESULT_NAME",
            "match_operator": "STARTS_WITH",
            "match_operand": "IC50",
            "method": "arithmetic_mean",
            "exclude_operators": False,
        }, {
            "id": 3,
            "match_target": None,
            "match_operator": None,
            "match_operand": None,
            "method": "max",
            "exclude_operators": True,
        }]
        response = self.ldclient.set_assay_default_aggregation_rules(AssayDefaultAggregationRule.from_list(rules))
        self.assertTrue(response is not None)
        rules_json = AssayDefaultAggregationRule.as_list(response)
        # Since we delete all existing rules and then add the sent rules, we want to compare the rules ignoring the 'id'
        # field
        for rule in rules:
            del rule['id']
        for rule in rules_json:
            del rule['id']
        self.assertEqual(rules, rules_json)

    def test_set_assay_default_aggregation_rules_raises_exception(self):
        rules = [{
            "id": 1,
            "match_target": None,
            "match_operator": None,
            "match_operand": u"αωΩδμ",
            "method": "min",
            "exclude_operators": True,
        }, {
            "id": 2,
            "match_target": None,
            "match_operator": None,
            "match_operand": None,
            "method": "max",
            "exclude_operators": True,
        }]
        with self.assertRaises(HTTPError) as err:
            self.ldclient.set_assay_default_aggregation_rules(AssayDefaultAggregationRule.from_list(rules))
        error_raised = err.exception
        self.assertTrue(isinstance(error_raised, HTTPError))
        self.assertTrue(
            error_raised.response.text.find('"message":"Rule - WsAssayDefaultAggregationRule{id=1, '
                                            u'matchTarget=null, matchOperator=null, matchOperand=αωΩδμ, '
                                            'method=MIN, excludeOperators=true} has a null value for match '
                                            'target"') != -1)

    def test_get_assay_default_aggregation_rules(self):
        rules = [{
            "id": 1,
            "match_target": "ASSAY_RESULT_TYPE",
            "match_operator": "EQUALS",
            "match_operand": "Ki",
            "method": "min",
            "exclude_operators": True,
        }, {
            "id": 2,
            "match_target": "ASSAY_RESULT_NAME",
            "match_operator": "STARTS_WITH",
            "match_operand": "IC50",
            "method": "arithmetic_mean",
            "exclude_operators": False,
        }, {
            "id": 3,
            "match_target": None,
            "match_operator": None,
            "match_operand": None,
            "method": "max",
            "exclude_operators": True,
        }]
        rules_created = self.ldclient.set_assay_default_aggregation_rules(AssayDefaultAggregationRule.from_list(rules))
        rules_retrieved = self.ldclient.get_assay_default_aggregation_rules()
        self.assertTrue(rules_retrieved is not None)
        self.assertEqual(AssayDefaultAggregationRule.as_list(rules_created),
                         AssayDefaultAggregationRule.as_list(rules_retrieved))

    def test_update_column_groups(self):
        live_report = self.get_new_live_report(title='service test: test_update_column_groups')
        live_report = self.ldclient.create_live_report(live_report)
        column_groups = self.ldclient.get_column_groups_by_live_report_id(live_report_id=live_report.id)

        column_groups[2], column_groups[3] = column_groups[3], column_groups[2]
        self.ldclient.update_column_groups(live_report_id=live_report.id, column_groups=column_groups)

        server_column_groups = self.ldclient.get_column_groups_by_live_report_id(live_report_id=live_report.id)

        for client_column_group, server_column_group in zip(column_groups, server_column_groups):
            self.assertEqual(client_column_group.as_dict(), server_column_group.as_dict())

    def test_load_formulations_from_json(self):
        lr_def = self.get_new_live_report(title='Service test: test_load_formulations_from_json')
        live_report = self.ldclient.create_live_report(lr_def)
        self.lr_id = live_report.id
        resp = self.ldclient.load_formulations_json(live_report.id,
                                                    '{0}/load_formulations_json.json'.format(self.data_path))

        @wait_for_data_consistency()
        def test(lr):
            live_report_additional_rows = self.ldclient.live_report_rows(lr.id)
            for import_response in resp:
                self.assertIn(import_response.corporate_id, live_report_additional_rows)

        test(live_report)
