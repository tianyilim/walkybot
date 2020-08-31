#!/bin/bash

set -e

g++ -Wall sendDataPacket.cpp -lwiringPi -o sendData
echo "Compiliation success"


#Allows us to wait until we actually wish to execute the test prog.
echo "Run the program?"
select yn in "y" "n"; do
    case $yn in
        y ) sudo ./sendData; break;;
        n ) exit;;
    esac
done