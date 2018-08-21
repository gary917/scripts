library(anytime)

rm(list=ls())


#Given timeframe and date, calculate number of rows of data in a CSV file
#add file headers as well 



FILE_PATH_CSV <- "/Users/garychen/Desktop/ELEC4120/ssh_folder/csv/08/BARKER_ENTER_2018-08-10.CSV"

#ACTUAL_PLATE replaced field PLATE_COLOR, camera gives no info about that field
file_header <- c("EVENT_DESC","DATE","TIME","PLATE","PLATE_HASH","PLATE_NOT_READ","PLATE_STRING","PLATE_COUNTRY",
                 "PLATE_PROVINCE","PLATE_COUNTRY_CODE","PLATE_REGION","OCRSCORE","OCRSCORE_CHAR","CHAR_HEIGHT",
                 "CHAR_WIDTH","NREAD","SHUTTER","GAIN","STROBO","AI_LEVEL","SPEED","CLASS","CLASS_STRING","VEHICLE_TYPE",
                 "DIRECTION","POS","DEVICE_SN","PLATE_COLOR_STRING","ACTUAL_LICENSE","DIAG_STATUS","DIAG_MASK","DIAG_STRING",
                 "ACQUISITION_MODE","PLATE_MIN_X","PLATE_MIN_Y","PLATE_MAX_X","PLATE_MAX_Y","ORIG_PLATE_MIN_X","ORIG_PLATE_MIN_Y",
                 "ORIG_PLATE_MAX_X","ORIG_PLATE_MAX_Y","TRANSIT_ID","TRIGGER_COUNT","PLATE_DESC_A","PLATE_DESC_B","VEHICLE_TYPE_NUM",
                 "QUALIF_0","QUALIF_1","QUALIF_0_DESC","QUALIF_1_DESC","OCCUPANCY_TIME","GAP_TIME","GAIN_RED","GAIN_BLUE","PLATE_STD","PLATE_TRL","PLATE_ADR","GRAB_MODE")




df <- read.csv(FILE_PATH_CSV, header = F, sep=";")

colnames(df) <- file_header #adds the header name to the df

#apply filter to calculate how many cars left
relevant_col <- df[strptime(df$TIME,"%H-%M-%S") > "2018-08-13 16:56:12 AEST",]
relevant_col <- relevant_col[strptime(relevant_col$TIME,"%H-%M-%S") < "2018-08-13 17:30:59 AEST", ]

print(nrow(relevant_col))

#enter 2018-08-10, first 50 image
