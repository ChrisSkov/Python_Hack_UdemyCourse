from ip2geotools.databases.noncommercial import DbIpCity
import pycountry
import datetime
import re
import yaml
from yaml.loader import SafeLoader
import glob

# Path to black list
black_list = './black_list.txt'
# Path to while list
white_list = './white_list.txt'

my_dict = {}

# List for files to read
files = []


# Word manipulation to put black and white list into list objects
def wrangle_file(file_to_wrangle):
    file_to_wrangle = open(str(file_to_wrangle), 'r').readlines()
    wrangled_file = file_to_wrangle[0].split(',')
    return wrangled_file


block_list = wrangle_file(black_list)
allow_list = wrangle_file(white_list)


# Find files in a directory according to pattern in configme.yaml
def find_files_in_dir():
    with open('configme.yaml') as config:
        data = yaml.load(config, Loader=SafeLoader)
        glob_pattern = data['parsing']['-name_pattern']

    for file in glob.glob(glob_pattern):
        files.append(file)


# compare contents of file(s) to black list
def cmp_file_to_blacklist():
    find_files_in_dir()
    lines = 0
    intrusion_attempts, results = setup_result_file()
    for file in files:
        with open(file, 'r') as log_to_read:
            for line in log_to_read.readlines():
                line = line.lower()
                for item in block_list[0:len(block_list)]:
                    if item in line:
                        intrusion_attempts += 1
                        line_to_print = find_info_from_ip(line)
                        results.write('\nINTRUSION ATTEMPT ' + line_to_print[0])
                        country = line_to_print[1].name
                        if country not in my_dict:
                            my_dict[country] = 1
                        else:
                            my_dict[country] = my_dict[country] + 1
                        break
                lines += 1


# compare contents of file(s) to white list
def cmp_file_to_whitelist():
    intrusion_attempts, results = setup_result_file()
    find_files_in_dir()
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


# Sort out naming of result file
def setup_result_file():
    intrusion_attempts = 0
    results_name = 'log_results_%s.txt' % (datetime.datetime.now().date())
    results = open(results_name, 'a')
    return intrusion_attempts, results


# look up suspicious IP address
def find_info_from_ip(line):
    if line is not None:
        request_ip = line[0:line.find(' ')]
        request_info = DbIpCity.get(request_ip, api_key='free')
        req_country = pycountry.countries.get(alpha_2=request_info.country)
        line_to_print = request_ip + ' ' + request_info.city + ' ' + req_country.name + ' ' + req_country.flag
        result = (line_to_print, req_country)
        return result


# Starts program according to parameters in the config file
def start_program():
    with open('configme.yaml') as config:
        data = yaml.load(config, Loader=SafeLoader)
        if data['parsing']['-black_list'] == 'True':
            cmp_file_to_blacklist()
        elif data['parsing']['-white_list'] == 'True':
            cmp_file_to_whitelist()
        elif data['parsing']['-black_list'] == 'True' and data['parsing']['-white_list'] == 'True':
            cmp_file_to_blacklist()
            cmp_file_to_whitelist()


if __name__ == '__main__':
    try:
        start_program()
    except Exception:
        print(Exception)
