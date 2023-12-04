import os
import csv
import numpy as np
import matplotlib.pyplot as plt

class DistrictPricesByRoom:
	def __init__(self, room_count):
		# arrays of prices for 1, 2, >3 room apartament
		self.abs_prices = []
		# arrays of mean prices for 1, 2, >3 room apartament
		self.rel_prices = []
		self.room_count = room_count

	def add(self, price, meters):
		self.abs_prices[-1].append(price)
		self.rel_prices[-1].append(float(price)/meters)

	def next_group(self):
		self.abs_prices.append([])
		self.rel_prices.append([])

def save_plot(districts, data_folders, is_abs = True):
	for dname, ddata in districts.items():
		for rooms in ddata:
			plt.style.use('_mpl-gallery')
			file_name = str(rooms.room_count) + "/"

			if is_abs is True:
				file_name += "abs/" + dname + ".svg"
			else:
				file_name += "rel/" + dname + ".svg"

			fig, ax = plt.subplots(figsize=(10, 10), facecolor='lightskyblue', layout='constrained')
			fig.suptitle('Rent cost by months in {0}'.format(dname))

			if is_abs is True:
				VP = ax.boxplot(rooms.abs_prices, labels=data_folders)
			else:
				VP = ax.boxplot(rooms.rel_prices, labels=data_folders)

			# if not os.path.exists(str(rooms.room_count)):
			# 	os.makedirs(str(rooms.room_count))

			if not os.path.exists(str(rooms.room_count) + "/abs"):
				os.makedirs(str(rooms.room_count) + "/abs")

			if not os.path.exists(str(rooms.room_count) + "/rel"):
				os.makedirs(str(rooms.room_count) + "/rel")

			plt.savefig(file_name)
			plt.close()


data_folders = ["april_2023", "september_2023", "october_2023", "november_2023", "december_2023"]
# dict: District --> array of DistrictPricesAtMoment
# district_history = {}

# container for districts
districts = {}

for directory in data_folders:
	for fname in os.listdir(directory):
		csv_filename = os.path.join(directory, fname)
		district_name = os.path.splitext(fname)[0]

		# add district if not exists
		if district_name not in districts.keys():
			districts[district_name] = [DistrictPricesByRoom(1), DistrictPricesByRoom(2), DistrictPricesByRoom(3)]

		cur_district = districts[district_name]

		for item in cur_district:
			item.next_group()

		with open(csv_filename) as f:
			reader = csv.reader(f, delimiter='\t')
			lst = list(reader)

			for row in lst:
				room_cnt = int(row[1])
				if room_cnt > 3:
					room_cnt = 3

				cur_district[room_cnt-1].add(int(row[2]), int(row[3]))


save_plot(districts, data_folders, True)
save_plot(districts, data_folders, False)
