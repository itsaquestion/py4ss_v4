#!/bin/sh
cp plotly.js _book/book_parts/case_study
git add .
git commit -m "$1"
git push
./sync.sh
