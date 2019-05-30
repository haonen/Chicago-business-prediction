#!/bin/bash
# Data loading
echo "merge 2014 data"
python3 geo_link.py --year 2014 --number 10000;

for f in *.csv;

do echo "uploading $f to google drive" 
   gdrive upload --parent 1n2umwVLx97bLSVfrNQ4oOMV3qv2voL8I $f;
   echo "removing $f";
   rm $f;
done

echo "merge 2015 data"
python3 geo_link.py --year 2015 --number 10000;

for f in *.csv;

do echo "uploading $f to google drive" 
   gdrive upload --parent 1n2umwVLx97bLSVfrNQ4oOMV3qv2voL8I $f;
   echo "removing $f";
   rm $f;
done

echo "merge 2016 data"
python3 geo_link.py --year 2016 --number 10000;

for f in *.csv;

do echo "uploading $f to google drive" 
   gdrive upload --parent 1n2umwVLx97bLSVfrNQ4oOMV3qv2voL8I $f;
   echo "removing $f";
   rm $f;
done

echo "merge 2017 data"
python3 geo_link.py --year 2017 --number 10000;

for f in *.csv;

do echo "uploading $f to google drive" 
   gdrive upload --parent 1n2umwVLx97bLSVfrNQ4oOMV3qv2voL8I $f;
   echo "removing $f";
   rm $f;
done

echo "merge 2018 data"
python3 geo_link.py --year 2018 --number 10000;

for f in *.csv;

do echo "uploading $f to google drive" 
   gdrive upload --parent 1n2umwVLx97bLSVfrNQ4oOMV3qv2voL8I $f;
   echo "removing $f";
   rm $f;
done

echo "Done"
