# theia_download

This is a simple piece of code to automatically download the products provided by Theia land data center : https://theia.cnes.fr. It can download the products delivered by Theia, such as the [Sentinel-2 L2A products] (http://www.cesbio.ups-tlse.fr/multitemp/?page_id=6041), [Landsat L2A products](http://www.cesbio.ups-tlse.fr/multitemp/?page_id=3487) and the [SpotWorldHeritage L1C products](https://www.theia-land.fr/en/projects/spot-world-heritage).

This code was written thanks to the precious help of one my colleague at CNES [Jérôme Gasperi](https://www.linkedin.com/pulse/rocket-earth-your-pocket-gasperi-jerome) who developped the "rocket" interface which is used by Theia, and the mechanism to get a token. It was then adapted by Dominique Clesse for the new Muscate interface to download Sentinel-2 products.

This code has been tested with python 2.7 and python 3.6. It relies on the curl utility. *Installing curl is therefore a prerequisite*. It has been developped and tested on Linux. It might work on windows, but I cannot test it. To use the code, you need to have an account and a password [at theia](http://theia.cnes.fr/atdistrib), and you need to add it to the config file as explained in the authentification paragraph.

## Examples for various sensors
If you have an account at theia, you may download products using command lines like 

- `python ./theia_download.py -l 'Toulouse' -c SENTINEL2 -a config_theia.cfg -d 2016-09-01 -f 2016-10-01`

 which downloads the SENTINEL-2 products above Toulouse, acquired in September 2016.
 
 - `python ./theia_download.py -l 'Toulouse' -c SENTINEL2 -a config_theia.cfg -d 2016-09-01 -f 2016-10-01 -m  50`

 which downloads the SENTINEL-2 products above Toulouse, acquired in September 2016 with less than 50% cloud cover

- `python ./theia_download.py -l 'Toulouse' -c LANDSAT -a config_theia.cfg -d 2019-01-01 -f 2019-02-01`

 which downloads the LANDSAT-8 products above Toulouse, acquired in January 2019.
 
 - `python ./theia_download.py -l 'Toulouse' -c Landsat -a config_theia.cfg -d 2016-09-01 -f 2016-10-01`

 which downloads the LANDSAT-8 products, with the old MUSCATE format above Toulouse, acquired in September 2016.

- `python ./theia_download.py -l 'France' -c VENUS -a config_theia.cfg -d 2019-01-01 -f 2019-02-01`

 which downloads the VENUS products from all sites in France, acquired in January 2019.
 
 - `python ./theia_download.py -s 'KHUMBU' -c VENUS -a config_theia.cfg -d 2019-01-01 -f 2019-02-01`

 which downloads the VENUS products above KHUMBU site, acquired in January 2019.

- `python ./theia_download.py -l 'Yaounde' -c SPOTWORLDHERITAGE -a config_theia.cfg -d 2012-01-01 -f 2013-01-01`

 
 - `python ./theia_download.py -l 'Toulouse' -c SWH1 -a config_theia.cfg -d 2006-01-01 -f 2007-01-01`

 which downloads the SPOT World Heritage products old format above Toulouse, acquired in 2006.

 - `python ./theia_download.py -l 'Foix' -c Snow -a config_theia.cfg -d 2016-11-01 -f 2016-12-01`

 which downloads the Theia snow products above Foix (Pyrenees), acquired in November 2016. The collection option is case sensitive.



## Other options

- `python ./theia_download.py -t T31TCJ -c SENTINEL2 -a config_theia.cfg -d 2016-09-01 -f 2016-10-01`

 which downloads the SENTINEL-2 products above tile T31TCJ, acquired in September 2016. 

- `python ./theia_download.py --lon 1 --lat 43.5 -c Landsat -a config_landsat.cfg -d 2015-11-01 -f 2015-12-01`

 which downloads the LANDSAT 8 products above --lon 1 --lat 43.5 (~Toulouse), acquired in November 2015.

- `python ./theia_download.py --lonmin 1 --lonmax 2 --latmin 43 --latmax 44 -c Landsat -a config_landsat.cfg -d 2015-11-01 -f 2015-12-01`

 which downloads the LANDSAT 8 products in latitude, longitude box around Toulouse, acquired in November 2015.

- `python theia_download.py -l 'Toulouse' -a config_landsat.cfg -c SPOTWORLDHERITAGE -p SPOT4 -d 2005-11-01 -f 2006-12-01`

which downloads the SPOTWORLDHERITAGE products acquired by SPOT5 in 2005-2006
 
- `python ./theia_download.py -c SENTINEL2 -t T31TCJ -r 51 d 2017-01-01 -f 2018-01-01`

which downloads the SENTINEL2 T31TCJ tile, with the relative Orbit Number 51, acquired in 2017.


## Authentification 

The config file  config_landsat.cfg or  config_landsat.cfg  must contain your email address and your password as in the examples provided.

If you need to go through a proxy, and if you have not configured your proxy variable (`export http_proxy=http://moi:secret@proxy.mycompany.fr:8050`), you may also use one of the files like config_theia_proxy.cfg or config_landsat_proxy.cfg and add your passwords in them.

The program first fetches a token using your email address and password, and then uses it to download the products. As the token is only valid for two hours, it is advised to request only a reasonable number of products. It is necessary to make a first download from the site manually in order to validate your accound and the licence in the case of SPOTWORLDHERITAGE.

## Alternatives

The EODAG tool has an interface to download data from Theia, PEPS, and many others, and it is probably much more professional code. You might give it a try.

https://eodag.readthedocs.io/en/latest/#

https://github.com/CS-SI/eodag
