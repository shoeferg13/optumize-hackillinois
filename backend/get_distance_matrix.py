#Route optimization algorithm for nurses

import googlemaps
from datetime import datetime
import pandas as pd
import numpy as np

def get_distance_matrix(filename, employee_id):
	patient_df = pd.read_csv(filename)
	patient_df = patient_df[patient_df['employee_id'] == employee_id]
	patient_df['full_address'] = patient_df['street_address'] + ', ' + patient_df['city'] +  ', ' + patient_df['state']
	patient_df = patient_df.dropna(subset=['full_address'])
	print(patient_df)

	api_key = open("api_key.txt","r")
	# print(api_key)
	gmaps = googlemaps.Client(key=api_key)
	now = datetime.now()

	dist_matrix = gmaps.distance_matrix(origins=patient_df['full_address'], destinations=patient_df['full_address'], mode='driving', departure_time=now)
	matrix_rows = dist_matrix['rows']

	array = np.zeros((len(patient_df['full_address']), len(patient_df['full_address'])))

	count = 0

	for i in range(0, len(patient_df['full_address'])):
		for j in range(0, len(patient_df['full_address'])):
			time_as_str = dist_matrix['rows'][i]['elements'][j]['duration']['text']
			split = time_as_str.split(' ')
			array[i, j] = split[0]
			count += 1

	return array


# print(get_distance_matrix('CSV/PATIENT_TASK_DATA.csv', 1))