#!/bin/bash

papeer list https://www.economist.com/weeklyedition/ -o json --selector='div.layout-weekly-edition-wtw>ul>li>a' > ./temp/articlelist.json