#!/bin/bash

a="_50.LagrangeMultLog"
b="amine_50K"
c="amine_"
mkdir $b
#for i in 2.4  2.5  2.6  2.8  3.0 3.2  3.4  3.5  3.6 3.8  4.0  4.2  4.4  4.6  4.8 5.0 5.2 5.4
#for i in 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2.1 2.3 2.5 2.7 2.9 3.1 3.3
for i in 2.4 2.5  2.6 2.8   3.2  3.4 3.5 3.6  3.8  4.0  4.2  4.4  4.6  4.8  5.0
#for i in 2.4 2.5  2.6 2.7 2.8  3.0  3.2  3.4  3.6  3.8  4.0  4.2  4.4  4.6  4.8  5.0  5.2 5.4
do 
cp $i/3w-1.LagrangeMultLog $b
mv $b/3w-1.LagrangeMultLog $b/$c$i$a
done
