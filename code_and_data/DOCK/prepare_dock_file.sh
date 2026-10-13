#!/bin/bash

#工作目录

for ORname in */; do

  ORname=${ORname%/}


  cp "../3-ligands/"*.{id,sdi} "$ORname/"


  sed -i 's/DOCK 3.7 parameter/DOCK 3.8 parameter/g' "$ORname/INDOCK"
  sed -i 's/mol2_score_maximum            -10.0/mol2_score_maximum            100/g' "$ORname/INDOCK"
  sed -i 's/atom_minimum                  4/atom_minimum                  2/g' "$ORname/INDOCK"
  sed -i 's/atom_maximum                  25/atom_maximum                  100/g' "$ORname/INDOCK"
  
  (cd "$ORname" && "$DOCKBASE/docking/setup/setup_db2_zinc15_file_number.py" ./ controls controls.sdi 1 count)
done