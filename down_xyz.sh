#!/bin/bash

a="_300.xyz"
b="amine_300K_xyz"
c="amine_"
mkdir $b
#for i in 2.4  2.5  2.6  2.8 3.2  3.4 3.5 3.6 3.8 4.0 4.2  4.4  4.6  4.8 5.0
#for i in 2.3  2.4  2.5  2.6  3.0  3.2  3.4  3.5  3.6  3.8  4.0  4.2  4.4  4.6  4.8  5.0
#for i in 2.4 2.5  2.6 2.7 2.8  3.0  3.2  3.4 3.5 3.6  3.8  4.0  4.2  4.4  4.6  4.8  5.0
#for i in 2.4 2.5  2.6 2.7 2.8  3.0  3.2  3.4  3.6  3.8  4.0  4.2  4.4  4.6  4.8  5.0  5.2 5.4
#for i in 2.4 2.5 2.6 2.8 3.0 3.2  3.6 3.8 4.0 4.2 4.4 4.6 4.8 5.0 5.2 5.4
#for i in 2.4 2.5 2.6 2.8 3.2 3.4  3.6 3.8 4.0 4.2 4.4 4.6 4.8 5.0 5.2 5.4
for i in 2.4 2.5 2.6 2.8 3.0 3.2 3.4 3.5 3.6 3.8 4.0 4.2 4.4 4.6 4.8 5.0
do
cp $i/3w-pos-1.xyz $b
mv $b/3w-pos-1.xyz $b/$c$i$a
done
