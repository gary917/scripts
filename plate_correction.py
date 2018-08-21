##script to determine how many plates are the same between ENTER and EXIT
#compare two list
import pandas as pd
import datetime
import Levenshtein

FILE_PATH = "/Users/garychen/Desktop/ELEC4120/ssh_folder/csv/08/"
FILE_PATH_CLEAN = "/Users/garychen/Desktop/ELEC4120/cleaned_csv/"

FILE_NAME_ENTER = "BARKER_ENTER_2018-08-16"
FILE_NAME_EXIT = "BARKER_EXIT_2018-08-16"

FILE_NAME_ENTER_CLEAN = "BARKER_ENTER_2018-08-16_CLEANED"
FILE_NAME_EXIT_CLEAN = "BARKER_EXIT_2018-08-16_CLEANED"


CSV_EXTENSION = ".CSV"


header_field = ["EVENT_DESC","DATE","TIME","PLATE","PLATE_HASH","PLATE_NOT_READ","PLATE_STRING","PLATE_COUNTRY",
                 "PLATE_PROVINCE","PLATE_COUNTRY_CODE","PLATE_REGION","OCRSCORE","OCRSCORE_CHAR","CHAR_HEIGHT",
                 "CHAR_WIDTH","NREAD","SHUTTER","GAIN","STROBO","AI_LEVEL","SPEED","CLASS","CLASS_STRING","VEHICLE_TYPE",
                 "DIRECTION","POS","DEVICE_SN","PLATE_COLOR_STRING","ACTUAL_LICENSE","DIAG_STATUS","DIAG_MASK","DIAG_STRING",
                 "ACQUISITION_MODE","PLATE_MIN_X","PLATE_MIN_Y","PLATE_MAX_X","PLATE_MAX_Y","ORIG_PLATE_MIN_X","ORIG_PLATE_MIN_Y",
                 "ORIG_PLATE_MAX_X","ORIG_PLATE_MAX_Y","TRANSIT_ID","TRIGGER_COUNT","PLATE_DESC_A","PLATE_DESC_B","VEHICLE_TYPE_NUM",
                 "QUALIF_0","QUALIF_1","QUALIF_0_DESC","QUALIF_1_DESC","OCCUPANCY_TIME","GAP_TIME","GAIN_RED","GAIN_BLUE","PLATE_STD","PLATE_TRL","PLATE_ADR","GRAB_MODE"]


def compare_plates(enter,exit):
	common = []
	
	i = 0
	j = 0
	for i in range(len(enter)):
		j = 0
		while j < len(exit):
			if Levenshtein.ratio(enter[i],exit[j]) > 0.65 :
				exit.pop(j)
				common.append(enter[i])
				j = j + 1
				break
			j = j + 1
	return common


def main():
	df_enter = pd.read_csv(FILE_PATH_CLEAN + FILE_NAME_ENTER_CLEAN + CSV_EXTENSION, delimiter = ';', header = None)
	df_exit = pd.read_csv(FILE_PATH_CLEAN + FILE_NAME_EXIT_CLEAN + CSV_EXTENSION, delimiter = ';',header = None)
	df_enter = df_enter.iloc[0]
	df_exit = df_exit.iloc[0]
	df_enter.columns = header_field
	df_exit.columns = header_field
	enter_length = df_enter.shape[0]
	exit_length = df_exit.shape[0]

	enter_plates = df_enter["PLATE_STRING"].tolist()
	exit_plates = df_exit["PLATE_STRING"].tolist()
	
	common_plates = compare_plates(enter_plates,exit_plates)	

	###############################
	print("Number of unique plates in enter :", enter_length)
	print("Number of unique plates in exit :", exit_length)
	print("*******************************")
	print("Number of matching plates :", len(common_plates))
	print("Percentage matched : ",(len(common_plates)/len(enter_plates))*100,"%")


if __name__ == '__main__':
	main()

