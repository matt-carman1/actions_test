"""
Experimental LDClient service tests
NOTE: all changes to LD test server should be scoped to project 4
"""
import logging
import os
import unittest

from library.api.urls import LDCLIENT_HOST
from ldclient.__experimental.experimental_client import ExperimentalLDClient
from ldclient.__experimental.experimental_models import QueryCondition
from ldclient.models import (FreeformColumn, LiveReport, Observation, Rationale)

logger = logging.getLogger(__name__)


@unittest.skip(reason="SS-30686: Replaced the test with api/advanced_search/test_advanced_search")
class ExperimentalLDClientServiceTests(unittest.TestCase):

    # test instance variables
    lr_id = None
    data_path = os.path.join(os.path.dirname(__file__), "../../../resources/legacy")

    @classmethod
    def setUpClass(cls):
        # Create connection to LiveDesign
        user = 'demo'
        password = 'demo'
        # This corresponds to the JS Testing project in Jenkins starter data
        cls.active_project = os.getenv('EXPERIMENTAL_LDCLIENT_TEST_PROJECT', '4')
        cls.ldclient = ExperimentalLDClient(LDCLIENT_HOST, user, password, compatibility_mode=(8, 10))
        cls.rationale = Rationale(description="WSClientIntegrationTest", user_name=None)

    def tearDown(self):
        if self.lr_id:
            self.ldclient.delete_live_report(live_report_id=self.lr_id)
            logger.debug('Deleted LiveReport {}'.format(self.lr_id))

    def _get_new_live_report(self, title='integration test'):
        live_report = LiveReport(title=title,
                                 description='some',
                                 update_policy='by_cachebuilder',
                                 default_rationale='Default rationale description',
                                 owner='demo',
                                 template=False,
                                 shared_editable=True,
                                 active=True,
                                 project_id=self.active_project)
        return live_report

    def test_update_lr_query_and_search_compounds(self):
        """
        Test the update adv query and search API service
        """
        lr_def = self._get_new_live_report(title='Service test: query updation and search execution test')
        live_report = self.ldclient.create_live_report(lr_def)
        self.lr_id = live_report.id
        # Load 2 compounds in the LR, having entity IDs ['DUMMY1', 'DUMMY2']
        compounds = self.ldclient.load_sdf(live_report.id,
                                           '{0}/real_dummy_compounds.sdf'.format(self.data_path),
                                           compound_source="non_pri")
        self.assertEqual(len(compounds), 2)
        # Create 2 FFCs on which we will run the query
        freeform_column_one = self.ldclient.create_freeform_column(
            FreeformColumn(
                name='First FFC',
                type=FreeformColumn.COLUMN_TEXT,
                description='I am a freeform column for text',
                project_id=live_report.project_id,
                live_report_id=live_report.id,
                published=True,
            ))
        freeform_column_two = self.ldclient.create_freeform_column(
            FreeformColumn(
                name='Second FFC',
                type=FreeformColumn.COLUMN_TEXT,
                description='I am a freeform column for text',
                project_id=live_report.project_id,
                live_report_id=live_report.id,
                published=True,
            ))
        # Fill in values for each of the columns, for both compounds
        # DUMMY_1 : (val_1, val_3), DUMMY_2: (val_2, val_4)
        observations_to_upload = (
            Observation(
                project_id=live_report.project_id,
                addable_column_id=freeform_column_one.id,
                entity_id='DUMMY_1',
                live_report_id=live_report.id,
                value='val_1',
            ),
            Observation(
                project_id=live_report.project_id,
                addable_column_id=freeform_column_one.id,
                entity_id='DUMMY_2',
                live_report_id=live_report.id,
                value='val_2',
            ),
            Observation(
                project_id=live_report.project_id,
                addable_column_id=freeform_column_two.id,
                entity_id='DUMMY_1',
                live_report_id=live_report.id,
                value='val_3',
            ),
            Observation(
                project_id=live_report.project_id,
                addable_column_id=freeform_column_two.id,
                entity_id='DUMMY_2',
                live_report_id=live_report.id,
                value='val_4',
            ),
        )
        observations = self.ldclient.add_freeform_column_values(observations_to_upload)
        self.assertEqual(len(observations), 4)
        # First condition: value in first FFC should be 'val_1' (true for DUMMY_1)
        condition_one = QueryCondition(
            addable_column_id=freeform_column_one.id,
            id='1',
            type='observation',
            value='val_1',
            value_type='value',
        )
        # Second condition: value in second FFC should be 'val_4' (true for DUMMY_2)
        condition_two = QueryCondition(
            addable_column_id=freeform_column_two.id,
            id='2',
            type='observation',
            value='val_4',
            value_type='value',
        )
        conditions = [condition_one, condition_two]
        expression = '1 | 2'

        result_compounds = set(['DUMMY_1', 'DUMMY_2'])
        # Do an advanced search query based on the new conditions and expression, search should return both the
        # compounds
        obsv_result_compounds = set(
            self.ldclient.update_lr_query_and_search_compounds(live_report.id, live_report.project_id, conditions,
                                                               expression))

        self.assertSetEqual(obsv_result_compounds, result_compounds)
