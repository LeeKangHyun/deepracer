#!/bin/bash

OS_NAME="$(uname | awk '{print tolower($0)}')"

SHELL_DIR=$(dirname $0)

TEMP_DIR=${SHELL_DIR}/build
mkdir -p ${TEMP_DIR}

URLS=${SHELL_DIR}/points.txt
COUNT=$(cat ${URLS} | wc -l | xargs)

echo "Pointes RacerName" > ${TEMP_DIR}/points.log

IDX=1
while read URL; do
    curl -sL ${URL} | jq -r '.items[].item | "\"\(.additionalFields.racerName)\" \(.additionalFields.lapTime) \(.additionalFields.points)"' > ${TEMP_DIR}/board_${IDX}_100.log
    # curl -sL ${URL} | jq -r '.items[].item | "\"\(.additionalFields.racerName)\" \(.additionalFields.lapTime)"' | head -20 > ${TEMP_DIR}/board_${IDX}_20.log

    IDX=$(( ${IDX} + 1 ))
done < ${URLS}

while read LINE; do
    ARR=(${LINE})

    NAME="$(echo ${ARR[0]} | cut -d'"' -f2)"
    TIME="${ARR[1]}"
    POINTS="${ARR[2]}"

    # echo "${NAME} ${TIME}"

    for IDX in {2..3}; do
        ARR=($(cat ${TEMP_DIR}/board_${IDX}_100.log | grep "\"${NAME}\""))

        SUB_TIME="${ARR[1]}"
        SUB_POINTS="${ARR[2]}"

        if [ "${SUB_TIME}" != "" ]; then
            if [ "${SUB_POINTS}" == "null" ]; then
                # SUB_POINTS="${ARR[1]:3}"
                SUB_POINTS=$(perl -e "print 1000-${ARR[1]:3}")
            fi

            # POINTS=$(( ${POINTS} + ${SUB_POINTS} ))
            POINTS=$(perl -e "print ${POINTS}+${SUB_POINTS}")
        fi
    done

    echo "${POINTS} ${NAME}" >> ${TEMP_DIR}/points.log

done < ${TEMP_DIR}/board_1_100.log

cat ${TEMP_DIR}/points.log | sort -r --version-sort | head -30 | column -t
