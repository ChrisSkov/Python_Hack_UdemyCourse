from ip2geotools.databases.noncommercial import DbIpCity
import pycountry

# res = DbIpCity.get('45.146.165.37', api_key='free')
# full_country_name = pycountry.countries.get(alpha_2=res.country)
# print(res.city + ' ' + full_country_name.name)
path_to_log = '/home/kali/Desktop/log1.txt'
intrusion_attempts = 0
lines = 0
black_list = open('./banned_requests.txt')
sus = black_list.readlines()
sus = sus[0].split(',')
my_file = open(path_to_log).readlines()

for item in sus[0:len(sus)]:
    for line in my_file:
        new_string = line.find(' ')
        request_ip = line[0:new_string]
        request_info = DbIpCity.get(str(request_ip), api_key='free')
        req_country = pycountry.countries.get(alpha_2=request_info.country)
        line_to_print = request_ip + ' ' + request_info.city + ' ' + req_country.name + ' ' + req_country.flag
        if item in line:
            print('INTRUSION ATTEMPT ' + line_to_print)
            intrusion_attempts += 1
            break
    lines += 1
    print(intrusion_attempts, lines)

