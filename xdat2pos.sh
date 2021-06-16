#!/bin/bash
#########################################################################
# File Name: xdat2pos.sh
# Author: wdhu@219.220.210.138
# Created Time: Tue 29 Mar 2016 04:07:58 PM CST
#########################################################################
if [[ -f ./POSCAR ]];then
	poscarfile=./POSCAR
else
	echo "no POSCAR exist. please specify the POSCAR"
	read poscarfile
	if [[ ! -f $poscarfile ]];then
		exit
	fi
fi
totnumions=`awk '{if(NR == 7) {sum = 0; for(i=1;i<=NF;i++) sum +=$i }}END{ print(sum)}' $poscarfile`
head  -9 $poscarfile > temp_lat
end=$((totnumions+9))
sed -n '10,'$end''p $poscarfile | awk '{print $4,$5,$6}' > temp_TF
egrep -A$totnumions "Direct configuration= *$1$" XDATCAR|tail -$totnumions > temp_xyz
cat temp_lat > POSCAR_$1
paste temp_xyz  temp_TF |awk '{printf"%18.12f%18.12f%18.12f    %s   %s   %s\n",$1,$2,$3,$4,$5,$6}' >> POSCAR_$1
rm temp_xyz  temp_TF temp_lat
