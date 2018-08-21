#filters out data based on range of time

import pandas as pd
import datetime

FILE_PATH = "/Users/garychen/Desktop/ELEC4120/ssh_folder/csv/08/"
FILE_NAME = "BARKER_ENTER_2018-08-16"
CSV_EXTENSION = ".CSV"

OUTPUT_PATH = "/Users/garychen/Desktop/ELEC4120/time_filter/"
OUTPUT_NAME = FILE_NAME + "_FILTERED" + CSV_EXTENSION

LOW_TIME_RANGE = datetime.time(hour = 11,minute = 31)
HIGH_TIME_RANGE = datetime.time(hour = 13,minute = 43)

header_field = ["EVENT_DESC","DATE","TIME","PLATE","PLATE_HASH","PLATE_NOT_READ","PLATE_STRING","PLATE_COUNTRY",
                 "PLATE_PROVINCE","PLATE_COUNTRY_CODE","PLATE_REGION","OCRSCORE","OCRSCORE_CHAR","CHAR_HEIGHT",
                 "CHAR_WIDTH","NREAD","SHUTTER","GAIN","STROBO","AI_LEVEL","SPEED","CLASS","CLASS_STRING","VEHICLE_TYPE",
                 "DIRECTION","POS","DEVICE_SN","PLATE_COLOR_STRING","ACTUAL_LICENSE","DIAG_STATUS","DIAG_MASK","DIAG_STRING",
                 "ACQUISITION_MODE","PLATE_MIN_X","PLATE_MIN_Y","PLATE_MAX_X","PLATE_MAX_Y","ORIG_PLATE_MIN_X","ORIG_PLATE_MIN_Y",
                 "ORIG_PLATE_MAX_X","ORIG_PLATE_MAX_Y","TRANSIT_ID","TRIGGER_COUNT","PLATE_DESC_A","PLATE_DESC_B","VEHICLE_TYPE_NUM",
                 "QUALIF_0","QUALIF_1","QUALIF_0_DESC","QUALIF_1_DESC","OCCUPANCY_TIME","GAP_TIME","GAIN_RED","GAIN_BLUE","PLATE_STD","PLATE_TRL","PLATE_ADR","GRAB_MODE"]

df = pd.read_csv(FILE_PATH + FILE_NAME + CSV_EXTENSION, delimiter = ';')
df.columns = header_field
before_length = df.shape[0]



#filter based on time range 
df['TIME'] = pd.to_datetime(df['TIME'],format ='%H-%M-%S-%f').dt.time
df = df.loc[df['TIME'] > LOW_TIME_RANGE]
df = df.loc[df['TIME'] < HIGH_TIME_RANGE]
after_length = df.shape[0]

print("The length before is: ",before_length)
print("The length after is: ",after_length)

df.to_csv(path_or_buf = OUTPUT_PATH + OUTPUT_NAME)
print("**** FILTERED BASED ON TIME ****")
