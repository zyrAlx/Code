rm USalign.sh
mkdir -p All_9513_align_pdb
for i in $(ls 8577+33+903_pdb/*.pdb);
do
#运行命令用（），变量用{}
name=$(basename ${i%%.pdb})
# a another way to express
# name=$(basename $i .pdb)
echo "USalign $i MhOR5.pdb -o All_9513_align_pdb/${name}_alignOR5" >> USalign.sh
done