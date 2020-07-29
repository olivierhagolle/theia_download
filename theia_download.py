#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
import glob
import json
import time
import os
import os.path
import optparse
import sys
from datetime import date, datetime
if sys.version_info[0] == 2:
    from urllib import urlencode
elif sys.version_info[0] > 2:
    from urllib.parse import urlencode


###########################################################################


class OptionParser (optparse.OptionParser):

    def check_required(self, opt):
        option = self.get_option(opt)

        # Assumes the option's 'default' is set to None!
        if getattr(self.values, option.dest) is None:
            self.error("%s option not supplied" % option)

###########################################################################


def checkDate(date_string):

    d = date_string.split('-')
    try:
        year = d[0]
        month = d[1]
        day = d[2]
        dd = datetime(int(year), int(month), int(day))
    except ValueError:
        print("Please use a valid date")
        sys.exit(-1)
    except IndexError:
        print("Please use yyyy-mm-dd format for dates")
        sys.exit(-1)

###########################################################################


# ==================
# parse command line
# ==================
if len(sys.argv) == 1:
    prog = os.path.basename(sys.argv[0])
    print('      '+sys.argv[0]+' [options]')
    print("     Aide : ", prog, " --help")
    print("        ou : ", prog, " -h")
    print("example 1 : python %s -t 'T31TFJ' -a config.cfg -d 2018-07-01 -f 2018-07-31" %
          sys.argv[0])
    print("example 2 : python %s -l 'Toulouse' -a config.cfg -d 2018-07-01 -f 2018-07-31 --level LEVEL3A" %
          sys.argv[0])
    print("example 3 : python %s --lon 1 --lat 44 -a config.cfg -d 2015-12-01 -f 2015-12-31" %
          sys.argv[0])
    print("example 4 : python %s --lonmin 1 --lonmax 2 --latmin 43 --latmax 44 -a config.cfg -d 2015-12-01 -f 2015-12-31" % sys.argv[
        0])
    print("example 5 : python %s -l 'Toulouse' -a config.cfg -c SPOTWORLDHERITAGE -p SPOT4 -d 2005-12-01 -f 2006-12-31" % sys.argv[
        0])
    print("example 6 : python %s -l 'France' -c VENUS -a config.cfg -d 2018-01-01" % sys.argv[0])
    print("example 7 : python %s -s 'KHUMBU' -c VENUS -a config.cfg -d 2018-01-01" % sys.argv[0])
    print("example 8 : python %s -l 'France' -c LANDSAT -a config.cfg -d 2018-01-01" % sys.argv[0])
    sys.exit(-1)
else:
    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)

    parser.add_option("-l", "--location", dest="location", action="store", type="string",
                      help="town name (pick one which is not too frequent to avoid confusions)", default=None)
    parser.add_option("-s", "--site", dest="site", action="store", type="string",
                      help="Venµs Site name", default=None)
    parser.add_option("-a", "--alternative_config", dest="alternative_config", action="store", type="string",
                      help="alternative configuration file", default=None)
    parser.add_option("-w", "--write_dir", dest="write_dir", action="store", type="string",
                      help="Path where the products should be downloaded", default='.')
    parser.add_option("-c", "--collection", dest="collection", action="store", type="choice",
                      help="Collection within theia collections", choices=['Landsat', 'Landsat57', 'SPOTWORLDHERITAGE', 'SWH1', 'LANDSAT', 'SENTINEL2', 'Snow', 'VENUS'], default='SENTINEL2')
    parser.add_option("-n", "--no_download", dest="no_download", action="store_true",
                      help="Do not download products, just print curl command", default=False)
    parser.add_option("-d", "--start_date", dest="start_date", action="store", type="string",
                      help="start date, fmt('2015-12-22')", default=None)
    parser.add_option("-t", "--tile", dest="tile", action="store", type="string",
                      help="Tile number (ex: T31TCJ), Sentinel2 only", default=None)
    parser.add_option("--lat", dest="lat", action="store", type="float",
                      help="latitude in decimal degrees", default=None)
    parser.add_option("--lon", dest="lon", action="store", type="float",
                      help="longitude in decimal degrees", default=None)
    parser.add_option("--latmin", dest="latmin", action="store", type="float",
                      help="min latitude in decimal degrees", default=None)
    parser.add_option("--latmax", dest="latmax", action="store", type="float",
                      help="max latitude in decimal degrees", default=None)
    parser.add_option("--lonmin", dest="lonmin", action="store", type="float",
                      help="min longitude in decimal degrees", default=None)
    parser.add_option("--lonmax", dest="lonmax", action="store", type="float",
                      help="max longitude in decimal degrees", default=None)
    parser.add_option("-f", "--end_date", dest="end_date", action="store", type="string",
                      help="end date, fmt('2015-12-23')", default=None)
    parser.add_option('-p', '--platform', type='choice', action='store', dest='platform',
                      choices=['LANDSAT5', 'LANDSAT7', 'LANDSAT8', 'SPOT1', 'SPOT2', 'SPOT3', 'SPOT4', 'SPOT5', 'SENTINEL2A', 'SENTINEL2B', 'VENUS'],  help='Satellite',)
    parser.add_option('-m', '--maxcloud', type='int', action='store', dest='maxcloud',
                      default=101,  help='Maximum cloud cover (%)')
    parser.add_option('-o', '--orbitNumber', type='int', action='store', dest='orbitNumber',
                      default=None, help='Orbit Number')
    parser.add_option('-r', '--relativeOrbitNumber', type='int', action='store', dest='relativeOrbitNumber',
                      default=None, help='Relative Orbit Number')
    parser.add_option('--level', type='choice', action='store', dest='level',
                      choices=['LEVEL1C', 'LEVEL2A', 'LEVEL3A'],  help='product level for reflectance products', default='LEVEL2A')
    (options, args) = parser.parse_args()

