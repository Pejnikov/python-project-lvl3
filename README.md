[![Actions Status](https://github.com/Pejnikov/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/Pejnikov/python-project-lvl3/actions)
![Project tests](https://github.com/Pejnikov/python-project-lvl3/actions/workflows/project-check.yml/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/cf93b925cb9cf01d4a64/maintainability)](https://codeclimate.com/github/Pejnikov/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/cf93b925cb9cf01d4a64/test_coverage)](https://codeclimate.com/github/Pejnikov/python-project-lvl3/test_coverage)

# Web Pages Loader
Simple tool which downloads web pages (and its resources) for local using. 

## Table Of Content
- [Web Pages Loader](#web-pages-loader)
  - [Table Of Content](#table-of-content)
  - [Learn More](#learn-more)
  - [Installation Guide](#installation-guide)
      - [Package:](#package)
      - [Library:](#library)
  - [Usage](#usage)
  - [Troubleshooting](#troubleshooting)


## Learn More
The tool downloads web page and saves it to directory (can be configured - see [Usage](#usage)). New directory is created for page resources with name "***\<page-name\>_files***".

Moreover, it will show the progress of downloading resources.

## Installation Guide

#### Package:
```bath
$ python3 -m pip install --user hexlet-code
$ page-loader <url>
```
#### Library:
```python
from page_loader import download

downloaded_page_path = download(url, directory)
print(downloaded_page_path)
```
## Usage
```bath
$ page-loader https://example.com
Downloading progress: ◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉ 100%
<script_path>/example-com.html
```
```bath
$ ls -h
example-com.html	example-com_files	page-loader
```
## Troubleshooting
It is easy to use the verbose argument for troubleshooting ("-v" - WARNING, "-vv" - INFO "-vvv" - DEBUG):
```bath
./page-loader https://example.com -vvv
2021-11-22 19:38:38,340 page_loader.content_helper DEBUG Processing the page tag: "link" with resource: "/bitrix/js/main/core/css/core.min.css?16256473552854"
2021-11-22 19:38:38,340 page_loader.content_helper DEBUG The resource is suitable: "link" with resource: "/bitrix/js/main/core/css/core.min.css?16256473552854"
```
<br/>
<br/>
<br/>
<div style="text-align: right"> Powered by <img alt="Hexlet" src="https://s3.eu-central-1.amazonaws.com/trengo/media/hc_fav_FxmAO9yYcM.png"></div>

