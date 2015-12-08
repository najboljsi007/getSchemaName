# !/usr/bin/python
# author MKnavs

import os, sys, glob
import shutil
import zipfile
import getpass
import biplist
from time import gmtime, strftime
import sys
import subprocess


#----------------SETTINGS-----------------#
saveHistory = "True"
deleteExtractedFolder = "True"
deleteApp = "False"
openHistoryInFinder = "False"
#----------------SETTINGS-----------------#


#Set enconding to utf8 used for extracting files
reload(sys)
sys.setdefaultencoding('utf8')

#Saves all schemes into list
schemesList = []
schemeNameNotExists = False


while 1:
#Set and Reset package counter
    packageCounter = 0

#Clear screen and get computer username and change dir
    os.system('clear')
    computer_username = getpass.getuser()
    mobileApplicationspath = "/Music/iTunes/iTunes Media/Mobile Applications/"
    workingDirPath = "/Users/" + computer_username + "/Music/iTunes/iTunes Media/Mobile Applications/"
    os.chdir(workingDirPath)


#listing  .ipa files in directory
    print ("Available packages:\n")
    file_list = glob.glob("*.ipa")
    # if file_list is :
    # 	print("No packages are available...\n")
    for i,file_ipa in enumerate(file_list):
        packageCounter =+ 1
        print "[%i] %s" % (i, file_ipa)

    if packageCounter == 0:
        print "No packages available. Download new apps via iTunes ...\n"

#Additional selection X - History
    print "[X] URL Schemes History"

#Enter number of the package
    appNum = raw_input("\nEnter the number of the package: ")

#Open history
    try:
        if appNum == "x" or appNum == "X":
            if openHistoryInFinder != "True":
                os.system("open /Users/" + computer_username + "/Music/iTunes/iTunes\ Media/Mobile\ Applications/URLSchemesHistory.txt")
            else:
                subprocess.call(["open", "-R", workingDirPath + "URLSchemesHistory.txt"])
            sys.exit()
    except ValueError:
        print "History does not exist yet or some error occurred ..."
        sys.exit()

#Start unziping process
    appName = file_list[int(appNum)]
    appNameNew = appName + ".zip"
    extractedFolderPath = "/Users/" + computer_username + "/Music/iTunes/iTunes Media/Mobile Applications/" + appName + " Extracted"

#Create new folder for extracting
    os.mkdir(extractedFolderPath, 0755);
    payloadPath = extractedFolderPath + "/Payload/"

#Converting .ipa to .zip
    print("Converting to .zip format ...")
    os.rename(appName,appNameNew)

#Extracting .zip file
    print ("Successfully converted! Extracting ...\n")
    zfile = zipfile.ZipFile(appNameNew)
    zfile.extractall(extractedFolderPath)

#Open .txt file for storing CFBundleURLSchemes
    storeFile = open("URLSchemesHistory.txt", 'a')


#Get URL Schemes and blacklist which are not correct
    blacklist = ["CFBundleURLName", "CFBundleTypeRole", "SchemeType"]

#Timestamp for history .txt
    runTimestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

#Search for Scheme name and write to file
    print("|---- SCHEME NAME and BUNDLE ID FOR %s: -----|\n" %appName)
    os.chdir(payloadPath)
    for file_app in glob.glob("*.app"):
        plist_path = payloadPath + file_app + "/Info.plist"
        parsed_plist = biplist.readPlist(plist_path)
#Try to find Schema name, if not, print error
        try:
            for i in parsed_plist["CFBundleURLTypes"]:
                for h in i.keys():
                    if h not in blacklist:
                        print "%s : %s" % (h, str(i[h]))
                        schemesList.append(str(i[h]))

        except KeyError:
            print "CFBundleURLTypes does not exist for selected app!"
            schemeNameNotExists = True

#Print BundleId
        os.chdir(extractedFolderPath)
        metaDataPlist = extractedFolderPath + "/iTunesMetadata.plist"
        parsed_plist_metadata = biplist.readPlist(metaDataPlist)
        print ("\nBundleID: " + parsed_plist_metadata["softwareVersionBundleId"])

#Save info to history - saveHistory -settings:
        if saveHistory != "False":
            storeFile.write(runTimestamp + "\n")
            storeFile.write("|----- SCHEME NAME and BUNDLE ID FOR %s: -----|\n" %appName)
            if schemeNameNotExists == False:
                storeFile.write("Scheme names: ")
                storeFile.write("\n              ".join(schemesList))
            else:
                storeFile.write("CFBundleURLTypes does not exist for selected app!\n")
            storeFile.write("\nBundleID: " + parsed_plist_metadata["softwareVersionBundleId"] + "\n\n")

#Remove extracted dir - deleteExtractedFolder = False -settings
    if deleteExtractedFolder == "True":
        shutil.rmtree(extractedFolderPath)

#Remove downloaded app .ipa file - deleteApp -settings
    if deleteApp == "True":
       os.remove(workingDirPath + appNameNew)



    print("\n")
    storeFile.write("\n")
    storeFile.close()
    raw_input("\nPress Enter key to continue.")
