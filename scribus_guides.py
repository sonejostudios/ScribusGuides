#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

try:
    import scribus
except ImportError,err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)



#############################################################



layout_text = """
Create new guides :

1 = around page
2 = around selected object
---
0 = delete all guides

"""



def main(argv):
    unit = scribus.getUnit()
    units = ['pts','mm','inches','picas','cm','ciceros']
    unitlabel = units[unit]
    
# get page size
    xysize = scribus.getPageSize()

    
# ask for layout style
    layout_style = scribus.valueDialog("Guides Layout", layout_text, "1")
    if layout_style == "":
        sys.exit()
        

# 0 = erase all guides
    if layout_style == "0":
        #guides
        scribus.setVGuides([])
        scribus.setHGuides([])
        sys.exit()


# 1 = guides around page
    if layout_style == "1":
        # set guides distance
        pageguides_str = scribus.valueDialog("Create Guides around Page", "Set distance to page borders ("+unitlabel+") :\n\n- positive (e.g. 3) for page margin\n\n- negative (e.g. -3) for page bleed\n", "3")
        if pageguides_str != "":
            pageguides = float(pageguides_str)
        else:
            sys.exit()
    
        #set guides
        scribus.setVGuides(scribus.getVGuides() + [pageguides, xysize[0]-pageguides])
        scribus.setHGuides(scribus.getHGuides() + [pageguides, xysize[1]-pageguides])
        

# 2 = guides around selected object
    if layout_style == "2":
        # set guides distance
        objectguides_str = scribus.valueDialog("Create Guides around selected Objects", "Set distance to object borders ("+unitlabel+") :\n\n- 0 for around the object borders\n\n- positive (e.g. 3) towards inside the object\n\n- negative (e.g. -3) towards outside the object\n", "0")
        if objectguides_str != "":
            objectguides = float(objectguides_str)
        else:
            sys.exit()
            
        if scribus.selectionCount() == 0:
            scribus.messageBox("Error", "Select an object first !", icon=scribus.ICON_WARNING)
            sys.exit()
            
        #get selected object
        selection_name = scribus.getSelectedObject(0)
        objectpos = scribus.getPosition(selection_name)
        objectsize = scribus.getSize(selection_name)
        
        #set guides
        scribus.setVGuides(scribus.getVGuides() + [objectpos[0]+objectguides, objectpos[0]+objectsize[0]-objectguides])
        scribus.setHGuides(scribus.getHGuides() + [objectpos[1]+objectguides, objectpos[1]+objectsize[1]-objectguides])


#############################################################


def main_wrapper(argv):
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        # Exit neatly even if the script terminated with an exception,
        # so we leave the progress bar and status bar blank and make sure
        # drawing is enabled.
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()


# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
    main_wrapper(sys.argv)


