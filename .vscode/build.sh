#!/usr/bin/env bash
CLI_LOCATION="$(pwd)/cli"
echo "Building plugin in $(pwd)"

SYSTEM_ARCH="$(uname -a)"

if [[ "$SYSTEM_ARCH" =~ "Darwin" ]]; then
    $CLI_LOCATION/decky plugin build $(pwd)
else
    printf "Please input sudo password to proceed.\n"

    # read -s sudopass

    # printf "\n"

    echo $sudopass | sudo $CLI_LOCATION/decky plugin build $(pwd)
fi
