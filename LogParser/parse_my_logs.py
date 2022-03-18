#!/usr/bin/env python
from ip2geotools.databases.noncommercial import DbIpCity
import pycountry
import datetime
import re
import os
import yaml
from yaml.loader import SafeLoader
import glob

# res = DbIpCity.get('45.146.165.37', api_key='free')
# full_country_name = pycountry.countries.get(alpha_2=res.country)
# print(res.city + ' ' + full_country_name.name)
# path_to_log = open('/home/kali/Desktop/log.txt', 'r')
black_list = './banned_requests.txt'
white_list = './white_list.txt'
dir_path = './'

files = []


def regex_test():
    with open('configme.yaml') as config:
        data = yaml.load(config, Loader=SafeLoader)
        regex1 = r"%s" % (data['parsing']['-name_pattern'])
    for file in os.listdir('./'):
        matches = re.findall(regex1, file, re.MULTILINE)
        files.append(matches[0])
        for match in matches:
            files.append(match.group())


def wrangle_file(file_to_wrangle):
    file_to_wrangle = open(str(file_to_wrangle), 'r').readlines()
    wrangled_file = file_to_wrangle[0].split(',')
    return wrangled_file


block_list = wrangle_file(black_list)
allow_list = wrangle_file(white_list)

my_dict = {}


# TODO: optimize for speed
# white list > black list
# how to output?
def cmp_file_to_blacklist():
    regex_test()
    lines = 0
    intrusion_attempts, results = setup_result_file()
    for file in files:
        with open(file, 'r') as log_to_read:
            for line in log_to_read:
                line = line.lower()
                for item in block_list[0:len(block_list)]:
                    if item in line:
                        intrusion_attempts += 1
                        line_to_print = find_info_from_ip(line)
                        print('INTRUSION ATTEMPT ' + line_to_print[0])
                        results.write('\nINTRUSION ATTEMPT ' + line_to_print[0])
                        country = line_to_print[1].name
                        if country not in my_dict:
                            my_dict[country] = 1
                        else:
                            my_dict[country] = my_dict[country] + 1
                        break
                lines += 1
                print(intrusion_attempts, lines)
    close_files()


def cmp_file_to_whitelist():
    intrusion_attempts, results = setup_result_file()
    regex_test()
    for file in files:
        with open(file, 'r') as log_to_read:
            for line in log_to_read:
                line_to_regex = line[line.index('"'):]
                line_to_regex = line_to_regex[1:line_to_regex[1:].find('"') + 1]
                regex = r"^(?:GET\s|POST\s)+(\/[a-zA-Z]+\/[a-zA-Z]+\s)(?:HTTP\/1.1)$"
                matches = re.findall(regex, line_to_regex, re.MULTILINE)
                if len(matches) == 0:
                    intrusion_attempts += 1
                    line_to_write = find_info_from_ip(str(line))
                    results.write(line_to_write[0] + '\n')


def setup_result_file():
    intrusion_attempts = 0
    results_name = 'log_results_%s.txt' % (datetime.datetime.now().date())
    results = open(results_name, 'a')
    return intrusion_attempts, results


def close_files():
    black_list.close()
    white_list.close()


def find_info_from_ip(line):
    request_ip = line[0:line.find(' ')]
    request_info = DbIpCity.get(request_ip, api_key='free')
    req_country = pycountry.countries.get(alpha_2=request_info.country)
    line_to_print = request_ip + ' ' + request_info.city + ' ' + req_country.name + ' ' + req_country.flag
    result = (line_to_print, req_country)
    return result


if __name__ == '__main__':
    #cmp_file_to_whitelist()
    cmp_file_to_blacklist()

