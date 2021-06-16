#!/bin/sh
atom_num_plus_2=83
Step=5000
PBC=(11.55661 11.55661 18.000 90.000 90.000 120.000)
JOB_NAME=temp

tail -$(($atom_num_plus_2*$Step)) OUT.ANI | awk -v a=${PBC[0]} -v b=${PBC[1]} -v c=${PBC[2]} -v alpha=${PBC[3]} -v beta=${PBC[4]} -v gamma=${PBC[5]} 'BEGIN{printf "!BIOSYM archive 3\nPBC=ON\n"} NF>2{if($1=="STEP") printf "end\nend\n\n!DATE\nPBC%10.4f%10.4f%10.4f%10.4f%10.4f%10.4f (P 1)\n",a,b,c,alpha,beta,gamma;else printf "%-5s%15.9f%15.9f%15.9f%23s\n",$1,$2,$3,$4,$1}END{printf "end\nend\n"}' | sed '3,4d' > $JOB_NAME.arc

