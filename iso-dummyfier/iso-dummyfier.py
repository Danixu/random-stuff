#!/usr/bin/env python3

"""
    This program will read all the ISO files into the to_process folder
    and will convert the indicated files into dummy files to save space
    when compressed.
"""

#  Copyright (C) 2022 Daniel Carrasco
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

import iso9660

scriptFolder = os.path.dirname(os.path.realpath(__file__))

filesToConvertIntoDummy = [
    "/PSP_GAME/SYSDIR/UPDATE/DATA.BIN",
    "/PSP_GAME/SYSDIR/UPDATE/EBOOT.BIN"
]

# Get all the ISO files in "to_process" folder
fileList = []
for file in os.listdir(os.path.join(scriptFolder, "to_process")):
    if file.endswith(".iso"):
        fileList.append(os.path.join(scriptFolder, "to_process", file))


# Prepare an script of the files position in ISO to be removed later
dummy_list = {}
for isoFile in fileList:
    iso = iso9660.ISO9660.IFS(source=isoFile)

    if not iso.is_open():
        print("Sorry, couldn't open %s as an ISO-9660 image." % iso_image_fname)
    else:
        dummy_list[isoFile] = {}
        for dummyFile in filesToConvertIntoDummy:
            file_stat = iso.stat(dummyFile)

            if file_stat:
                dummy_list[isoFile][dummyFile] = {
                    "file_position": file_stat["LSN"] * 2048,
                    "file_size": file_stat["size"]
                }

        iso.close()


# Rewrite the files inside the ISO to turn it into dummies
for file, fileData in dummy_list.items():
    print(f"Replacing files in '{file}' with dummy data.")
    try:
        with open(file, "r+b") as iso_write:
            for dummy, dummy_data in fileData.items():
                print(f"\t{dummy}")
                iso_write.seek(dummy_data["file_position"])

                current_size = 0
                while current_size < dummy_data["file_size"]:
                    to_write = dummy_data["file_size"] - current_size
                    if to_write > 2048:
                        to_write = 2048
                    
                    iso_write.write(b'\0' * to_write)
                    
                    current_size += to_write

    except Exception as e:
        print(f"There was an error processing the file: {e}")