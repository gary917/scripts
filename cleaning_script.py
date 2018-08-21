#actual cleaning, remove duplicates

import pandas as pd
import datetime
import Levenshtein

FILE_PATH = "/Users/garychen/Desktop/ELEC4120/ssh_folder/csv/08/"
TIME_FILTER = True

FILE_NAME_ENTER = "BARKER_ENTER_2018-08-16"
FILE_NAME_EXIT = "BARKER_EXIT_2018-08-16"

CSV_EXTENSION = ".CSV"

OUTPUT_PATH = "/Users/garychen/Desktop/ELEC4120/cleaned_csv/"

OUTPUT_NAME_ENTER = FILE_NAME_ENTER + "_CLEANED" + CSV_EXTENSION
OUTPUT_NAME_EXIT = FILE_NAME_EXIT + "_CLEANED" + CSV_EXTENSION

NUM_ROW_COMPARE = 5 #number of rows to compare to find duplicates

LOW_TIME_RANGE = datetime.time(hour = 11,minute = 31)
HIGH_TIME_RANGE = datetime.time(hour = 13,minute = 44)

DUPLICATE_1_ENTER = 0  #DUPLICATEs, exact string
DUPLICATE_2_ENTER = 0	 #duplicates, different string
DUPLICATE_1_EXIT = 0  #DUPLICATEs, exact string
DUPLICATE_2_EXIT = 0	 #duplicates, different string

header_field = ["EVENT_DESC","DATE","TIME","PLATE","PLATE_HASH","PLATE_NOT_READ","PLATE_STRING","PLATE_COUNTRY",
                 "PLATE_PROVINCE","PLATE_COUNTRY_CODE","PLATE_REGION","OCRSCORE","OCRSCORE_CHAR","CHAR_HEIGHT",
                 "CHAR_WIDTH","NREAD","SHUTTER","GAIN","STROBO","AI_LEVEL","SPEED","CLASS","CLASS_STRING","VEHICLE_TYPE",
                 "DIRECTION","POS","DEVICE_SN","PLATE_COLOR_STRING","ACTUAL_LICENSE","DIAG_STATUS","DIAG_MASK","DIAG_STRING",
                 "ACQUISITION_MODE","PLATE_MIN_X","PLATE_MIN_Y","PLATE_MAX_X","PLATE_MAX_Y","ORIG_PLATE_MIN_X","ORIG_PLATE_MIN_Y",
                 "ORIG_PLATE_MAX_X","ORIG_PLATE_MAX_Y","TRANSIT_ID","TRIGGER_COUNT","PLATE_DESC_A","PLATE_DESC_B","VEHICLE_TYPE_NUM",
                 "QUALIF_0","QUALIF_1","QUALIF_0_DESC","QUALIF_1_DESC","OCCUPANCY_TIME","GAP_TIME","GAIN_RED","GAIN_BLUE","PLATE_STD","PLATE_TRL","PLATE_ADR","GRAB_MODE"]


def remove_duplicate(df): #removes duplicate
	dup_1 = 0  #DUPLICATEs, exact string
	dup_2 = 0	 #duplicates, different string
	i = 0
	while True: #traverse through the rows
		i = i + 1
		if i > df.shape[0] - 1:
			return (df,dup_1,dup_2)
		license_1 = df['PLATE_STRING'][i]
		for j in range(i + 1,i + NUM_ROW_COMPARE): #compare with next 5 rows
			if j > df.shape[0] - 1:
				return (df,dup_1,dup_2)
			license_2 = df['PLATE_STRING'][j]
			if Levenshtein.distance(license_1,license_2) < 3: #drop the duplicate plate

				if Levenshtein.ratio(license_1,license_2) == 1: #calcuate number of occurance of errors
					dup_1 = dup_1 + 1
				else:
					dup_2 = dup_2 + 1

				if df['OCRSCORE'][i] > df['OCRSCORE'][j] : #compare OCR score, the lower one will be deleted
					df = df.drop(j)
					df = df.reset_index(drop=True)	
					i = i - 1
				else:
					df = df.drop(i)
					df = df.reset_index(drop=True)
					i = i - 1
	return (df,dup_1,dup_2)


