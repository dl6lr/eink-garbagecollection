# eink-garbagecalendar

Create an image suitable to be displayed on a SoluM ST-GR29000 ePaper price tag.
The image shows if today or tomorrow a garbage can has to be placed outside for collection. 

# Prerequisites

The python script currently uses Python 3.9.2 with PyYAML 6.0, Pillow 9.3.0, pyowm 3.3.0 and matplotlib 3.6.2
Especially if you run the scripts from cron, make sure the packages are installed in the system, not in the user path only.
Make sure you have the right version installed in the system paths, it is quite confusing if you test the scripts as a regular user and exhibit strange behaviour when run from cron due to different versions installed in the system and user path. Don't ask how I know...

    sudo pip install pyowm Pillow matplotlib pyyaml

# The generated image

A generated image looks similar to the following example:

![collection display](https://github.com/dl6lr/eink-garbagecollection/blob/main/collection.jpg "collection display")

# Configuration

Configuration is done in config.yml that resides beneath owm.py. If you download the package for the first time, copy the sample file to config.yml and edit it.
Paste your OWM API key to config.yml and set your city and country:


    output:
        filename: collection.jpg

    fonts:
        small: fonts/VeraSe12.pil
        big: fonts/VeraSe18.pil

    openepaperlink:
        apip: 192.168.178.30
        mac: 026d29c13b16


Running the script with:

    python garbage.py

should give no error message and the file garbage.jpg should be updated and uploaded to the access point.  The image fits the price tags orientation with the barcode to the left.

