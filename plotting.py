import pandas as pd
import datetime
import Levenshtein

from datetime import timedelta

FILE_PATH = "/Users/garychen/Desktop/ELEC4120/ssh_folder/csv/08/"
FILE_NAME_ENTER = "BARKER_ENTER_"
FILE_NAME_EXIT = "BARKER_EXIT_"
DATE = "2018-08-15"

CSV_EXTENSION = ".CSV"

OUTPUT_PATH = "/Users/garychen/Desktop/ELEC4120/cleaned_csv/"
OUTPUT_NAME = "BARKER_COMMON_" + DATE + CSV_EXTENSION

NUM_ROW_COMPARE = 8 #number of rows to compare to find duplicates

header_field = ["EVENT_DESC","DATE","TIME","PLATE","PLATE_HASH","PLATE_NOT_READ","PLATE_STRING","PLATE_COUNTRY",
                 "PLATE_PROVINCE","PLATE_COUNTRY_CODE","PLATE_REGION","OCRSCORE","OCRSCORE_CHAR","CHAR_HEIGHT",
                 "CHAR_WIDTH","NREAD","SHUTTER","GAIN","STROBO","AI_LEVEL","SPEED","CLASS","CLASS_STRING","VEHICLE_TYPE",
                 "DIRECTION","POS","DEVICE_SN","PLATE_COLOR_STRING","ACTUAL_LICENSE","DIAG_STATUS","DIAG_MASK","DIAG_STRING",
                 "ACQUISITION_MODE","PLATE_MIN_X","PLATE_MIN_Y","PLATE_MAX_X","PLATE_MAX_Y","ORIG_PLATE_MIN_X","ORIG_PLATE_MIN_Y",
                 "ORIG_PLATE_MAX_X","ORIG_PLATE_MAX_Y","TRANSIT_ID","TRIGGER_COUNT","PLATE_DESC_A","PLATE_DESC_B","VEHICLE_TYPE_NUM",
                 "QUALIF_0","QUALIF_1","QUALIF_0_DESC","QUALIF_1_DESC","OCCUPANCY_TIME","GAP_TIME","GAIN_RED","GAIN_BLUE","PLATE_STD","PLATE_TRL","PLATE_ADR","GRAB_MODE"]


def remove_duplicate(df): #removes duplicate
	i = 0
	while True: #traverse through the rows
		i = i + 1
		if i > df.shape[0] - 1:
			return df
		license_1 = df['PLATE_STRING'][i]
		for j in range(i + 1,i + NUM_ROW_COMPARE): #compare with next 5 rows
			if j > df.shape[0] - 1:
				return df
			license_2 = df['PLATE_STRING'][j]
			if Levenshtein.ratio(license_1,license_2) > 0.65: #drop the duplicate plate
				if df['OCRSCORE'][i] > df['OCRSCORE'][j] : #compare OCR score, the lower one will be deleted
					df = df.drop(j)
					df = df.reset_index(drop=True)	
					i = i - 1
				else:
					df = df.drop(i)
					df = df.reset_index(drop=True)
					i = i - 1
	return df

def compare_plates(enter_list, exit_list): #makes list of common license plate and their enter and exit time
	common = []
	enter_time = []
	exit_time = []
	j = 0
	for i in range(len(enter_list)):
		j = 0
		while j < len(exit_list):
			if Levenshtein.distance(enter_list['PLATE_STRING'][i],exit_list['PLATE_STRING'][j]) < 3 : #need to go thru entire list and find plate with highest ratio
				common.append(enter_list['PLATE_STRING'][i])
				enter_time.append(enter_list['TIME'][i])
				exit_time.append(exit_list['TIME'][j])
				exit_list = exit_list.drop(j)
				exit_list = exit_list.reset_index(drop=True) ##NEED TO PARSE IN DICT OF {ENTER_PLATE, ENTER TIME} {EXIT_PLATE, EXIT ITME}
				j = j + 1
				break
			j = j + 1
	return (common, enter_time, exit_time)


def prepare_df(df): #takes in a df, adds header_field, remove diplicates and extract its LICENSE_PLATE and TIME
	df.columns = header_field
	df = remove_duplicate(df)
	plates = df["PLATE_STRING"]
	time = pd.to_datetime(df["TIME"],format = '%H-%M-%S-%f')
	plates_time = pd.concat([plates, time],axis = 1)
	return plates_time



def main():
	df_enter = pd.read_csv(FILE_PATH + FILE_NAME_ENTER + DATE + CSV_EXTENSION, delimiter = ';')
	df_exit = pd.read_csv(FILE_PATH + FILE_NAME_EXIT + DATE + CSV_EXTENSION, delimiter = ';')

	print("**** CLEANING ****")
	enter = prepare_df(df_enter)
	exit = prepare_df(df_exit)

	print("**** MATCHING ****")
	common_plates, enter_time, exit_time = compare_plates(enter , exit)
	print("Plates matched:",len(common_plates))
	enter_time1 = pd.Series(enter_time)
	exit_time1 = pd.Series(exit_time)
	stay_duration = exit_time1.sub(enter_time1)

	d = {'LICENSE_PLATE': common_plates, 'ENTER_TIME': enter_time1, 'EXIT_TIME': exit_time1, 'STAY_DURATION': stay_duration }
	df_common = pd.DataFrame(data = d)
	df_common.to_csv(path_or_buf = OUTPUT_PATH + OUTPUT_NAME )

	print("Outputted")

	#stay_duration = [plate_exit[i] - plate_enter[i] for i in len(plate_exit)]




if __name__ == '__main__':
	main()