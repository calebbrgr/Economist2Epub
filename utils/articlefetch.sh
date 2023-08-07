#!/bin/bash

papeer list https://www.economist.com/weeklyedition/ -o json --selector='section.layout-weekly-edition-section>div.e16rqvvr0>h3>a' > ./temp/articlelist.json