## ICLR AISG 2019 worskhop website

To compile the website : 
`python compile.py`

The python script uses mako templating package to create the html pages. 
Mako templates allow the usage of python inside the html files which allows for dynamic generation of html.

Two mechanisms are used : 

* Workshop custom informations are defined in the `custom.json` file and values are retrieved to insert 
information inside the different pages.

* Information is retrieved from files found in the directory structure.  Files are read (see code in the templates) 
and the html is generated automatically.  This is used for the schedule and the accepted papers. 
  

### Schedule 

Schedule items are defined in the custom.json file (time and speaker name).  Since writing the title and abstract in
the json file is not user-friendly, these are read from a different file (one per schedule item).

The directory `schedule-items`, contains a file per speaker (event) with the required information.

For example, in `custom.json`  : 
```
 {"time" : "9:00", "speaker_name": "Speaker Name"}
```

in `Spearker_Name.txt` (name needs to be identical to the name entered in the .json)
```
title:Opening remarks
abstract: 
```

The template will look for all the files corresponding to the speaker name and will create an entry for each.

### Accepted papers

The accepted papers are retrieved from the`papers_dir` defined in the `custom.json` file.  
Here, the different elements are found from the files present in the specified  directory.

In the current structure, they are found in the `accepted/track1`. 

This directory contains a `pdfs` folder and files containing informations about each accepted paper. 

For example, `0_aisg_iclr2019.txt`: 

```
title:Example
authors:People Any, And Other, et. al
tag:
```

The pdf file can be specified or by default, is assumed to match the name of the .txt file (0_aisg_iclr2019.pdf).

The template retrieves all the .txt files in the directory and creates a table dynamically containing the specified information.


#### Requirements : 
* python v3
* mako 
  
