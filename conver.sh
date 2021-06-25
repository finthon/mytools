filelist=`ls /work/mse-zhouc/cif/NiAl`
cd NiAl
for file in $filelist
do 
c=${file%.*}
b=".cif"
ase convert $file $c$b
done
