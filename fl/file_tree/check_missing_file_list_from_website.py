# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:01:27 2023

@author: iant


ANALYSE LIST OF MISSING FILES AND FIND THE REASON

"""

import os
import h5py
import glob
import re
from datetime import datetime
import sys

sys.path.append(r"C:\Users\iant\Dropbox\NOMAD\Python")
from tools.file.paths import paths
from tools.pipeline.make_reprocess_command import make_reprocess_command
from tools.general.progress_bar import progress

input_filepath = r"upload\missing.txt"

with open(input_filepath, "r") as f:
    missing_file_data = f.readlines()
    
h5_exectimes = [s.split(",")[0].strip() for s in missing_file_data]
h5_obstypes = [s.split(",")[1].strip() for s in missing_file_data]
h5_channels = [s.split(",")[2].strip() for s in missing_file_data]
h5_prefixes = [s.split(",")[3].strip() for s in missing_file_data]

no_h5_ixs = [i for i,s in enumerate(h5_prefixes) if s == "NULL"]

print("There are %i missing files, of which %i are missing completely" %(len(h5_prefixes), len(no_h5_ixs)))


last_obs_dt = datetime(2023, 3, 16)


#need fixing
# 20221011_024508 LNO Phobos no obs type letter found
# 20230127_113451 LNO Phobos no obs type letter found
# 20230217_074121 LNO Phobos no obs type letter found
# 20230223_011421 LNO Phobos no obs type letter found
# 20230225_220121 LNO Phobos no obs type letter found
# 


def check_known_errors(h5_prefix):

    known_errors = {
    "20180616_204825":"LNO occultation test",
    
    "20190404_215749":"UVIS transmittance not accepted",
    "20190419_102536":"UVIS transmittance not accepted",
    "20190429_151950":"UVIS transmittance not accepted",

    "20190616_041757":"TGO temperatures missing",
    "20190616_055622":"TGO temperatures missing",

    "20190617_035259":"TGO temperatures missing",
    "20190617_064705":"TGO temperatures missing",

    "20201123_100227":"TGO temperatures missing",
    "20201123_111046":"TGO temperatures missing",
    "20201123_114607":"TGO temperatures missing",

    "20211124_194131":"TGO temperatures missing",
    "20211124_200017":"TGO temperatures missing",
    "20211124_233720":"TGO temperatures missing",

    "20220202_202310":"TGO temperatures missing",
    "20220202_210033":"TGO temperatures missing",
    "20220202_212210":"TGO temperatures missing",

    "20220223_181351":"TGO temperatures missing",
    "20220223_183753":"TGO temperatures missing",

    "20220225_141613":"TGO temperatures missing",

    "20220405_012049":"TGO temperatures missing",
    "20220405_015736":"TGO temperatures missing",
    "20220405_022111":"TGO temperatures missing",
    "20220405_051701":"TGO temperatures missing",
    "20220405_055333":"TGO temperatures missing",
    "20220405_071502":"TGO temperatures missing",
    "20220405_075129":"TGO temperatures missing",
    "20220405_111100":"TGO temperatures missing",
    "20220405_114713":"TGO temperatures missing",
    "20220405_121110":"TGO temperatures missing",
    "20220405_150700":"TGO temperatures missing",
    "20220405_154302":"TGO temperatures missing",
    "20220405_193855":"TGO temperatures missing",
    "20220405_210110":"TGO temperatures missing",
    "20220405_213652":"TGO temperatures missing",
    "20220405_234907":"TGO temperatures missing",
    "20220406_013234":"TGO temperatures missing",
    "20220406_045314":"TGO temperatures missing",
    "20220406_052828":"TGO temperatures missing",
    "20220406_055307":"TGO temperatures missing",
    "20220406_084922":"TGO temperatures missing",
    "20220406_092418":"TGO temperatures missing",
    "20220406_104722":"TGO temperatures missing",
    "20220406_112211":"TGO temperatures missing",
    "20220406_114708":"TGO temperatures missing",
    "20220406_144322":"TGO temperatures missing",
    "20220406_151758":"TGO temperatures missing",
    "20220406_211148":"TGO temperatures missing",
    "20220406_213710":"TGO temperatures missing",

    "20220424_081812":"TGO temperatures missing",

    "20220511_113325":"TGO temperatures missing",

    "20220608_013402":"TGO temperatures missing",
    "20220608_072716":"TGO temperatures missing",
    "20220608_191338":"TGO temperatures missing",

    "20220704_223130":"TGO temperatures missing",
    "20220704_231515":"TGO temperatures missing",
    
    "20221214_120546":"TGO temperatures missing",
    "20221214_123937":"TGO temperatures missing",

    "20230222_060344":"TGO temperatures missing",
    "20230222_062234":"TGO temperatures missing",
    "20230222_111414":"TGO temperatures missing",
    "20230222_115730":"TGO temperatures missing",
    "20230222_151005":"TGO temperatures missing",
    "20230222_155325":"TGO temperatures missing",
    "20230222_170804":"TGO temperatures missing",
    "20230222_181008":"TGO temperatures missing",
    "20230222_230148":"TGO temperatures missing",
    "20230223_011421":"TGO temperatures missing",
    
    "20230311_051245":"TGO temperatures missing",

    }
    
    if h5_prefix in known_errors.keys():
        reason = known_errors[h5_prefix]
        return reason
    
    return ""






def check_known_off_periods(h5_exectime):
    """check if observation time is within a known off-period"""

    #define known off-periods
    off_periods = [
        [datetime(2018, 6, 1, 13, 0, 0), datetime(2018, 6, 2, 1, 0, 0), "Malargue ground station failure"],
        [datetime(2019, 5, 18, 10, 14, 0), datetime(2019, 5, 25, 19, 0, 0), "TGO safe mode"],
        [datetime(2020, 3, 28, 17, 0, 0), datetime(2020, 4, 11, 12, 0, 0), "Covid-19 at MOC"],

    ] 

    dt = datetime.strptime(h5_exectime, "%Y-%m-%d %H:%M:%S")
    for off_period in off_periods:
        if off_period[0] < dt < off_period[1]:
            reason = off_period[2]
            return reason

    return ""



def h5_filename_to_datetime(h5):
    
    dt = datetime(int(h5[0:4]), int(h5[4:6]), int(h5[6:8]), int(h5[9:11]), int(h5[11:13]), int(h5[13:15]))
    return dt



def missing_file_reason(level, itl_obstype, h5_path):


    reason = ""
    
    h5 = os.path.basename(h5_path)
    h5_channel = re.match("\d*_\d*_[0-9]p[0-9][a-z]_([A-Z]*)(?:\.h5|_.*)", h5)[1]
    h5_dt = h5_filename_to_datetime(h5)
    
    if level == "0p2a":
        h5_obs_type = re.match("\d*_\d*_[0-9]p[0-9][a-z]_(?:[A-Z]*).*_([A-Z]{1,2})(?:_\d*)?\.h5", h5)[1]
    
    
        if h5_channel == "UVIS":
        
            # check if 0.2a UVIS file is a calibration < MTP001
            if h5_obs_type == "C" and h5_dt < datetime(2018, 4, 21, 12, 0, 0):
                #includes dayside nadirs, etc.
                reason = "UVIS nadir test observation before MTP001"
                return reason

            elif h5_obs_type == "C" and "Calibration" in itl_obstype:
                reason = "UVIS calibration observation"
                return reason

            elif h5_obs_type == "P" :
                reason = "No radiometric calibration for LNO Phobos observation"
                return reason
    
            elif h5_obs_type == "Q" :
                reason = "No radiometric calibration for LNO Deimos observation"
                return reason



        elif h5_channel == "LNO":
            if h5_obs_type == "N" :
                reason = "No radiometric calibration for LNO nightside nadir"
                return reason

            # elif h5_obs_type == "F" :
            #     reason = "No radiometric calibration for LNO nadir fullscans"
            #     return reason
    
            elif h5_obs_type == "L" :
                reason = "No radiometric calibration for LNO dayside limb"
                return reason
    
            elif h5_obs_type == "O" :
                reason = "No radiometric calibration for LNO nightside limb"
                return reason
    
            elif h5_obs_type == "P" :
                reason = "No radiometric calibration for LNO Phobos observation"
                return reason
    
            elif h5_obs_type == "Q" :
                reason = "No radiometric calibration for LNO Deimos observation"
                return reason
    

    if level == "0p1a":
        # open file, check if vertically binned (if so, not generated at 0.2a level)
        if h5_channel == "UVIS":
            with h5py.File(h5_path, "r") as h5f:
                if h5f["Channel/AcquisitionMode"][0] == 1:
                    reason = "UVIS vertically binned"
                    return reason

    elif level == "0p2a":
        # open file, check if dark calibration (so-dark and dark-nadir=0)
        if h5_channel == "UVIS":
            with h5py.File(h5_path, "r") as h5f:
                if h5f["Channel/DarkToObservationSteps"][0] == 0 and h5f["Channel/ObservationToDarkSteps"][0] == 0:
                    reason = "UVIS dark calibration (during normal observation)"
                    return reason

                # check if final dark frame is present
                if h5f["Channel/ReverseFlagAndDataTypeFlagRegister"][-1] != 0:
                    reason = "UVIS last dark frame missing from file"
                    return reason
            

    return reason




            


missing_file_outputs = []
reprocess_inserted = []

#open 0.1a file, check contents
for file_ix in progress(range(len(h5_prefixes))):
# for file_ix in range(len(h5_prefixes)):
    
    

    h5_prefix = h5_prefixes[file_ix]
    h5_obstype = h5_obstypes[file_ix]
    h5_exectime = h5_exectimes[file_ix]
    h5_channel = h5_channels[file_ix]

    if datetime.strptime(h5_exectime, "%Y-%m-%d %H:%M:%S") > last_obs_dt:
        continue


    year = h5_prefix[0:4]
    month = h5_prefix[4:6]
    day = h5_prefix[6:8]

    #make path to file, check if exists    
    level = "hdf5_level_0p1a"
    dir_path = os.path.join(paths["DATASTORE_ROOT_DIRECTORY"], "hdf5", level, year, month, day)
    matching_files_01a = glob.glob(dir_path+os.sep+h5_prefix+f"*{h5_channel}*.h5")
    
  
    reason = ""
    
    if len(matching_files_01a) == 1: #if file exists at 0.1a level (1 file per channel, no splitting by diffraction order)

        # obs_channel_01a = obs_channels_01a[h5_channel]
                
        # check if 0.2a file exists for that channel
        level = "hdf5_level_0p2a"
        dir_path = os.path.join(paths["DATASTORE_ROOT_DIRECTORY"], "hdf5", level, year, month, day)
        matching_files_02a = glob.glob(dir_path+os.sep+h5_prefix+f"*{h5_channel}*.h5")
        
        if len(matching_files_02a) > 0: #if file exists at 0.2a level (can split by order, could be multiple files)
            h5_highest_level = "0p2a"
            #find reason why it is present in 0.2a but missing in higher levels
            reason = missing_file_reason("0p2a", h5_obstype, matching_files_02a[0])
            # print(h5_prefix, h5_channel, reason)
            
            #if reason is not known, check known errors
            if reason == "":
                reason = check_known_errors(h5_prefix)
        
        else: #if only at 0.1a level
            h5_highest_level = "0p1a"
            #find reason why it is present in 0.1a but missing in 0.2a
            reason = missing_file_reason("0p1a", h5_obstype, matching_files_01a[0])
            # print(h5_prefix, h5_channel, reason)
            
            

    else: #if at neither 0.1a or 0.2a

        #if reason is not known, check known off periods
        reason = check_known_off_periods(h5_exectime)
        h5_highest_level = "None"

    
    
    
    if reason == "":
        
        #if reason is still unknown, make reprocessing scripts to try again
        print("%i: %s %s %s %s (%s)" %(file_ix, h5_prefix, h5_channel, h5_highest_level, reason, h5_exectime))
        
        if h5_channel == "SO":
            if h5_highest_level == "0p1a":
                make_reprocess_command("hdf5_l01a", "hdf5_l10a", h5_prefix=h5_prefix, h5_exectime=None, filter_=".*_SO", filepath="reprocess.sh")
            
            if h5_highest_level == "0p2a":
                make_reprocess_command("hdf5_l02a", "hdf5_l10a", h5_prefix=h5_prefix, h5_exectime=None, filter_=".*_SO", filepath="reprocess.sh")
            
        if h5_channel == "LNO":
            if h5_highest_level == "0p1a":
                make_reprocess_command("hdf5_l01a", "hdf5_l10a", h5_prefix=h5_prefix, h5_exectime=None, filter_=".*_LNO", filepath="reprocess.sh")
            
            if h5_highest_level == "0p2a":
                make_reprocess_command("hdf5_l02a", "hdf5_l10a", h5_prefix=h5_prefix, h5_exectime=None, filter_=".*_LNO", filepath="reprocess.sh")

        if h5_channel == "UVIS":
            if h5_highest_level == "0p1a":
                make_reprocess_command("hdf5_l01a", "hdf5_l10a", h5_prefix=h5_prefix, h5_exectime=None, filter_=".*_UVIS", filepath="reprocess.sh")
            
            if h5_highest_level == "0p2a":
                make_reprocess_command("hdf5_l02a", "hdf5_l10a", h5_prefix=h5_prefix, h5_exectime=None, filter_=".*_UVIS", filepath="reprocess.sh")

        #EXMs have no channel in the filename
        if h5_highest_level == "None":
            #avoid reprocessing twice if written to the sh script
            if h5_exectime not in reprocess_inserted:
                make_reprocess_command("inserted", "hdf5_l10a", h5_prefix=None, h5_exectime=h5_exectime, filepath="reprocess_inserted.sh")
                reprocess_inserted.append(h5_exectime)

        
        reason = "Unknown"
         
    if h5_highest_level == "0p2a":
        h5 = os.path.basename(matching_files_02a[0])
    if h5_highest_level == "0p1a":
        h5 = os.path.basename(matching_files_01a[0])
    if h5_highest_level == "None":
        h5 = "None"
    
    missing_file_outputs.append("%s,%s,%s,%s,%s,%s,%s" %(h5_exectime, h5_obstype, h5_channel, h5_prefix, h5_highest_level, h5, reason))

with open("db/missing_file_log.txt", "w") as f:
    for missing_file_output in missing_file_outputs:
        f.write("%s\n" %missing_file_output)
        