if options.tile == None:
    if options.location == None and options.site == None:
        if options.lat == None or options.lon == None:
            if options.latmin == None or options.lonmin == None or options.latmax == None or options.lonmax == None:
                print("provide at least a point or  rectangle")
                sys.exit(-1)
            else:
                geom = 'rectangle'
        else:
            if options.latmin == None and options.lonmin == None and options.latmax == None and options.lonmax == None:
                geom = 'point'
            else:
                print("please choose between point and rectangle, but not both")
                sys.exit(-1)
    else:
        if options.latmin == None and options.lonmin == None and options.latmax == None and options.lonmax == None and options.lat == None or options.lon == None:
            if options.location != None:
                geom = 'location'
            elif options.site != None:
                geom = 'site'
        else:
            print("please choose location/site or coordinates, but not both")
            sys.exit(-1)
else:
    if (options.tile.startswith('T') and len(options.tile) == 6):
        tile = options.tile
        geom = 'tile'

    elif (not(options.tile.startswith('T')) and len(options.tile) == 5):
        tile = 'T'+options.tile
        geom = 'tile'
    else:
        print('tile number much gave this format : T31TFJ')

if geom == 'point':
    query_geom = 'lat=%f\&lon=%f' % (options.lat, options.lon)
    dict_query = {'lat': options.lat, 'lon': options.lon}
elif geom == 'rectangle':
    query_geom = 'box={lonmin},{latmin},{lonmax},{latmax}'.format(
        latmin=options.latmin, latmax=options.latmax, lonmin=options.lonmin, lonmax=options.lonmax)
    dict_query = {'box': '{lonmin},{latmin},{lonmax},{latmax}'.format(
        latmin=options.latmin, latmax=options.latmax, lonmin=options.lonmin, lonmax=options.lonmax)}

elif geom == 'location':
    query_geom = "q=%s" % options.location
    dict_query = {'q': options.location}
elif geom == 'tile':
    query_geom = 'location=%s' % tile
    dict_query = {'location': tile}
elif geom == 'site':
    query_geom = 'location=%s' % options.site
    dict_query = {'location': options.site}


if options.start_date != None:
    start_date = options.start_date
    checkDate(start_date)
    if options.end_date != None:
        end_date = options.end_date
        checkDate(end_date)
    else:
        end_date = date.today().isoformat()


# ====================
# read config
# ====================

try:
    config = {}
    f = open(options.alternative_config)
    for line in f.readlines():
        spliteline = line.split('=', 1)
        if len(spliteline) == 2:
            config[spliteline[0].strip()] = spliteline[1].strip()
except IOError as e:
    print("error with config file opening or parsing")
    print(e)
    sys.exit(-2)

config_error = False
cheking_keys = ["serveur", "resto", "login_theia", "password_theia", "token_type"]
if "proxy" in list(config.keys()):
    cheking_keys.extend(["login_proxy", "password_proxy"])

for key_name in cheking_keys:
    if key_name not in list(config.keys()):
        config_error = True
        print(str("error with config file, missing key : %s" % key_name))
if config_error:
    sys.exit(-2)

# =====================
# proxy
# =====================
curl_proxy = ""
if "proxy" in list(config.keys()):
    curl_proxy = str('-x %s --proxy-user "%s:%s"' %
                     (config["proxy"], config["login_proxy"], config["password_proxy"]))