def compare_plates(enter,exit):
	common = []
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



def time_range_filter(df): #filter rows based on time range
	df['TIME'] = pd.to_datetime(df['TIME'],format ='%H-%M-%S-%f').dt.time
	df = df.loc[df['TIME'] > LOW_TIME_RANGE]
	df = df.loc[df['TIME'] < HIGH_TIME_RANGE]
	df = df.reset_index(drop=True)	

	return df



def main():
	df_enter = pd.read_csv(FILE_PATH + FILE_NAME_ENTER + CSV_EXTENSION, delimiter = ';')
	df_exit = pd.read_csv(FILE_PATH + FILE_NAME_EXIT + CSV_EXTENSION, delimiter = ';')
	df_enter.columns = header_field
	df_exit.columns = header_field

	if TIME_FILTER:
		print("filtering from", LOW_TIME_RANGE, 'to', HIGH_TIME_RANGE)
		df_enter = time_range_filter(df_enter)
		df_exit = time_range_filter(df_exit)

	before_length_enter = df_enter.shape[0] #number of rows before cleaning
	before_length_exit = df_exit.shape[0] #number of rows before cleaning

	print("**** CLEANING",FILE_NAME_ENTER, 'AND' , FILE_NAME_EXIT, "****")

	#Find number of rows with NOTREAD
	other_error_enter = df_enter.loc[df_enter['EVENT_DESC'] == 'Ocr Not Read']
	other_error_exit = df_exit.loc[df_exit['EVENT_DESC'] == 'Ocr Not Read']

	#Remove Duplicates from CSV
	df_enter,DUPLICATE_1_ENTER,DUPLICATE_2_ENTER = remove_duplicate(df_enter)
	df_exit,DUPLICATE_1_EXIT,DUPLICATE_2_EXIT = remove_duplicate(df_exit)

	#Keep only the OCR read
	df_enter = df_enter[df_enter.EVENT_DESC == 'Ocr Read'] #keep only OCR read
	df_exit = df_exit[df_exit.EVENT_DESC == 'Ocr Read'] #keep only OCR read

	#Comparing plates between enter and exit
	enter_plates = df_enter["PLATE_STRING"].tolist()
	exit_plates = df_exit["PLATE_STRING"].tolist()
	common_plates = compare_plates(enter_plates, exit_plates)

	#filter low OCR scores
	df_enter = df_enter.loc[df_enter['OCRSCORE'] > 60] #OCR score too low, take them out
	df_exit = df_exit.loc[df_exit['OCRSCORE'] > 60] #OCR score too low, take them out



	#########################################################
	######################## RESULTS ########################
	#########################################################

	after_length_enter = df_enter.shape[0]
	after_length_exit = df_exit.shape[0]


	print("********** ENTER ************")
	print("Number of entries before: ",before_length_enter)
	print("Number of entries after: ",after_length_enter)

	print("--------- ERRORS -----------")
	print("Duplicates (exact):", DUPLICATE_1_ENTER)
	print("Duplicates (different):", DUPLICATE_2_ENTER)
	print("Other :", other_error_enter.shape[0])

	print("\n\n")
	print("********** EXIT ************")
	print("Number of entries before: ",before_length_exit)
	print("Number of entries after: ",after_length_exit)

	print("--------- ERRORS -----------")
	print("Duplicates (exact):", DUPLICATE_1_EXIT)
	print("Duplicates (different):", DUPLICATE_2_EXIT)
	print("Other :", other_error_exit.shape[0])

	print("\n\n")

	print("********** Matching ************")
	print("Number of matching plates:", len(common_plates))
	print("\n\n")

	df_enter.to_csv(path_or_buf = OUTPUT_PATH + OUTPUT_NAME_ENTER)
	df_exit.to_csv(path_or_buf = OUTPUT_PATH + OUTPUT_NAME_EXIT)

if __name__ == '__main__':
	main()

