import unittest
import mock
from tracer.tracer_data_store import TracerStore, CampaignDailyAction, CampaignDaily, Campaign
import datetime

TEST_STATS = '\n'.join([
    'campaign_id,ad_type,date,spend,actions',
    '856c435c-2dd1-42dd-ad40-b4d3c24d99d9,photo,2017-06-21,943,"[{""A"": 47, ""action"": ""views""}]"',
    'b9c9bcb5-505e-4a39-8c17-51a7941b3fea,photo,2017-06-19,403,"[{""K"": 70, ""action"": ""conversions""}, {""J"": 83, ""action"": ""views""}]"'
])


TEST_AUDIENCES = '\n'.join([
    'campaign_id,audience,impressions',
    'dce13dc8-3da2-4c6f-9e6b-1a2d07ee7f7f,MT_green_33-38,2652',
    'a1ae1c39-491-4974-8bab-b402e581cd9c,SD_blue_27-32,5875',
    '1dd74e30-e65f-4e0b-a5aa-c25da025ec03,MD_pink_48-53,2017',
    '856c435c-2dd1-42dd-ad40-b4d3c24d99d9,RI_green_42-47,1471',
    'b9c9bcb5-505e-4a39-8c17-51a7941b3fea,OK_brown_60-65,7539'
])


class TracerStoreTestCase(unittest.TestCase):

    def get_path(self, filename):
        import os
        return os.path.realpath(os.path.join(os.path.dirname(__file__), '..', filename))

    def test_store(self):

        with mock.patch("tracer.tracer_data_store.open") as mock_file_open:
            side_effects = [
                mock.MagicMock(readlines=mock.MagicMock(return_value=TEST_AUDIENCES.split('\n'))),
                mock.MagicMock(readlines=mock.MagicMock(return_value=TEST_STATS.split('\n'))),
            ]
            mock_file_open.return_value = mock.MagicMock(__enter__=mock.MagicMock(side_effect=side_effects))
            store = TracerStore()
            self.assertListEqual([
                Campaign(campaign_id='dce13dc8-3da2-4c6f-9e6b-1a2d07ee7f7f', state='MT', hair_color='green', age='33-38', impressions=2652),
                Campaign(campaign_id='a1ae1c39-491-4974-8bab-b402e581cd9c', state='SD', hair_color='blue', age='27-32', impressions=5875),
                Campaign(campaign_id='1dd74e30-e65f-4e0b-a5aa-c25da025ec03', state='MD', hair_color='pink', age='48-53', impressions=2017),
                Campaign(campaign_id='856c435c-2dd1-42dd-ad40-b4d3c24d99d9', state='RI', hair_color='green', age='42-47', impressions=1471),
                Campaign(campaign_id='b9c9bcb5-505e-4a39-8c17-51a7941b3fea', state='OK', hair_color='brown', age='60-65', impressions=7539)
            ], store.campaigns)

            self.assertListEqual([
                CampaignDaily(campaign_id='856c435c-2dd1-42dd-ad40-b4d3c24d99d9', state='RI', hair_color='green', age='42-47',
                              impressions=1471, ad_type='photo', date=datetime.date(2017, 6, 21), spend=943,
                              actions=[
                                  CampaignDailyAction(campaign_id='856c435c-2dd1-42dd-ad40-b4d3c24d99d9', state='RI',
                                                      hair_color='green', age='42-47', impressions=1471, ad_type='photo',
                                                      date=datetime.date(2017, 6, 21), spend=943, source='A',
                                                      action='views', value=47)
                              ]),
                CampaignDaily(campaign_id='b9c9bcb5-505e-4a39-8c17-51a7941b3fea', state='OK', hair_color='brown',
                              age='60-65', impressions=7539, ad_type='photo', date=datetime.date(2017, 6, 19), spend=403,
                              actions=[
                                  CampaignDailyAction(campaign_id='b9c9bcb5-505e-4a39-8c17-51a7941b3fea', state='OK',
                                                      hair_color='brown', age='60-65', impressions=7539, ad_type='photo',
                                                      date=datetime.date(2017, 6, 19), spend=403, source='K',
                                                      action='conversions', value=70),
                                  CampaignDailyAction(campaign_id='b9c9bcb5-505e-4a39-8c17-51a7941b3fea', state='OK',
                                                      hair_color='brown', age='60-65', impressions=7539, ad_type='photo',
                                                      date=datetime.date(2017, 6, 19), spend=403, source='J',
                                                      action='views', value=83)
                              ])
            ], store.daily_campaign_stats)

            self.assertListEqual([
                CampaignDailyAction(campaign_id='856c435c-2dd1-42dd-ad40-b4d3c24d99d9', state='RI', hair_color='green',
                                    age='42-47', impressions=1471, ad_type='photo', date=datetime.date(2017, 6, 21),
                                    spend=943, source='A', action='views', value=47),
                CampaignDailyAction(campaign_id='b9c9bcb5-505e-4a39-8c17-51a7941b3fea', state='OK', hair_color='brown',
                                    age='60-65', impressions=7539, ad_type='photo', date=datetime.date(2017, 6, 19),
                                    spend=403, source='K', action='conversions', value=70),
                CampaignDailyAction(campaign_id='b9c9bcb5-505e-4a39-8c17-51a7941b3fea', state='OK', hair_color='brown',
                                    age='60-65', impressions=7539, ad_type='photo', date=datetime.date(2017, 6, 19),
                                    spend=403, source='J', action='views', value=83)
            ], store.daily_action_stats)

            mock_file_open.assert_has_calls([
                mock.call(self.get_path('data_source/Tracer source1.csv'), 'r'),
                mock.call().__enter__(),
                mock.call().__exit__(None, None, None),
                mock.call(self.get_path('data_source/Tracer source2.csv'), 'r'),
                mock.call().__enter__(),
                mock.call().__exit__(None, None, None),
            ])


if __name__ == '__main__':
    unittest.main()
