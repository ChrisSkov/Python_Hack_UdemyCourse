from ip2geotools.databases.noncommercial import DbIpCity
import pycountry

# res = DbIpCity.get('45.146.165.37', api_key='free')
# full_country_name = pycountry.countries.get(alpha_2=res.country)
# print(res.city + ' ' + full_country_name.name)
path_to_log = ''
with open(path_to_log, 'r') as file:
    for line in file.readlines():
        new_string = line.find(' ')
        request_ip = line[0:new_string]
        request_info = DbIpCity.get(str(request_ip), api_key='free')
        req_country = pycountry.countries.get(alpha_2=request_info.country)
        line_to_print = request_ip + ' ' + request_info.city + ' ' + req_country.name + ' ' + req_country.flag
        if 'chmod' or 'shell' or 'cmd' in line:
            print('INTRUSION ATTEMPT ' + line_to_print)

        print(line_to_print)
    # for line in file.readlines():

    #   res_2 = DbIpCity.get(line[:13], api_key='free')
    #  print(res_2)
