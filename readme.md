Author: Macleay Stephenson, Australian Synchrotron
Date: 30/10/2015

This tool is used to:-

	- Validate the configuration of a GBLV across multiple axis files(*.e.pmc).
	- Produce a motor record for application a beamlines EPICS configuration.
	- Produce an asbuilt motor list for reference of configuration of beamlines.
    - Produce labels for both cables and GBLV front panel.

Requires:-

	- Anaconda 3.4(Python distribution) https://www.continuum.io/downloads
    
    Install Anaconda and ensure that python is added the the PATH variable. This enables the use of "python" in cmd.exe. 

Instructions:-
    - This tool is designed to work with Xmodel e.pmc files created from version 7. 
    - Place all the files in one location. Shift + Right click to open a command window in that folder.
    - Output files are located in the location that the program is run from.
	- Run 'Configuration validation tool.py' with python from the command line.
        "python Configuration validation tool.py"
	- Information that you may require:-
        - Location of the 'Master.pmc' or the parent directory.(Multiple Master.pmc files can be analysed by providing the parent directory.)
        - 'st.cmd' of the relevant controller
    - Tools:-
        - '1' the E.pmc Configuration Cross Check tool
        - '2' the EPICS motor record tool.
        - '3' the Cable label tool.
        - '4' the GBLV Front Panel Labels tool.
        - '5' the Motor List tool.
    - Errors can be read in the logfile.txt.
    
    
E.pmc Configuration Cross Check tool:

This tool cross checks variables in the e.pmc files that may overwrite variables in other related axis. Such conflicts can happen at a GBLV level and also at a channel level within the GBLV. The output file is a list of all the available variables on that controller and the condition of that variable, be it healthly, unhealthly etc. 

EPICS motor record:
This tool outputs a text block, comma value separated, that can be placed in an IOC's st.cmd or similar to configure the IOC. This string requires some editing since there are some default values. 

The default values are: 
    -ADEL = 0.1
    -BACC = 0.2
    -BDST = 0.1
    -BVEL = 1
    -DIR = 0
    -DHLM = 0
    -DLLM = 0
    -PREC = 3
    -RDBD = 0
    -TWV = 0
    -UEIP = 0
    -VELO = 1
    -OFF = 0
    -DESC = '*Description*'
    
Cable and GBLV label tools:

The cable label tool outputs a file that is able to be used with the Brady Labelling machine, the BMP-71 with the correct labels, instructions can be found on Confluence here.

    https://confluence.synchrotron.org.au/pages/viewpage.action?pageId=2788677

The GBLV label tool outputs a .csv file that can be imported to P.touch Editor 5.1 for use with the PT-2730 labelling machine. I was unable to create a layout that automatically enables printing. Using the layout file(Ptouch Layout template.lbx) provided with the tool it is possible to open the P.Touch software, select the database that you have just created and then merge the fields with the wizard. Then, when printing, select "Print all records". Now the program will print all the records.

Motor list:

The motor list tool outputs a csv file that reflects the asbuilt nature of the instrument. 