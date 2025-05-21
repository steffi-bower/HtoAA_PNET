#!/bin/bash

set ERAS = (2 3 4)
set PARTS = (A C D)
foreach ERA ($ERAS)
    foreach PART ($PARTS)
        echo "crab_ParkingBPH$ERA-Run2018$PART-05May2019-v1-MINIAOD" 
        crab resubmit -d "crab_ParkingBPH$ERA-Run2018$PART-05May2019-v1-MINIAOD"