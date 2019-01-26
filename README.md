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
