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


data_folders = ["april_2023", "september_2023", "october_2023"]
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

nm = "Arabkir"

print(districts[nm][0].rel_prices)
# for districts in district_history:
plt.style.use('_mpl-gallery')
# plot
fig, ax = plt.subplots()
VP = ax.boxplot(districts[nm][0].rel_prices)

# ax.set(xlim=(0, 8), xticks=np.arange(1, 8), ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()


# print(district_history["Malatia_Sebastia"])
