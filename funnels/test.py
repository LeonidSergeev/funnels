import pandas as pd
import numpy as np
from collections import OrderedDict

test = OrderedDict([('2015-12-28', [{'field': 'app_instance', 'name': 'install_ios', 'value': 31397}, {'field': 'app_instance', 'name': 'active', 'value': 17952}, {'field': 'user_id', 'name': 'active', 'value': 17321}]),
                    ('2016-01-04', [{'field': 'app_instance', 'name': 'install_ios', 'value': 66938}, {'field': 'app_instance', 'name': 'active', 'value': 38100}, {'field': 'user_id', 'name': 'active', 'value': 35399}]),
                    ('2016-01-11', [{'field': 'app_instance', 'name': 'install_ios', 'value': 66074}, {'field': 'app_instance', 'name': 'active', 'value': 36089}, {'field': 'user_id', 'name': 'active', 'value': 33059}]),
                    ('2016-01-18', [{'field': 'app_instance', 'name': 'install_ios', 'value': 43093}, {'field': 'app_instance', 'name': 'active', 'value': 23094}, {'field': 'user_id', 'name': 'active', 'value': 21118}])])
test1 = [{'field': 'app_instance', 'name': 'install_ios', 'value': 235336}, {'field': 'app_instance', 'name': 'active', 'value': 130768}, {'field': 'user_id', 'name': 'active', 'value': 121296}]

p = pd.DataFrame(test1)
p['name'] = p["name"].map(str) + " " + p["field"]
p = p.set_index('name')
print p.transpose

# dates = [test.items()[x][0] for x in range(len(test))]
# fields = [test.items()[x][1][0]['field'] for x in range(len(test))]
# print fields
# dates = []
# names = []
# values = []
# columns = []
# for time_unit, values_list in test.items():
#     dates.append(time_unit)
#     tt = []
#     fields = []
#     for item in values_list:
#         fields.append(str(item['field']) + " " + str(item['name']))
#         print fields
#         tt.append(item['value'])
#     values.append(tt)
#     # for element in time_unit:
#     #     print element

# # print dates, fields, values
# # group by
# # index = pd.MultiIndex(levels=fields, labels=values)
# results = pd.DataFrame(values, index=dates, columns=fields)
# print results

# # print test
# # print [test.items()[x][0] for x in range(len(test))]

# # print pd.DataFrame(
# #     index=[[test.items()[x][1][0]['field'] for x in range(len(test))], [test.items()[x][1][0]['name'] for x in range(len(test))]],
# #     columns=[test.items()[x][0] for x in range(len(test))]
# )


def df_results(funnel_type, results):
    '''converting funnel results to dataframe'''
    first_run = True
    fields = []
    if funnel_type == 'time_based_super_funnel':
        dates = []
        values = []
        for time_unit, values_list in results.items():
            dates.append(time_unit)
            val = []
            tmp_fields = []
            for item in values_list:
                val.append(item['value'])
                tmp_fields.append(str(item['field']) + " " + str(item['name']))

            # checking fields consistency
            if first_run:
                fields = tmp_fields
                first_run = False
            else:
                if fields != tmp_fields:
                    raise ValueError('item fields are not the same')

            values.append(val)
        return pd.DataFrame(values, index=dates, columns=fields)

# print df_results('time_based_super_funnel', test)