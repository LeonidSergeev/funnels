#!/usr/bin/env python
# coding: utf-8
"""
utility for calculating funnels using conversion metrics processor
steps calc settings stored in query.yaml and super_query.yaml
first sys argument is a provided funnel type
funnel steps passed as command-line arguments where agrument is a query name
ex. "python funnel_calc.py app_opened trial subscription"

author -- ToxaZ
"""

from pyanalytics.kpi2.metrics.conversion_utils.processor import funnel, time_based_funnel, super_funnel, time_based_super_funnel
import logging
import argparse
import yaml
import pandas as pd

# supressing unneccessary output
logging.basicConfig(level=logging.INFO)
logging.getLogger('elasticsearch').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)


def get_queries(query_yaml, funnel_steps, time_unit=None):
    '''acquiring queries from provided funnel_steps names'''
    with open(query_yaml, 'r') as f:
        all_queries = yaml.load(f)
    filtered_queries = []
    for each in funnel_steps:
        if each not in all_queries:
            raise ValueError('invalid funnel step {0}'.format(each))
        else:
            filtered_queries.append(all_queries[each])

    # changing default queries time unit for provided:
    if time_unit is not None:
        filtered_queries[0]['time_unit'] = time_unit
    return filtered_queries


def make_request(funnel_type, funnel_query):
    '''making funnel request for certain funnel_type and provided list of queries'''
    if funnel_type == 'funnel':
        return funnel(*funnel_query)
    elif funnel_type == 'super_funnel':
        return super_funnel(*funnel_query)
    elif funnel_type == 'time_based_funnel':
        return time_based_funnel(*funnel_query)
    elif funnel_type == 'time_based_super_funnel':
        return time_based_super_funnel(*funnel_query)
    else:
        raise ValueError(
            'invalid funnel_type {0}'
            '(not "funnel", "time_based_funnel", "super_funnel", "time_based_super_funnel")'
            .format(funnel_type)
        )


def time_based_super_funnel_to_df(results):
    '''converting super funnel results to dataframe'''
    records = []
    for date, values_dict_list in results.items():
        first_run = True
        for values_dict in values_dict_list:
            tmp_fields = []
            values_dict['date'] = date
            records.append(values_dict)

            # checking fields consistency
            if first_run:
                column_names = tmp_fields
                first_run = False
            else:
                if column_names != tmp_fields:
                    raise ValueError('item fields are not the same')

    data = pd.DataFrame.from_records(records)
    return pd.pivot_table(data, values='value', index='date', columns=['name', 'field'])


def main():
    '''main script logic'''
    # parsing command-line arguments
    parser = argparse.ArgumentParser(description='Processing zvq funnels using conversion utils processor '
                                    '(http://bit.ly/1NvBGeq).')
    parser.add_argument('-s', '--super', help='return superfunnel instead of common funnel, '
                        'superfunnel allows to aggregate multiple identifiers.',
                        action="store_true")
    parser.add_argument('-t', '--time_based', help='splitting funnel by time units,'
                        'requires specifying a unit ("day", "week" or "month").',
                        type=str, choices=['day', 'week', 'month'], default=None)
    parser.add_argument('-q', '--queiries', help='print queries parameters', action='store_true')
    parser.add_argument('funnel_steps', nargs='+', help='names of funnel steps in config file')
    args = parser.parse_args()

    # checking for selected funnel type and obtaining funnel steps
    if args.super is False and args.time_based is None:
        funnel_type = 'funnel'
    elif args.super is False and args.time_based in ('day', 'week', 'month'):
        funnel_type = 'time_based_funnel'
    elif args.super is True and args.time_based is None:
        funnel_type = 'super_funnel'
    elif args.super is True and args.time_based in ('day', 'week', 'month'):
        funnel_type = 'time_based_super_funnel'
    else:
        raise ValueError('invalid funnel_type')

    funnel_steps = args.funnel_steps
    query_file = 'query.yaml'
    if args.super:
        query_file = 'super_query.yaml'

    if args.queiries:
        print get_queries(query_file, funnel_steps, args.time_based)

    if funnel_type == 'time_based_super_funnel':
        return time_based_super_funnel_to_df(
            make_request(
                funnel_type, get_queries(
                    query_file, funnel_steps, args.time_based
                )
            )
        )
    elif funnel_type == 'super_funnel':
        return pd.DataFrame(
            make_request(
                funnel_type, get_queries(
                    query_file, funnel_steps, args.time_based
                    )
                ),
        ).transpose()
    else:
        return pd.DataFrame(
            make_request(
                funnel_type, get_queries(
                    query_file, funnel_steps, args.time_based
                    )
                ),
            funnel_steps
        ).transpose()

# if __name__ == '__main__':
#     main

print main()
