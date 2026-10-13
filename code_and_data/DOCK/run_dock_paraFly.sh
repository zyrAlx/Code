#!/bin/bash


work_path="/home/zhangtm/Insect/Fun_evolution_analysis/All_OR_DOCK/4-default_parameters"

for ORname in */; do

  ORname=${ORname%/}


  echo "cd ${ORname}/controls0000 && /home/zhangtm/software/DOCK-3.8/DOCK_Release_Apr_21_2023/dock3/dock64 && cd ${work_path}" >> run_dock_parafly.txt
done