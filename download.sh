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
			while [ $j -ne 40 ]
			do
				fullpath=`echo $url | sed 's/\?/\/'$j'\?/g'`
				echo $i$j
				# $url + $j
				curl $fullpath > $i$j.html
				if [ ! -s "$i$j.html" ]; then
					rm $i$j.html
					break
				fi

				j=$(($j+1))
			done
			cd ../..
		else
			# url
			url="$i"
		fi
	done
done
