# ISO Dummyfier

This script will convert files inside an ISO image into dummy files. The reason for this is to make the image smaller after compressing, like for example converting the update files in a PSP ISO into emtpy files to reduce the CSO size.

It works just replacing the file data by zeroes. It doesn't recreate the ISO file in any way, so keep a backup of the input file.