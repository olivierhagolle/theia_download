import json
import time
import os, os.path, optparse,sys


###########################################################################
class OptionParser (optparse.OptionParser):
 
    def check_required (self, opt):
      option = self.get_option(opt)
 
      # Assumes the option's 'default' is set to None!
      if getattr(self.values, option.dest) is None:
          self.error("%s option not supplied" % option)
 
###########################################################################

#==================
#parse command line
#==================
if len(sys.argv) == 1:
    prog = os.path.basename(sys.argv[0])
    print '      '+sys.argv[0]+' [options]'
    print "     Aide : ", prog, " --help"
    print "        ou : ", prog, " -h"
    print "example python  %s -q 'Toulouse 2014' -a auth_theia.txt"%sys.argv[0]
    sys.exit(-1)
else:
    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)
  
    parser.add_option("-q","--query", dest="query", action="store", type="string", \
            help="query : example Toulouse 2013",default=None)		
    parser.add_option("-a","--auth_theia", dest="auth_theia", action="store", type="string", \
            help="Theia account and password file")
    parser.add_option("-w","--write_dir", dest="write_dir", action="store",type="string",  \
            help="Path where the products should be downloaded",default='.')
    parser.add_option("-c","--colelction", dest="collection", action="store",type="string",  \
            help="Colection within theia collections",default='Landsat')

    (options, args) = parser.parse_args()



#====================
# read authentification file
#====================
try:
    f=file(options.auth_theia)
    (email,passwd)=f.readline().split(' ')
    if passwd.endswith('\n'):
        passwd=passwd[:-1]
    f.close()
except :
    print "error with password file"
    sys.exit(-2)
query=options.query.replace(" ","%20")

#============================================================
# get a token to be allowed to bypass the authentification.
# The token is only valid for two hours. If your connection is slow
# or if you are downloading lots of products, it might be an issue
#=============================================================

get_token='curl -k -s -X POST --data-urlencode "ident=%s" --data-urlencode "pass=%s" https://theia.cnes.fr/services/authenticate/>token.json'%(email,passwd)

os.system(get_token)

with open('token.json') as data_file:    
    token_json = json.load(data_file)
    token=token_json["access_token"]

#====================
# search catalogue
#====================

if os.path.exists('search.json'):
    os.remove('search.json')
    
search_catalog='curl -k -o search.json "https://theia.cnes.fr/resto/api/collections/Landsat/search.json?q=%s\&maxRecords=500"'%query
print search_catalog
os.system(search_catalog)
time.sleep(10)


#====================
# Download
#====================

with open('search.json') as data_file:    
    data = json.load(data_file)

for i in range(len(data["features"])):    
    print data["features"][i]["properties"]["productIdentifier"],data["features"][i]["id"],data["features"][i]["properties"]["startDate"]
    prod=data["features"][i]["properties"]["productIdentifier"]
    feature_id=data["features"][i]["id"]
    get_product='curl -o %s.zip -k -H "Authorization: Bearer %s" https://theia.cnes.fr/resto/collections/Landsat/%s/download/?issuerId=theia'%(prod,token,feature_id)
    os.system(get_product)

