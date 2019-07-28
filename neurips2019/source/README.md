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

The biographies of each speaker need to be in folder `bio`, with the name Speaker_Name.bio.html (as found in the custom.json file in the people section {"Speaker Name" : {img...}}).
Spaces are replaced with underscore and the file are .hmtl file to allow links and custom formatting.

### Accepted papers

The accepted papers are retrieved from the`papers_dir` defined in the `custom.json` file.
Here, the different elements are found from the files present in the specified  directory.

In the current structure, they are found in the `accepted/track1`.

This directory contains `pdfs` and `posters` folder and files containing informations about each accepted paper.

For example, `0_aisg_neurips2019.txt`:

```
title:
authors: 
category:  # poster, paper
tag: # health, democracy, etc.
extra: # best paper

```

The name of the pdf files in both the `pdfs` and `posters` folders need to match the name of the .txt file (0_aisg_icml2019.pdf).

The template retrieves all the .txt files in the directory and creates a table dynamically containing the specified information.


#### Requirements :
* python v3
* mako

