# !/usr/bin/python
# author MKnavs

import os, sys, glob
import zipfile
import getpass
import biplist
from time import gmtime, strftime
import subprocess

#Set enconding to utf8 used for extracting files
reload(sys)
sys.setdefaultencoding('utf8')

while 1:
#Set and Reset package counter
    packageCounter = 0

#Clear screen and get computer username and change dir
    os.system('clear')
    computer_username = getpass.getuser()
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

#If x selected, open history in finder
    print "[X] URL Schemes History"

#Enter number of the package
    appNum = raw_input("\nEnter the number of the package: ")
#Open history
    try:
        if appNum == "x" or appNum == "X":
#Uncomment to directly open Scheme History
            os.system("open /Users/" + computer_username + "/Music/iTunes/iTunes\ Media/Mobile\ Applications/URLSchemesHistory.txt")
#Uncomment to open in Finder
            #subprocess.call(["open", "-R", workingDirPath + "URLSchemesHistory.txt"])
            break
    except ValueError:
        break

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
    blacklist = ["CFBundleURLName", "CFBundleTypeRole"]

#Timestamp for history .txt
    runTimestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

#Search for Scheme name and write to file
    storeFile.write(runTimestamp + "\n")
    print("|---- SCHEME NAME and BUNDLE ID FOR %s: -----|\n" %appName)
    storeFile.write("|----- SCHEME NAME and BUNDLE ID FOR %s: -----|\n" %appName)
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
                        storeFile.write("%s : %s\n" % (h, str(i[h])))
        except KeyError:
            print "CFBundleURLTypes does not exist for selected app!"
            storeFile.write("CFBundleURLTypes does not exist for selected app!\n")

 #Print BundleId
        os.chdir(extractedFolderPath)
        metaDataPlist = extractedFolderPath + "/iTunesMetadata.plist"
        parsed_plist_metadata = biplist.readPlist(metaDataPlist)
        print ("BundleID: " + parsed_plist_metadata["softwareVersionBundleId"])
        storeFile.write("BundleID: " + parsed_plist_metadata["softwareVersionBundleId"] + "\n\n")


    print("\n")
    storeFile.write("\n")
    storeFile.close()
    raw_input("\nPress Enter key to continue.")
