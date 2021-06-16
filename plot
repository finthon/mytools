#!/bin/bash
if [ $# -eq 0 ];then
  plotfile=result.txt
else
  if [ -e "$1" ];then
    plotfile=$1;
  else
    if [ "$1" == "-f" ];then
      grep FORCES: OUTCAR -a | awk '{print $5}' > result.txt
    elif [ "$1" == "-e" ];then
      grep F OSZICAR -a | awk '{print $5}' > result.txt
    elif [ "$1" == "-m" ];then
      grep F OSZICAR -a | awk '{print $10}' > result.txt
    elif [ "$1" == "-d" ];then
      grep F OSZICAR -a | awk '{print $9}' > result.txt
    fi
    plotfile=result.txt
  fi
fi
if [ ! -e $plotfile ];then
  grep F OSZICAR | awk '{print $5}' > result.txt
fi
xr=$2
yr=$3
gnuplot -persist <<EOF
set xrange [$xr]
set yrange [$yr]
plot '$plotfile'
EOF
