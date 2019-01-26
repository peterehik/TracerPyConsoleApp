# The goal of this exercise is to simulate the creation of a report, by working with two datasets, and drawing some basic insights. Given the stated assumptions, please provide your answers to the following questions (in a .txt file), as well as your code. Please use either Python or Ruby.
#
# source1.csv contains a list of campaigns, audiences and impressions served
#     - the audience is composed of three elements separated by the delimiter "_"
#     - the elements represent the state, hair color and age range of that campaign, respectively
#
# source2.csv contains stats by day for each audience, broken out by ad_type
#     - actions are a json string in the format [{'action': name, source: value}]
#     - for example, {'action': 'conversions', A': 20} means source A reported 20 conversions
#
# Do not disregard any data as invalid.
#
# 1. what was the total spent against people with purple hair?
# 2. how many campaigns spent on more than 4 days?
# 3. how many times did source H report on clicks?
# 4. which sources reported more "junk" than "noise"?
# 5. what was the total cost per view for all video ads, truncated to two decimal places?
# 6. how many source B conversions were there for campaigns targeting NY?
# 7. what combination of state and hair color had the best CPM?
#
# BONUS - include a timestamp of the run time for your solution :)

from tracer.tracer_data_store import TracerStore
import itertools
import datetime


def timeit(func):
    def wrapper(self):
        start = datetime.datetime.now()
        result = func(self)
        end = datetime.datetime.now()
        time_str = 'Runtime: {0:.3f} seconds'.format((end-start).total_seconds())
        return '%s\n%s' % (result, time_str)
    return wrapper


class MyTimer(object):

    def __init__(self, text):
        self._text = text
        self._start, self._end = None, None

    def __enter__(self):
        self._start = datetime.datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._end = datetime.datetime.now()
        print '{0} {1:.3f} seconds'.format(self._text, (self._end - self._start).total_seconds())


class TracerMetricsRunner(object):

    def __init__(self, store):
        self._store = store  # type: TracerStore

    @timeit
    def metric1(self):
        """
        # 1. what was the total spent against people with purple hair?
        """
        return sum(map(lambda x: x.spend, filter(lambda x: x.hair_color == 'purple', self._store.daily_campaign_stats)))

    @timeit
    def metric2(self):
        """
        # 2. how many campaigns spent on more than 4 days?
        """

        campaign_dates = sorted(set([(item.campaign_id, item.date)
                                     for item in self._store.daily_campaign_stats if item.spend > 0]),
                                key=lambda x: x[0])
        campaign2numdates = [[campaign_id, len(list(grp))] for campaign_id, grp in
                             itertools.groupby(campaign_dates, key=lambda x: x[0])]
        return len(filter(lambda x: x[1] > 4, campaign2numdates))

    @timeit
    def metric3(self):
        """
        # 3. how many times did source H report on clicks?
        """
        return sum(map(lambda x: x.value,
                       filter(lambda x: x.source == 'H' and x.action == 'clicks', self._store.daily_action_stats)))

    @timeit
    def metric4(self):
        """
        # 4. which sources reported more "junk" than "noise"?
        """
        junk_data = sorted(filter(lambda x: x.action == 'junk', self._store.daily_action_stats),
                           key=lambda x: x.source)
        noise_data = sorted(filter(lambda x: x.action == 'noise', self._store.daily_action_stats),
                            key=lambda x: x.source)

        junk = dict((key, len(list(grp)),) for key, grp in itertools.groupby(junk_data, key=lambda x: x.source))
        noise = dict((key, len(list(grp)),) for key, grp in itertools.groupby(noise_data, key=lambda x: x.source))

        return len([k for k, v in junk.iteritems() if v > noise.get(k, 0)])

    @timeit
    def metric5(self):
        """
        what was the total cost per view for all video ads, truncated to two decimal places?
        """
        data = filter(lambda x: x.action == 'views' and x.ad_type == 'video', self._store.daily_action_stats)
        total_views = sum(x.value for x in data)
        total_cost = sum(float(x.spend) for x in data)
        return '{0:.2f}'.format(total_cost/total_views)

    @timeit
    def metric6(self):
        """
        how many source B conversions were there for campaigns targeting NY?
        """
        data = filter(lambda x: x.action == 'conversions' and x.state == 'NY' and x.source == 'B',
                      self._store.daily_action_stats)
        return len(data)

    @timeit
    def metric7(self):
        """
        what combination of state and hair color had the best CPM i.e. cost per 1000 impressions?
        """
        def keyfunc(item):
            return item.state, item.hair_color

        def cpm(items):
            cost = sum(float(x.spend) for x in items)
            impressions = sum(float(x.impressions)/1000 for x in items)
            return cost/impressions

        data = sorted(self._store.daily_campaign_stats, key=keyfunc)
        grp_data = [(key, cpm((list(grp)))) for key, grp in itertools.groupby(data, key=keyfunc)]
        state_hair_color, total_cpm = max(grp_data, key=lambda x: x[1])
        return 'state: %s, hair color: %s' % state_hair_color

    def results_as_string(self):
        result_stats = [
            '1. what was the total spent against people with purple hair? %s' % self.metric1(),
            '2. how many campaigns spent on more than 4 days? %s' % self.metric2(),
            '3. how many times did source H report on clicks? %s' % self.metric3(),
            '4. which sources reported more "junk" than "noise"? %s' % self.metric4(),
            '5. what was the total cost per view for all video ads, truncated to two decimal places? %s' % self.metric5(),
            '6. how many source B conversions were there for campaigns targeting NY? %s' % self.metric6(),
            '7. what combination of state and hair color had the best CPM? %s' % self.metric7()
        ]
        return '\n'.join(result_stats)


def main():
    with MyTimer('Tracer report processing time:'):
        with MyTimer('Loading source files into memory'):
            store = TracerStore()
        runner = TracerMetricsRunner(store)
        print runner.results_as_string()


if __name__ == '__main__':
    main()
