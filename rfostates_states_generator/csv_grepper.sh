if [ ! -f "$2" ];then
	echo File dose not exist!
	exit 1
fi
fline=$(head -1 "$2")
echo First line is: $fline
nFile="$1_grepped.csv"
grep $1 $2 > $nFile
sed -i "1i $fline" $nFile

