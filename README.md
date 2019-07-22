# Better manage SABnzbd's history

This script connects to your SABnzbd server via the API. You can query your history and delete all of the entries found. 

The script was written in Python3 and requires the libraries:

- json
- urllib
  
Since they are standard libraries they should come with your python install.

The script has to parameters that you can define beforehand in the source code of the script or upon each run:

- baseurl ie. the address of your SABnzbd server like localhost:8080
- API key which you can find in Config -> General

_If you are planning to use the script more regularly it might be convenient to save your url and key in the config section of the script._

When searching your history you can also use wildcards like "Iggy*Pop" to find strings like "Iggy Pop" and "Iggy.Pop".

Don't worry, the script will ask you to confirm before deleting all the entries found.