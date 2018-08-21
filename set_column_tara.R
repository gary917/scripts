rm(list=ls())

# Load libraries
library(tidyverse)
library(chron)
library(plotly)
library(dplyr)

# Load Data ---------------------------------------------

## File path (month 7 year 2018 only)
FILE_PATH <- "/Users/garychen/Desktop/ELEC4120/ssh_folder/csv/08” 
TEST_FILE_PATH <- “/Users/tarasutjarittham/Google-Drive/PhD/smartcampus/projects/smart-carpark/data/2018/05/”

## All field names
file_header <- c(“EVENT_DESC”, “DATE”, “TIME”, “PLATE”, “PLATE_HASH”, “PLATE_NOT_READ”,“PLATE_STRING”,
“PLATE_COUNTRY”, “PLATE_PROVINCE”, “PLATE_COUNTRY_CODE”,“PLATE_REGION”,“OCRSCORE”,“OCRSCORE_CHAR”,“CHAR_HEIGHT”,
“CHAR_WIDTH”,“NREAD”, “SHUTTER”, “GAIN”,“STROBO”, “AI_LEVEL”, “SPEED”,“CLASS”, “CLASS_STRING”, “VEHICLE_TYPE”,“DIRECTION”, 
“POS”, “DEVICE_SN”,“PLATE_COLOR_STRING”,“PLATE_COLOR”, “DIAG_STATUS”,“DIAG_MASK”,“ACQUISITION_MODE”,“PLATE_MIN_X”,
“PLATE_MIN_Y”,“PLATE_MAX_X”,“PLATE_MAX_Y”,“ORIG_PLATE_MIN_X”,“ORIG_PLATE_MIN_Y”,“ORIG_PLATE_MAX_X”,“ORIG_PLATE_MAX_Y”,
“TRANSIT_ID”,“TRIGGER_COUNT”,“PLATE_DESC_A”,“PLATE_DESC_B”,“VEHICLE_TYPE_NUM”,“QUALIF_0”,“QUALIF_1”,“QUALIF_0_DESC”,
“QUALIF_1_DESC”,“OCCUPANCY_TIME”,“GAP_TIME”,“GAIN_RED”,“GAIN_BLUE”,“PLATE_STD”,“PLATE_TRL”,“PLATE_ADR”,“GRAB_MODE")

## Function to read csv file
readMyCsv <- function(file_name){
  print(paste(“Saving csv files: “, file_name))
  df <- read.csv(file_name, sep=“;”, header = F)
  
  df$camera <- ifelse(grepl(“ENTER”,file_name), “ENTER”, “EXIT”)
  return(df)
}

## Save all csv files into one single df
temp = list.files(path = FILE_PATH, pattern=“*.CSV”)
myfiles = lapply(paste0(FILE_PATH,temp), readMyCsv)
carpark_df <- do.call(rbind, myfiles)

carpark_df <- carpark_df %>%
  select(-V33) %>%
  set_names(c(file_header, “camera”))

## Occupancy
temp = list.files(path = TEST_FILE_PATH, pattern=“*2018-05-22.CSV”)
myfiles = lapply(paste0(TEST_FILE_PATH,temp), readMyCsv)
carpark_test_df <- do.call(rbind, myfiles)

carpark_test_df <- carpark_test_df %>%
  select(-V33) %>%
  set_names(c(file_header, “camera”))