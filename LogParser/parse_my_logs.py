from ip2geotools.databases.noncommercial import DbIpCity
import pycountry
import datetime
import re
# res = DbIpCity.get('45.146.165.37', api_key='free')
# full_country_name = pycountry.countries.get(alpha_2=res.country)
# print(res.city + ' ' + full_country_name.name)
path_to_log = open('/home/kali/Desktop/log.txt', 'r')
black_list = open('./banned_requests.txt')
white_list = open('./white_list.txt')

log_to_read = path_to_log.readlines()
block_list = black_list.readlines()
block_list = block_list[0].split(',')
allow_list = white_list.readlines()
allow_list = allow_list[0].split(',')

my_dict = {}


# TODO: optimize for speed
# white list > black list
# how to output?
def cmp_file_to_blacklist():
    intrusion_attempts = 0
    lines = 0
    results_name = 'log_results_%s.txt' % (datetime.datetime.now().date())
    results = open(results_name, 'a')
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
    intrusion_attempts = 0
    results_name = 'log_results_%s.txt' % (datetime.datetime.now().date())
    results = open(results_name, 'a')
    for line in log_to_read:
        line_to_regex = line[line.index('"'):]
        line_to_regex = line_to_regex[1:line_to_regex[1:].find('"')+1]
        regex = r"^(?:GET\s|POST\s)+(\/[a-zA-Z]+\/[a-zA-Z]+\s)(?:HTTP\/1.1)$"
        matches = re.findall(regex, line_to_regex, re.MULTILINE)
        if len(matches) == 0:
            intrusion_attempts += 1
            line_to_write = find_info_from_ip(line)
            results.write(line_to_write[0] + '\n')
        # for matchNum, match in enumerate(matches, start=1): print("Match {matchNum} was found at {start}-{end}: {
        # match}".format(matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()))

    print(intrusion_attempts)



def close_files():
    path_to_log.close()
    black_list.close()
    white_list.close()


def find_info_from_ip(line):
    request_ip = line[0:line.find(' ')]
    request_info = DbIpCity.get(str(request_ip), api_key='free')
    req_country = pycountry.countries.get(alpha_2=request_info.country)
    line_to_print = request_ip + ' ' + request_info.city + ' ' + req_country.name + ' ' + req_country.flag
    result = (line_to_print, req_country)
    return result


if __name__ == '__main__':
    #cmp_file_to_blacklist()
    cmp_file_to_whitelist()
    #print(my_dict)
