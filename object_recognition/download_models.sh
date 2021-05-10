#!/bin/bash
# wget https://danielsawyer.com/gw5q146a9dqd2t82jhu8noe3m-Object-Detector.zip
wget https://data.bris.ac.uk/datasets/tar/gw5q146a9dqd2t82jhu8noe3m.zip
unzip gw5q146a9dqd2t82jhu8noe3m-Object-Detector.zip
mkdir models
mv gw5q146a9dqd2t82jhu8noe3m/* models/
rm -rf gw5q146a9dqd2t82jhu8noe3m