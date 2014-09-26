from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )
import httplib, string, sys, re
import nmap
import math


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'gip'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_gip_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.

"""
@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    return dict(project='gip')


@view_config(route_name='geo_ip',renderer='templates/geo_ip.pt')
def geo_view(request):
    return dict(title='IP Geolocation')

@view_config(route_name='geoip', renderer='templates/geoip.pt')
def geoip_view(request):
    coordinates=''
    host= request.POST.get('ip')
    body = "ips=" + host
    exists = MyModel.exists(host)
    if exists:
        ip_host=MyModel.get_by_host(host).ip
        city=MyModel.get_by_host(host).city
        country=MyModel.get_by_host(host).country
        coordinates=MyModel.get_by_host(host).coordinates
        



    else:
        try:

            v = httplib.HTTP("www.geoiptool.com")
            v.putrequest('GET', "/es/?IP=" + host)
            v.putheader('Host', 'www.geoiptool.com')
            v.putheader('User-agent', 'Internet Explorer 6.0 ')
            v.endheaders()
            returncode, returnmsg, headers = v.getreply()
            response = v.file.read()

            res = re.compile("<td align=\"left\" class=\"arial_bold\">.*</td>")
            results = res.findall(response)
            res = []

            for i in results:
                i = i.replace("<td align=\"left\" class=\"arial_bold\">", "")
                i = i.replace("</td>", "")
                res.append(i)

            ip_host = res[0]
            country = re.sub("<.*nk\">", "", res[1])
            country = country.replace("</a>", "")
            country = re.sub("<.*middle\" >", "", country) + " " + res[2]
            city = re.sub("<.*nk\">", "", res[3])
            city = city.replace("</a>", "") + " " + res[4]
            coordinates = res[8] + "," + res[7]

            info=MyModel(host=host,ip=ip_host,country=country,city=city,coordinates=coordinates)
            DBSession.add(info)



        except:
            pass

    return {
         'host': host,
        'ip_host': ip_host,
        'country': country,
        'city': city,
        'coordinates': coordinates
        }
@view_config(route_name='scan', renderer='templates/scan.pt')
def scan_view(request):
    return dict(project='gip')

@view_config(route_name='scanner',renderer='templates/scanner.pt')
def scanner_view(request):
    msg=None
    host=request.POST.get('ip')
    host=str(host)
    port=str(request.POST.get('port'))

    nmScan = nmap.PortScanner()
    nmScan.scan(host,port)
    state=nmScan[host]['tcp'][int(port)]['state']
    return {
        'host':host,
        'port':port,
        'msg':msg,
        'state':state
    }

@view_config(route_name='distance', renderer='templates/distance.pt')
def distance_view(request):
    return dict(project='gip')

@view_config(route_name='distance_calci', renderer='templates/dist.pt')
def distance_calci_view(request):
    lat1=request.POST.get('lat1')
    lat2=request.POST.get('lat2')
    long1=request.POST.get('long1')
    long2=request.POST.get('long2')

    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - float(lat1))*degrees_to_radians
    phi2 = (90.0 - float(lat2))*degrees_to_radians

    # theta = longitude
    theta1 = float(long1)*degrees_to_radians
    theta2 = float(long2)*degrees_to_radians
    # distance = radius of earcth * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    distance_km=arc*6371
    distance_mile=arc*3963.1676
    distance_meter=arc*6378100
    return {
    'km':distance_km,
    'mile':distance_mile,
    'meter':distance_meter,
    'lat1':lat1,
    'lat2':lat2,
    'long1':long1,
    'long2':long2


    }


@view_config(route_name='google_hacking', renderer='templates/google.pt')
def ghacking_view(request):
    return dict(desc='GOOGLE HACKING')







