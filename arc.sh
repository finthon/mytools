#!/bin/bash
#########################################################################
# File Name: /data/home/wdhu/car.sh
# Author: wdhu@59.78.92.45
# Created Time: Mon 01 Dec 2014 04:43:08 PM CST
#########################################################################
outcar=OUTCAR
if [ x$1 == x ];then
	infile=OUT.ANI
else
	infile=$1
fi
if [ ! -f OUT.ANI  ];then
	/data/apps/vasp/vtstscripts/xdat2xyz.pl
	infile=movie.xyz
fi
if [ $infile == CONTCAR ];then
	pos2xyz.pl CONTCAR
	infile=CONTCAR.xyz
fi
	

outfile=`grep "PBS -N" vasp.script | awk '{print $3}' | head -1`.arc
#frames=`grep STEP $infile | cat -n | tail -1 | awk '{print $1}'`
#atomsnum=`sed -n 1p $infile`
#a=`$HOME/script/lattice.py | sed -n '2'p | awk '{printf"%.5f", $3} '`
#b=`$HOME/script/lattice.py | sed -n '3'p | awk '{printf"%.5f", $3} '`
#c=`$HOME/script/lattice.py | sed -n '4'p | awk '{printf"%.5f", $3} '`
#alpla=`$HOME/script/lattice.py | sed -n '5'p | awk '{printf"%.5f",  $3} '`
#beta=`$HOME/script/lattice.py | sed -n '6'p | awk '{printf"%.5f",  $3} '`
#gamma=`$HOME/script/lattice.py | sed -n '7'p | awk '{printf"%.5f",  $3} '`



#rm -f $outfile
#rm -f $outfile""_*
#echo "!BIOSYM archive 3" > $outfile
#echo "PBC=ON" >> $outfile
#func(){
#	echo "Auto Generated CAR File"  >>  $outfile""_$i
#	echo "!DATE `date | sed 's/CST / /g'`" >> $outfile""_$i
#	echo "PBC   $a  $b  $c  $alpla  $beta  $gamma (P1)" >> $outfile""_$i
#	ionsend=$((atomsnum * i + i * 2))
#	onsstart=$(( ionsend - atomsnum + 1))
#	awk '{if(NR>="'$onsstart'" && NR <= "'$ionsend'"){printf "%-5s %14.9f %14.9f %14.9f XXXX 1       xx     %-2s 0.0000\n", $1NR,$2,$3,$4,$1 }}' $infile >> $outfile""_$i
#	echo end >> $outfile""_$i
#	echo end >> $outfile""_$i
#}
#for i in `seq 1 $frames `
#do
#	func &
#done
#wait
#for i in `seq 1 $frames `
#do
#	echo "Auto Generated CAR File"  >> $outfile 
#	echo "!DATE `date | sed 's/CST / /g'`" >> $outfile
#	echo "PBC   $a  $b  $c  $alpla  $beta  $gamma (P1)" >> $outfile
#	cat $outfile""_$i >> $outfile
#	rm -rf $outfile""_$i
#	ionsend=$((atomsnum * i + i * 2))
#	ionsstart=$(( ionsend - atomsnum + 1))
#	sed -n ''$ionsstart','$ionsend''p $infile | awk '{printf "%-5s %14.9f %14.9f %14.9f XXXX 1       xx     %-2s 0.0000\n", $1NR,$2,$3,$4,$1 }' >> $outfile""_$i
#	echo end >> $outfile
#	echo end >> $outfile
#done
#eval cat  test.arc_{1..$frames} >> $outfile
#rm $outfile""_*
#sz $outfile

#echo $atomsnum
awk 'BEGIN{"head -1 '$infile'"|getline n;n=n+2
	while("sed -n '3,5'p POSCAR|xargs"|getline ){
		a=($1*$1+$2*$2+$3*$3)^0.5
		b=($4*$4+$5*$5+$6*$6)^0.5
		c=($7*$7+$8*$8+$9*$9)^0.5
		aa=($4*$7+$5*$8+$6*$9)/(b*c);alpla=atan2((1-aa^2)^0.5,aa)*180/3.1415926535898
		ab=($1*$7+$2*$8+$3*$9)/(a*c);beta=atan2((1-ab^2)^0.5,ab)*180/3.1415926535898
		ac=($1*$4+$2*$5+$3*$6)/(a*b);gamma=atan2((1-ac^2)^0.5,ac)*180/3.1415926535898
	};close("POSCAR");close("'$infile'")
	}
	{if(NR==1)
		{printf"!BIOSYM archive 3\nPBC=ON\nAuto Generated CAR File\n!DATE %s\n",strftime("%a %b %e %H:%M:%S  %Y")}
	else if(NR%n==1)
		{printf"Auto Generated CAR File\n!DATE %s\n",strftime("%a %b %e %H:%M:%S  %Y")}
	else if(NR%n==2)
		{printf"PBC   %.5f  %.5f  %.5f  %.5f  %.5f  %.5f (P1)\n",a,b,c,alpla,beta,gamma}
	else if(NR%n==0)
		{printf "%-5s %14.9f %14.9f %14.9f XXXX 1       xx     %-2s 0.0000\nend\nend\n", $1(NR-2)%n,$2,$3,$4,$1 }
	else
		{printf "%-5s %14.9f %14.9f %14.9f XXXX 1       xx     %-2s 0.0000\n", $1(NR-2)%n,$2,$3,$4,$1 }
	}' $infile > $outfile


sz $outfile
rm $outfile

