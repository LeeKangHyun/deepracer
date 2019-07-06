#!/bin/bash

OS_NAME="$(uname | awk '{print tolower($0)}')"

SHELL_DIR=$(dirname $0)

URLS=${SHELL_DIR}/urls.txt
COUNT=$(cat ${URLS} | wc -l | xargs)

_prepare() {
    mkdir -p ${SHELL_DIR}/build
    mkdir -p ${SHELL_DIR}/target

    if [ -f ${SHELL_DIR}/build/points.log ]; then
        rm -rf ${SHELL_DIR}/build/points.log
    fi
}

_build() {
    IDX=1
    while read URL; do
        curl -sL ${URL} | jq -r '.items[].item | "\"\(.additionalFields.racerName)\" \(.additionalFields.lapTime) \(.additionalFields.points)"' > ${SHELL_DIR}/build/board_${IDX}_100.log
        # curl -sL ${URL} | jq -r '.items[].item | "\"\(.additionalFields.racerName)\" \(.additionalFields.lapTime)"' | head -20 > ${SHELL_DIR}/build/board_${IDX}_20.log
        # &item.additionalFields.racerName=kimwooglae

        IDX=$(( ${IDX} + 1 ))
    done < ${URLS}

    while read LINE; do
        ARR=(${LINE})

        NAME="$(echo ${ARR[0]} | cut -d'"' -f2)"
        TIME="${ARR[1]}"
        POINTS="${ARR[2]}"

        for IDX in {2..3}; do
            ARR=($(cat ${SHELL_DIR}/build/board_${IDX}_100.log | grep "\"${NAME}\""))

            SUB_TIME="${ARR[1]}"
            SUB_POINTS="${ARR[2]}"

            if [ "${SUB_TIME}" != "" ]; then
                if [ "${SUB_POINTS}" == "null" ]; then
                    SUB_POINTS=$(perl -e "print 1000-${ARR[1]:3}")
                fi

                POINTS=$(perl -e "print ${POINTS}+${SUB_POINTS}")
            fi
        done

        echo "${POINTS} ${NAME}" >> ${SHELL_DIR}/build/points.log
    done < ${SHELL_DIR}/build/board_1_100.log

    echo "*DeepRacer Virtual Circuit*" > ${SHELL_DIR}/target/message.log
    cat ${SHELL_DIR}/build/points.log | sort -r -g | head -20 | nl >> ${SHELL_DIR}/target/message.log
}

_slack() {
    if [ -z ${SLACK_TOKEN} ]; then
        return
    fi

    json="{\"text\":\"$(cat ${SHELL_DIR}/target/message.log)\"}"

    webhook_url="https://hooks.slack.com/services/${SLACK_TOKEN}"
    curl -s -d "payload=${json}" "${webhook_url}"
}

_prepare

_build

_slack
