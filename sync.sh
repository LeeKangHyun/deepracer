#!/bin/bash

TEMP="/tmp/DeepRacer-SageMaker-RoboMaker-comm-model/"
rm -rf $TEMP
mkdir -p $TEMP

SOURCE="aws-deepracer-3b4bdc58-3fd5-4c15-ba29-0a7aee470679"
SOURCE="s3://${SOURCE}/DeepRacer-SageMaker-RoboMaker-comm-560674140255-20190806095121-c4d7228c-b2a0-484d-bd68-ae2ee58b551c/model/"

TARGET="aws-deepracer-94df3fea-6d7f-407e-bb61-2db52f88eaab"
TARGET="s3://${TARGET}/DeepRacer-SageMaker-RoboMaker-comm-510452226051-20190808004343-d7aade8d-986d-4419-87ce-3c8c4c76a268/model/"

aws s3 sync ${SOURCE} ${TEMP}

aws s3 rm ${TARGET} --recursive

aws s3 sync ${TEMP} ${TARGET}
