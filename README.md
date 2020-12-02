# Kensho Wikimedia for Natural Language Processing - Dump Downloader

kwnlp_dump_downloader is a Python package to help you download raw [Wikimedia dumps](https://dumps.wikimedia.org/).

# Quick Install (Requires Python >= 3.6)

```bash
pip install kwnlp-dump-downloader
```

# Python Package

This python package provides two main pieces of functionality.  The first allows you to check the status of a Wikipedia dump and the second allows you to download specific parts of a Wikipedia dump (called jobs).

## Checking Status

```python
from kwnlp_dump_downloader import get_dump_status
wp_yyyymmdd = "20200920"
wds = get_dump_status(wp_yyyymmdd)
print(wds.report())
```

```bash
abstractsdump: done ✅
abstractsdumprecombine: done ✅
allpagetitlesdump: done ✅
articlesdump: done ✅
articlesdumprecombine: done ✅
articlesmultistreamdump: done ✅
articlesmultistreamdumprecombine: done ✅
babeltable: done ✅
categorylinkstable: done ✅
categorytable: done ✅
changetagdeftable: done ✅
changetagstable: done ✅
externallinkstable: done ✅
flaggedimagestable: done ✅
flaggedpageconfigtable: done ✅
flaggedpagependingtable: done ✅
flaggedpagestable: done ✅
flaggedrevspromotetable: done ✅
flaggedrevsstatisticstable: done ✅
flaggedrevstable: done ✅
flaggedrevstrackingtable: done ✅
flaggedtemplatestable: done ✅
geotagstable: done ✅
imagelinkstable: done ✅
imagetable: done ✅
iwlinkstable: done ✅
langlinkstable: done ✅
metacurrentdump: done ✅
metacurrentdumprecombine: done ✅
metahistory7zdump: done ✅
metahistorybz2dump: done ✅
namespaces: done ✅
pagelinkstable: done ✅
pagepropstable: done ✅
pagerestrictionstable: done ✅
pagetable: done ✅
pagetitlesdump: done ✅
protectedtitlestable: done ✅
redirecttable: done ✅
sitestable: done ✅
sitestatstable: done ✅
templatelinkstable: done ✅
userformergroupstable: done ✅
usergroupstable: done ✅
wbcentityusagetable: done ✅
xmlpagelogsdump: done ✅
xmlpagelogsdumprecombine: done ✅
xmlstubsdump: done ✅
xmlstubsdumprecombine: done ✅
```

## Downloading Jobs

```python
from kwnlp_dump_downloader import download_jobs
wp_yyyymmdd = "20200920"
wd_yyyymmdd = "20200921"
data_path = "/path/where/data/should/live"
jobs_to_download = ["pagetable", "articlesdump"]
download_jobs(wp_yyyymmdd, wd_yyyymmdd, data_path=data_path, jobs_to_download=jobs_to_download)
```

Any of the jobs listed in the status report above can be specified in the `jobs_to_download` kwarg. In addition, there are two special job strings,

* `pageviewcomplete`: used to download monthly pageviews (e.g. `pageviews-20200901-user.bz2`)
* `wikidata`: used to download Wikidata json dumps (e.g. `wikidata-20200921-all.json.bz2`)


# Command Line Interface

If you prefer to use the command line to check status and download dumps, you can do that too. After pip installing this package, you should have two new commands available,

## Checking Status

```bash
usage: kwnlp-get-dump-status [-h] [--mirror_url MIRROR_URL] [--wiki WIKI] [--loglevel LOGLEVEL] wp_yyyymmdd

get Wikipedia dump status

positional arguments:
  wp_yyyymmdd           date string for Wikipedia dump (e.g. 20200920)

optional arguments:
  -h, --help            show this help message and exit
  --mirror_url MIRROR_URL
                        base URL for Wikimedia dumps (e.g. https://dumps.wikimedia.org)
  --wiki WIKI           selects which language wikipedia to use (e.g. enwiki)
  --loglevel LOGLEVEL   python logging level integer (e.g. 20)
```

## Downloading Jobs

```bash
usage: kwnlp-download-jobs [-h] [--data_path DATA_PATH] [--mirror_url MIRROR_URL] [--wiki WIKI] [--jobs JOBS]
                           [--loglevel LOGLEVEL]
                           wp_yyyymmdd wd_yyyymmdd

download Wikimedia data

positional arguments:
  wp_yyyymmdd           date string for Wikipedia dump (e.g. 20200920)
  wd_yyyymmdd           date string for Wikidata dump (e.g. 20200921)

optional arguments:
  -h, --help            show this help message and exit
  --data_path DATA_PATH
                        path to top level data directory (e.g. /data/wikimedia-ingestion)
  --mirror_url MIRROR_URL
                        base URL for Wikimedia dumps (e.g. https://dumps.wikimedia.org)
  --wiki WIKI           selects which language wikipedia to use (e.g. enwiki)
  --jobs JOBS           comma separated list of job names to download (e.g. pagecounts,pagetable)
  --loglevel LOGLEVEL   python logging level integer (e.g. 20)
```

# License

Licensed under the Apache 2.0 License. Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Copyright 2020-present Kensho Technologies, LLC. The present date is determined by the timestamp of the most recent commit in the repository.
