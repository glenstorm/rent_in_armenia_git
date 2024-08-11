cat input.txt | while read line
do
	n=0
	url=''
	IFS=' ' #setting space as delimiter
	read -ra ADDR <<<"$line" #reading str as an array as tokens separated by IFS
	for i in "${ADDR[@]}"; #accessing each element of array
	do
		((n=n+1))
		if [ `expr $n % 2` == 0 ]
		then
			# district
			# echo "$url" - "$i"
			mkdir -p $i/web
			cd $i/web

			j=1
			while [ $j -ne 20 ]
			do
				fullpath=`echo $url | sed 's/\?/\/'$j'\?/g'`
				echo $i$j
				# $url + $j
				curl $fullpath -compressed -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0' -H 'Cookie: !!!Copy from browser!!!' > $i$j.html
				sleep 1
				if [ ! -s "$i$j.html" ]; then
					rm $i$j.html
					break
				fi

				j=$(($j+1))
			done
			cd ../..
			sleep 10
		else
			# url
			url="$i"
		fi
	done
done

python3 parse.py
cp -f csv/* august_2024/ # rename each time
rm -rf csv
python3 build_candles.py
