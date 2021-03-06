# Cube Message Processor
___
Community project to monitor discord activity on the official CubeCraft discord server. 
And with community I mean, me Fesa D:
___
## Installing
You'll simply have to clone the repository to your local storage. 
```git
cd <your folder>

git clone https://github.com/Fesaa/cube-msg-processor
```
You also need a custom module made by to select the wanted options from within the terminal;
```git
# Windows
py -m pip install git+https://github.com/Fesaa/CommandLineOptions

# macOS/Linux
python3 -m pip install git+https://github.com/Fesaa/CommandLineOptions
```
And three other "normal" modules:
```git
# Windows
py -m pip install requests
py -m pip install matplotlib
py -m pip install tkcalendar

# macOS/Linux
python3 -m pip install requests
python3 -m pip install matplotlib
python3 -m pip install tkcalendar
```
Lastly, remove ```.example``` from ```config.json.example```, and edit the file if you want. More info on this below!
___
## CubeCraft specific
If you're using the program to create graphs on Cube statistics. You'll be using the data provided in the repository. And thus also its `external_id_cache.json`. If you're not using this, you'll want to remove all files from `/input`, delete `external_id_cache.json` and remove `external_id_cache.json.example` to `external_id_cache.json`. You **need** to give a bot token if you're using your own cache. If you the input files provided by the repository, the cache will always contain all needed ids.
___
## Usage (Terminal)
Once you've cloned the repository and installed the needed modules. You can start making graphs with the data in ```processor/input/```. 
Graphs will always be saved in ```out```, an example can be found there.
And are only shown if you enable to option before running the file. A most basic example would be
```git 
#Windows
py main.py FileName=processor/input/legancy_staff_help.csv,processor/input/174845164899139584.csv StaffHelp=True

#macOS/Linux
python3 main.py FileName=processor/input/legancy_staff_help.csv,processor/input/174845164899139584.csv StaffHelp=True
```
This will return the default graphs in for staff help. The tag ```StaffHelp=True``` **must** be given if you want to monitor staff help.

Some handy flags:
* ```Path``` use all files in a certain folder. 
* ```Exclude``` used in combination with ```Path``` to skip over certain files in a folder.
   * Note: Can be used with ```FileName``` but would be redundant as you can just not give the file name in the first place.
   * Example:
      * Would displayed information for all channels except staff help.
   ```git 
   py main.py Path=processor/input/ Exclude=processor/input/legancy_staff_help.csv,processor/input/174845164899139584.csv
   ```
      

* ```User``` used to get an users stats. Will force which graphs are displayed.
   * Example: 
       * Would displayed information for ```Eva#1337```
   ```git
   python3 main.py Path=processor/input/ Exclude=processor/input/legancy_staff_help.csv,processor/input/174845164899139584.csv User=322007790208155650
   ```
     

* ```MinMsg & MinTime``` used to limit the amount of users on the graphs. Will cause for less clutter and better readability.
   * Note: The total list will always be printed to your terminal.
   * Example: 
      * Would only display staff members with at least ```500``` messages in staff help and ```3``` hour spend in it.
      ```git
      python3 main.py FileName=processor/input/legancy_staff_help.csv,processor/input/174845164899139584.csv StaffHelp=True MinMsg=500 MinTime=3
      ```
      
* ```ShowGraphs``` displays graphs in a python window after computation.
   * Note: Graphs will always be saved.
   * Example: 
   ```git
   py main.py Path=processor/input/ ShowGraphs=True
   ```

All the flags are, these are made in ```init.py``` if you're interested;
* FileName
* Path
* Exclude
* Daily
* ConsecutiveTime
* TotalMessages
* ReplyTimes
* DailyMessages
* RoleDistribution
* HourlyActivity
* IgnoreMessages
* Percentages
* StartDate
* EndDate
* User
* MinMsg
* MinTime
* UpdateJson
* FigName
* ShowGraphs
* Accurate
* StaffHelp

A more detailed list of flags can be obtained with;
```git
#Windows
py main.py --options

#macOS/Linux
python3 main.py --options
```
___
# Usage (GUI)
You're also able to use a horrible looking GUI by simply running 
```git
# Windows
py main.py

# macOS/Linux
python3 main.py
````
Instructions will reside in the GUI!
___
# Username cache & Bot Token
Use your bot token as follows: `Bearer TOKEN` where `TOKEN` is your specific token. It is recommend to always use the cache to save API requests and not waste time waiting for rate limits.

___
## HELP!
Just ping me in english general, I'll reply sooner or later :D

___
## Contribution, Bugs and Feature request
You're always free to open a pull request, Issue if you want to see something changed. 
Feel free to just tag me in the discord as well but I might forget that way :p
