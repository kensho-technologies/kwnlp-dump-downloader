# Copyright 2020-present Kensho Technologies, LLC.
"""Download wikimedia dumps."""
from calendar import monthrange
import datetime
import logging
import os
from typing import Iterable, List

import wget

from kwnlp_dump_downloader import argconfig
from kwnlp_dump_downloader.dump_status import WikimediaDumpStatus

logger = logging.getLogger(__name__)


def _check_requests_against_status(
    dump_status: WikimediaDumpStatus, jobs_to_download: Iterable[str]
) -> bool:
    proceed = True
    for job_name in jobs_to_download:
        if dump_status.jobs[job_name].status == "done":
            mark = "\u2705"
        elif dump_status.jobs[job_name].status == "waiting":
            mark = "\u274c"
            proceed = False
        else:
            mark = ""
            proceed = False
        logger.info("{}: {} {}".format(job_name, dump_status.jobs[job_name].status, mark))
    return proceed


def _download_wikipedia_job(
    dump_status: WikimediaDumpStatus,
    job_name: str,
    out_path: str,
    mirror_url: str,
) -> None:
    """Download a "standard" job (i.e. one included in dump_status)."""
    if job_name not in dump_status.jobs:
        raise ValueError(
            "job name {} not in dump_status.jobs {}".format(job_name, dump_status.jobs.keys())
        )

    job = dump_status.jobs[job_name]
    job_path = os.path.join(out_path, job_name)
    os.makedirs(job_path, exist_ok=True)
    for wdsfile in job.files.values():
        download_url = "{}/{}".format(mirror_url, wdsfile.url)
        out = os.path.join(job_path, wdsfile.name)
        logger.info(f"downloading {job_name} from {download_url} to {out}")
        if os.path.exists(out):
            logger.info("{} exists, skipping".format(out))
        else:
            wget.download(download_url, out=out)


def _download_pageviewcomplete(
    wp_yyyymmdd: str,
    out_path: str,
    mirror_url: str,
) -> None:
    wp_date = datetime.date(
        year=int(wp_yyyymmdd[0:4]),
        month=int(wp_yyyymmdd[4:6]),
        day=int(wp_yyyymmdd[6:8]),
    )

    job_name = "pageviewcomplete"
    job_path = os.path.join(out_path, job_name)
    os.makedirs(job_path, exist_ok=True)
    wp_date_minus_one_month = wp_date.replace(day=1) - datetime.timedelta(days=1)
    year = wp_date_minus_one_month.year
    month = wp_date_minus_one_month.month
    _, days_in_month = monthrange(wp_date_minus_one_month.year, wp_date_minus_one_month.month)
    for day in range(1, days_in_month + 1):

        pageview_file = "pageviews-{}{:0>2d}{:0>2d}-user.bz2".format(year, month, day)
        download_url = "{}/other/pageview_complete/{}/{}-{:0>2d}/{}".format(
            mirror_url, year, year, month, pageview_file)
        out = os.path.join(job_path, pageview_file)
        logger.info(f"downloading {job_name} from {download_url} to {out}")
        if os.path.exists(out):
            logger.info(f"{out} exists, skipping")
        else:
            wget.download(download_url, out=out)


def _download_wikidata(
    wd_yyyymmdd: str,
    out_path: str,
    mirror_url: str,
) -> None:
    os.makedirs(out_path, exist_ok=True)
    wikidata_dump_file = "wikidata-{}-all.json.bz2".format(wd_yyyymmdd)
    download_url = "{}/wikidatawiki/entities/{}/{}".format(
        mirror_url, wd_yyyymmdd, wikidata_dump_file
    )
    out = os.path.join(out_path, wikidata_dump_file)
    logger.info(f"downloading wikidata from {download_url} to {out}")
    if os.path.exists(out):
        logger.info("{} exists, skipping".format(out))
    else:
        wget.download(download_url, out=out)


def download_jobs(
    wp_yyyymmdd: str,
    wd_yyyymmdd: str,
    data_path: str = argconfig.DEFAULT_KWNLP_DATA_PATH,
    mirror_url: str = argconfig.DEFAULT_KWNLP_WIKI_MIRROR_URL,
    wiki: str = argconfig.DEFAULT_KWNLP_WIKI,
    jobs_to_download: List[str] = argconfig.DEFAULT_KWNLP_DOWNLOAD_JOBS.split(","),
) -> None:

    # parse input
    # =====================================================================
    if "wikidata" in jobs_to_download:
        include_wikidata = True
        jobs_to_download.remove("wikidata")
    else:
        include_wikidata = False

    if "pageviewcomplete" in jobs_to_download:
        include_pageviewcomplete = True
        jobs_to_download.remove("pageviewcomplete")
    else:
        include_pageviewcomplete = False

    # get wikipedia dump status
    # =====================================================================
    url = "{}/{}/{}/dumpstatus.json".format(mirror_url, wiki, wp_yyyymmdd)
    logger.info(f"retrieving dump status from : {url}")
    dump_status = WikimediaDumpStatus.from_url(url)
    proceed = _check_requests_against_status(dump_status, jobs_to_download)
    if not proceed:
        return

    # set output paths
    # =====================================================================
    if jobs_to_download or include_pageviewcomplete:
        wikipedia_dumps_path = os.path.join(data_path, f"wikipedia-raw-{wp_yyyymmdd}")
        logger.info(f"wikipedia_dumps_path: {wikipedia_dumps_path}")
        os.makedirs(wikipedia_dumps_path, exist_ok=True)

    if include_wikidata:
        wikidata_dumps_path = os.path.join(data_path, f"wikidata-raw-{wd_yyyymmdd}")
        logger.info(f"wikidata_dumps_path: {wikidata_dumps_path}")
        os.makedirs(wikidata_dumps_path, exist_ok=True)

    # download wikipedia pageviewcomplete for the month previous to wp_yyyymmdd
    # =====================================================================
    if include_pageviewcomplete:
        _download_pageviewcomplete(wp_yyyymmdd, wikipedia_dumps_path, mirror_url)

    # download wikipedia dumps
    # =====================================================================
    for job_name in jobs_to_download:
        _download_wikipedia_job(dump_status, job_name, wikipedia_dumps_path, mirror_url)

    # download wikidata dump
    # =====================================================================
    if include_wikidata:
        _download_wikidata(wd_yyyymmdd, wikidata_dumps_path, mirror_url)
