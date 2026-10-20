#!/usr/bin/python3

# Before running this, read the README.md.
# This tool is experimental and makes several presumptions
# that are not checked before or during runtime.

from os import listdir
from git import Repo
from datetime import date
from getpass import getuser
from requests import get
from argparse import ArgumentParser

# Preparation: get the working dir
parsedfolder = ArgumentParser(
                 prog='autoChangeCheck_F-KDE',
                 description='Identify KDE-sided or Fedora-sided changes',
                 epilog='Read the README.md before using this!')
parsedfolder.add_argument("working_directory")
folder = parsedfolder.parse_args().working_directory
if folder[0-1] != "/":
    folder = folder + "/"

# see README.md: the tool is not fault tolerant and works
# with many presumptions. The initial try/exception ensures
# that issues end up on the user's "To Do" list, just like
# the changes the tool identifies, but do not rely on the
# assumption that this try/exception will identify any
# potential issue if any of the presumptions of the tool
# is not met, nor that exceptions imply changes.
try:
    # Check if names exist in both sourcegit and distgit
    # Subsequent parts will take place only for folders that exist
    # in both sourcegit and distgit
    packagenames = set(listdir(folder + "sourcegit")) & set(listdir(folder + "distgit"))

    # Determine iterations
    iter = len(packagenames)

    # One iteration for each package
    for x in range(0,iter,1):
        name = packagenames.pop()
        repodist = Repo(folder + "distgit/" + name)
        reposource = Repo(folder + "sourcegit/" + name)

        # distgit part
        distoldcommits = repodist.head.commit
        try:
            rdpulldata = repodist.remotes.origin.pull()
            distnewcommits = repodist.head.commit
        except:
            distnewcommits = "Error"

        # sourcegit part
        sourceoldrefs=reposource.references
        try:
            rspulldata = reposource.remotes.origin.pull()
            sourcenewrefs=reposource.references
        except:
            sourcenewrefs="Error"

        # download-kde part
        pagechanged = 0
        downloadkdebroken = 0
        kdedownlresult = ""
        try:
            kdl = get("https://download.kde.org/stable/release-service/")
            verl = []
            for x in range(0,len(kdl.text.split("\n")),1):
                if "[DIR]" in kdl.text.split("\n")[x]:
                    if "/icons/folder.gif" in kdl.text.split("\n")[x]:
                        if (kdl.text.split("\n")[x][30:37]
                            == kdl.text.split("\n")[x][105:112]):
                            if (kdl.text.split("\n")[x][105:112]
                                == kdl.text.split("\n")[x][115:122]):
                                if "." in kdl.text.split("\n")[x][30:37]:
                                    verl.append(kdl.text.split("\n")[x][30:37])
            if verl == []:
                pagechanged = 1
            verl.sort()
            maxver = verl[0-1]
            numver = len(verl)
            updatefile = 0
            try:
                with open(folder
                          + "kdedownload_previous-versions", "r") as kdc:
                    kdcache=kdc.read()
                oldmaxver=kdcache[2:0-1]
                oldnumver=int(kdcache[0:1])
                if oldnumver != numver:
                    kdedownlresult = "oldnumver != numver"
                    updatefile = 1
                if oldmaxver != maxver:
                    kdedownlresult = "oldmaxver != maxver"
                    updatefile = 1
            except FileNotFoundError:
                updatefile = 1
            if updatefile == 1:
                with open(folder
                          + "kdedownload_previous-versions", "w") as kdc:
                    kdc.write(str(numver) + "\n")
                    kdc.write(maxver + "\n")
        except ValueError:
            downloadkdebroken = 2
        except:
            downloadkdebroken = 1

        # Prepare ToDo files if any change occurred
        # It is assumed the files to be deleted by the users' workflow
        message = str(date.today()) + " NEW ENTRY \n"
        if distoldcommits != distnewcommits:
            if distnewcommits == "Error":
                datad = "Error in pulling distgit"
            else:
                datad = "distoldcommits differs from distnewcommits"
            datad = (datad + " distOLDcommits: " + str(distoldcommits)
                     + " distNEWcommits: " + str(distnewcommits) + "\n")
            message = message + datad
        if sourceoldrefs != sourcenewrefs:
            if sourcenewrefs == "Error":
                datas = "Error in pulling distgit"
            else:
                datas = "sourceoldrefs differs from sourcenewrefs"
            datas = (datas + " sourceOLDrefs " + str(sourceoldrefs)
                     + " sourceNEWrefs " + str(sourcenewrefs) + "\n")
            message = message + datas
        if kdedownlresult != "":
            message = message + kdedownlresult + " \n"
        if pagechanged == 1:
            message = (message + "pagechanged_value_"
                       + str(pagechanged)
                       + " \n")
        if downloadkdebroken > 0:
            message = (message + "downloadkdebroken_value_"
                       + str(downloadkdebroken)
                       + " \n")

        # THE SUBSEQUENT "message" LINE IS FOR THE TESTING PERIOD:
        # DELETE THE TESTING LINE ONCE THE TOOL HAS PROVEN TO WORK!
        # BEGIN TESTING
        message = message + "TESTING: add a line for each invocation!\n"
        # TESTING END

        # Create or append to the ToDo files:
        if message != str(date.today()) + " NEW ENTRY \n":
            with open("/home/"+getuser()+"/Desktop/PackageToDo.txt", "a") as f:
                f.write(message)

except:
    with open("/home/"+getuser()+"/Desktop/PackageToDo.txt", "a") as f:
        f.write("Error, exception 130, check source file \n")
