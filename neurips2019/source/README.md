## NeuRIPS Joint AISG 2019 Worskhop Website

#### Do not modify the html directly as your changes will be overidden 
#### Modify these sources

To compile the website and generate the .html pages:
`python compile.py`

The python script uses mako templating package to create the html pages.
Mako templates allow the usage of python inside the html files which allows for dynamic generation of html.

Two mechanisms are used :

* Workshop custom informations are defined in the `custom.json` file and values are retrieved to insert
information into the different pages.

* Information is retrieved from files found in the directory structure.  Files are read (see code in the templates)
and the html is generated automatically.  This is used for the schedule and the accepted papers pages.


### Schedule

Schedule items are defined in the `custom.json` file.  Since writing the title and abstract in
the json file is not user-friendly, these are read from a different .txt file (one per schedule item).

The directory `schedule-items`, contains a .txt file per event (time) with the required information.

In `custom.json`  :
```
  {"id": "aisg_neurips2019_0",  "time": "", "speaker_name": []}
```

In `aisg_neurips2019_0.txt` 
```
title:Opening remarks
abstract:
```

The `speaker_name` list contains the name of the speakers. They need to be identical to the names in the `people` section as `compile.py` will look for bio files (see below) corresponding to the speaker name and will create an entry for each.  

The biographies of each speaker need to be in folder `bio`, with the name "Speaker_Name.bio.html" (as found in  `custom.json` in the people section {"Speaker Name" : {img...}}). Spaces are replaced with underscore and the files are .html to allow the presence of links and custom formatting.

### Accepted papers

The accepted papers information are retrieved from the `papers_dir` defined in the `custom.json` file.
Here, the different elements are read from the .txt files present in the specified  directory.

In the current structure, they are found in the `accepted/track1`.

This directory contains `pdfs` and `posters`. That is where the camera ready and posters (in pdfs) are organized.

For example, in `accepted/track1/`, `0_aisg_neurips2019.txt` contains the following field :

```
title:
authors: 
category:  # poster, paper
tag: # health, democracy, etc.
extra: #  [optional], for example best paper 

```

The name of the pdf files in both the `pdfs` and `posters` folders need to match the name of the .txt file (0_aisg_neurips2019.pdf).

The script retrieves all the .txt files in the directory and creates a table dynamically containing the specified information.


#### Requirements :
* python v3
* mako

