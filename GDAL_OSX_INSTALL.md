## Install libgdal on OSX

If you are getting errors on startup about missing libGDAL, the following steps helped me:
```
$ brew install gdal
$ pip install psycopg2
$ excport GDAL_LIBRARY_PATH=/usr/local/Cellar/gdal/2.4.2/lib/libgdal.20.dylib 
$ createdb cykel
$ export DATABASE_URL="postgis:///cykel"
$ ./manage.py migrate
```
