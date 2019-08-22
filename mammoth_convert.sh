#!/bin/bash

for f in *.docx; do
    mammoth "$f" "${f%.docx}.html"
done
