#!/usr/bin/env Rscript

library(reticulate)

args <- commandArgs(trailingOnly = TRUE)

reticulate::use_python(Sys.which("python3"), required = TRUE)
reticulate::source_python("fb_geoinsights.py")

fb_downloader <- FbGeoinsights()
fb_downloader$fetch(
    start_date = args[1],
    name = args[2],
    loc_id = args[3]
)