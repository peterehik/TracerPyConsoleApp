from collections import namedtuple
import json
import datetime
import os

Campaign = namedtuple('Campaign', 'campaign_id, state, hair_color, age, impressions')
CampaignDaily = namedtuple('CampaignDaily',
                           'campaign_id, state, hair_color, age, impressions, ad_type, date, spend, actions')
CampaignDailyAction = \
    namedtuple('CampaignDailyAction',
               'campaign_id, state, hair_color, age, impressions, ad_type, date, spend, source, action, value')
_store = None


class TracerStore(object):

    def __init__(self):
        self._campaigns, self._campaign_daily_stats, self.campaign_daily_action_stats = None, None, None
        self._campaign_look_up = dict()
        self.reload()

    def reload(self):
        self._load_audiences()
        self._load_audience_stats_by_day()

    @property
    def campaigns(self):
        if self._campaigns is None:
            self.reload()
        return self._campaigns

    @property
    def daily_action_stats(self):
        if self.campaign_daily_action_stats is None:
            self.reload()
        return self.campaign_daily_action_stats

    @property
    def daily_campaign_stats(self):
        if self._campaign_daily_stats is None:
            self.reload()
        return self._campaign_daily_stats

    def _create_audience_stats(self, line):

        def breakdown_action(action_data):
            action = action_data['action']
            source, value = [(k, v) for k, v in a.iteritems() if k != 'action'][0]
            action_dict = dict(action=str(action), source=str(source), value=int(value))
            action_dict.update(daily_campaign_data._asdict())
            action_dict = dict((k, v) for k, v in action_dict.iteritems() if k != 'actions')
            return CampaignDailyAction(**action_dict)

        campaign, ad_type, date, spend, _ = line[:line.index('"')].split(',')
        actions = line[line.index('"')+1:].strip('"').replace('""', '"')
        actions = json.loads(actions)
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        campaign_data = self._campaign_look_up[campaign]

        daily_campaign_data = CampaignDaily(campaign_id=campaign, ad_type=ad_type, date=date, spend=int(spend),
                                            state=campaign_data.state, hair_color=campaign_data.hair_color,
                                            age=campaign_data.age, impressions=campaign_data.impressions,
                                            actions=None)
        actions = [breakdown_action(a) for a in actions]
        daily_campaign_data_asdict = daily_campaign_data._asdict()
        daily_campaign_data_asdict['actions'] = actions
        daily_campaign_data = CampaignDaily(**daily_campaign_data_asdict)
        return daily_campaign_data, actions

    @staticmethod
    def _create_audience(line):
        campaign, audience, impression = line.split(',')
        state, hair_color, age = audience.split('_')
        return Campaign(campaign_id=campaign, state=state, hair_color=hair_color, age=age, impressions=int(impression))

    @staticmethod
    def _source_file_name(filename):
        return os.path.realpath(os.path.join(os.path.dirname(__file__), '..', filename))

    def _load_audiences(self):
        self._campaigns = []
        with open(self._source_file_name('data_source/Tracer source1.csv'), 'r') as file_obj:
            i = 0
            for line in file_obj.readlines():
                if i > 0:
                    campaign = self._create_audience(line.strip())
                    self._campaigns.append(campaign)
                    self._campaign_look_up[campaign.campaign_id] = campaign
                i = i + 1

    def _load_audience_stats_by_day(self):
        self._campaign_daily_stats, self.campaign_daily_action_stats = [], []
        with open(self._source_file_name('data_source/Tracer source2.csv'), 'r') as file_obj:
            i = 0
            for line in file_obj.readlines():
                if i > 0:
                    stats_per_day, actions = self._create_audience_stats(line.strip())
                    self.campaign_daily_action_stats = \
                        self.campaign_daily_action_stats + actions
                    self._campaign_daily_stats.append(stats_per_day)
                i = i + 1


def main():
    pass


if __name__ == '__main__':
    main()