# ============================================================
# get a token to be allowed to bypass the authentification.
# The token is only valid for two hours. If your connection is slow
# or if you are downloading lots of products, it might be an issue
# =============================================================

print("Get theia single sign on token")
get_token = 'curl -k -s -X POST %s --data-urlencode "ident=%s" --data-urlencode "pass=%s" %s/services/authenticate/>token.json' % (
    curl_proxy, config["login_theia"], config["password_theia"], config["serveur"])

# print get_token

os.system(get_token)
print("Done")
token = ""
token_type = config["token_type"]
with open('token.json') as data_file:
    try:
        if token_type == "json":
            token_json = json.load(data_file)
            token = token_json["access_token"]

        elif token_type == "text":
            token = data_file.readline()

        else:
            print(str("error with config file, unknown token_type : %s" % token_type))
            sys.exit(-1)
    except:
        print("Authentification is probably wrong")
        print("check password file")
        print("password should only contain alpha-numerics")
        sys.exit(-1)
os.remove('token.json')

# ====================
# search catalogue
# ====================
if os.path.exists('search.json'):
    os.remove('search.json')

# query=  "%s\&platform=%s\&startDate=%s\&completionDate=%s\&maxRecords=500"\%(query_geom,options.platform,start_date,end_date)

if options.platform != None:
    dict_query['platform'] = options.platform
dict_query['startDate'] = start_date
dict_query['completionDate'] = end_date
dict_query['maxRecords'] = 500


if options.collection == "SENTINEL2" or options.collection == "VENUS":
    dict_query['processingLevel'] = options.level

if options.relativeOrbitNumber != None:
    dict_query['relativeOrbitNumber'] = options.relativeOrbitNumber

if options.orbitNumber != None:
    dict_query['orbitNumber'] = options.orbitNumber


query = "%s/%s/api/collections/%s/search.json?" % (
    config["serveur"], config["resto"], options.collection)+urlencode(dict_query)
print(query)
search_catalog = 'curl -k %s -o search.json "%s"' % (curl_proxy, query)
print(search_catalog)
os.system(search_catalog)
time.sleep(5)


# ====================
# Download
# ====================

with open('search.json') as data_file:
    data = json.load(data_file)

try:
    for i in range(len(data["features"])):
        prod = data["features"][i]["properties"]["productIdentifier"]
        feature_id = data["features"][i]["id"]
        cloudtemp = data["features"][i]["properties"]["cloudCover"]
        if cloudtemp != None:
            cloudCover = int(cloudtemp)
        else:
            cloudCover = 0
        acqDate = data["features"][i]["properties"]["startDate"]
        prodDate = data["features"][i]["properties"]["productionDate"]
        pubDate = data["features"][i]["properties"]["published"]
        print ('------------------------------------------------------')
        print(prod, feature_id)
        print("cloudCover:", cloudCover)
        print("acq date", acqDate[0:14], "prod date", prodDate[0:14], "pub date", pubDate[0:14])

        if options.write_dir == None:
            options.write_dir = os.getcwd()
        file_exists = os.path.exists("%s/%s.zip" % (options.write_dir, prod))
        rac_file = '_'.join(prod.split('_')[0: -1])
        print((">>>>>>>", rac_file))
        fic_unzip = glob.glob("%s/%s*" % (options.write_dir, rac_file))
        if len(fic_unzip) > 0:
            unzip_exists = True
        else:
            unzip_exists = False
        tmpfile = "%s/%s.tmp" % (options.write_dir, prod)
        get_product = 'curl %s -o "%s" -k -H "Authorization: Bearer %s" %s/%s/collections/%s/%s/download/?issuerId=theia' % (
            curl_proxy, tmpfile, token, config["serveur"], config["resto"], options.collection, feature_id)
        print(get_product)
        if not(options.no_download) and not(file_exists) and not(unzip_exists):
            # download only if cloudCover below maxcloud
            if cloudCover <= options.maxcloud:
                os.system(get_product)

                # check if binary product

                with open(tmpfile) as f_tmp:
                    try:
                        tmp_data = json.load(f_tmp)
                        print("Result is a text file")
                        print(tmp_data)
                        sys.exit(-1)
                    except ValueError:
                        pass

                os.rename("%s" % tmpfile, "%s/%s.zip" % (options.write_dir, prod))
                print("product saved as : %s/%s.zip" % (options.write_dir, prod))
            else:
                print("cloud cover too high : %s" % (cloudCover))
        elif file_exists:
            print("%s already exists" % prod)
        elif options.no_download:
            print("no download (-n) option was chosen")

except KeyError:
    print(">>>no product corresponds to selection criteria")
