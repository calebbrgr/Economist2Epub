#!/bin/bash
curl $1 -s -L -I -o /dev/null -w '%{url_effective}'