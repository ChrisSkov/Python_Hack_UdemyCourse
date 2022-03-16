from ip2geotools.databases.noncommercial import DbIpCity
import pycountry
import datetime

# res = DbIpCity.get('45.146.165.37', api_key='free')
# full_country_name = pycountry.countries.get(alpha_2=res.country)
# print(res.city + ' ' + full_country_name.name)
path_to_log = '/home/kali/Desktop/log1.txt'

black_list = open('./banned_requests.txt')
sus = black_list.readlines()
sus = sus[0].split(',')
my_file = open(path_to_log).readlines()

my_dict = {}


# TODO: optimize for speed
# white list > black list
# how to output?


def cmp_file_to_wordlist():
    intrusion_attempts = 0
    lines = 0
    results_name = 'log_results_%s.txt' % (datetime.datetime.now().date())
    results = open(results_name, 'a')
    for line in my_file:
        for item in sus[0:len(sus)]:
            if item in line:
                line_to_print = find_info_from_ip(line)
                print('INTRUSION ATTEMPT ' + line_to_print[0])
                intrusion_attempts += 1
                results.write('\nINTRUSION ATTEMPT ' + line_to_print[0])
                country = line_to_print[1].name
                if country not in my_dict:
                    my_dict[country] = 1
                else:
                    my_dict[country] = my_dict[country] + 1
                break
        lines += 1
    print(intrusion_attempts, lines)


def find_info_from_ip(line):
    request_ip = line[0:line.find(' ')]
    request_info = DbIpCity.get(str(request_ip), api_key='free')
    req_country = pycountry.countries.get(alpha_2=request_info.country)
    line_to_print = request_ip + ' ' + request_info.city + ' ' + req_country.name + ' ' + req_country.flag
    result = (line_to_print, req_country)
    return result


if __name__ == '__main__':
    cmp_file_to_wordlist()
    print(my_dict)
