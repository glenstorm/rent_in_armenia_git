from lxml import html
# Import the os module, for the os.walk function
import os

ext = ('.html')
# Set the directory you want to start from
rootDir = '.'
for dirName, subdirList, fileList in os.walk(rootDir):
	# print('Found directory: %s' % dirName)
	for fname in fileList:
		if fname.endswith(ext):
			if not os.path.exists("csv"):
				os.mkdir("csv")
			out_csv_name = "csv/" + dirName[2:-4] + ".csv"
			out_file = open(out_csv_name, mode="a")
			# print(out_csv_name)
			text_file = open(dirName + "/" + fname, mode="r")
			data = text_file.read()
			text_file.close()

			tree = html.fromstring(data)
			aparts = tree.xpath('//*[@id="contentr"]/div[@class="dl"]/a[*]')

			for z in aparts:
				price = None
				where = None
				link = z.values()[0]
				for divs in z:
					if divs.tag == 'div':
						for inner_div in divs:
							# print(f"inner_div.attrib = {inner_div.attrib}")
							if inner_div.attrib == {'class': 'ad-info-line-wrapper'}:
								for pdivs in inner_div:
									if pdivs.attrib == {'class':'p'}:
										price = pdivs.text
							if inner_div.attrib == {'class': 'at'}:
								where = inner_div.text

				if price is not None and where is not None:
					# price part
					intprice = 0
					price = price.replace(',', '')
					index = price.find(' ')
					if index != -1:
						price = price[:index]

					if price[0] == '$':
						price = price[1:]
						intprice = int(price) * 404
					elif price[0] == '€':
						price = price[1:]
						intprice = int(price) * 445
					else:
						intprice = int(price)

					# square part
					index_where = where.find(" кв.м.")
					leftborderwhere = -1
					if index_where != -1:
						leftborderwhere = where.rfind(', ', 0, index_where)

					index_rooms = where.find(" ком.")
					leftborderrooms = -1
					if index_rooms != -1:
						leftborderrooms  = where.rfind(', ', 0, index_rooms)
					# print(str(leftborderwhere))
					if leftborderwhere != -1 and leftborderrooms != -1:
						newwhere = where[leftborderwhere+2:index_where]
						newrooms = where[leftborderrooms+2:index_rooms]
						out_file.write(where + "\t" + str(newrooms) + "\t" + str(intprice) + "\t" + str(newwhere) + "\t" + "https://www.list.am" + link + "\n")


			out_file.close()
			# exit()

# import shutil
# foldrs2delete = ["Achapnyack", "Avan", "Nork_Marash", "Nubarashen", "Zeitun_Kanaker", "Kentron", "Nor_Nork", "Arabkir", "Davidashen", "Erebuni", "Malatia_Sebastia", "Shengavit"]
# for fldr in foldrs2delete:
# 	shutil.rmtree(fldr)
