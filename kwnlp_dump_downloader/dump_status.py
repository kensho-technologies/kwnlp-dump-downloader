# Copyright 2020-present Kensho Technologies, LLC.
from dataclasses import dataclass
from typing import Dict

import requests

from kwnlp_dump_downloader import argconfig


@dataclass
class WdsFile:
    name: str
    sha1: str
    md5: str
    size: int
    url: str


@dataclass
class WdsJob:
    name: str
    status: str
    files: Dict[str, WdsFile]
    updated: str


@dataclass
class WikimediaDumpStatus:

    jobs: Dict[str, WdsJob]
    version: str

    def __init__(self, dumpstatus: Dict) -> None:
        self._dumpstatus = dumpstatus
        self.version = dumpstatus["version"]
        self.jobs = {}
        for jobname, job in dumpstatus["jobs"].items():
            files = {
                filename: WdsFile(
                    name=filename,
                    sha1=fileinfo.get("sha1", ""),
                    md5=fileinfo.get("md5", ""),
                    size=fileinfo.get("size", 0),
                    url=fileinfo.get("url", ""),
                )
                for filename, fileinfo in job.get("files", {}).items()
            }
            job = WdsJob(name=jobname, status=job["status"], updated=job["updated"], files=files)
            self.jobs[jobname] = job

    @classmethod
    def from_url(cls, url: str) -> "WikimediaDumpStatus":
        try:
            res = requests.get(url)
        except requests.exceptions.RequestException as oops:
            raise SystemExit(oops)
        res.raise_for_status()
        return cls(res.json())

    def report(self) -> str:
        job_strings = []
        for jobname in sorted(self.jobs.keys()):
            if self.jobs[jobname].status == "done":
                mark = "\u2705"
            elif self.jobs[jobname].status == "waiting":
                mark = "\u274c"
            else:
                mark = ""
            job_strings.append("{}: {} {}".format(jobname, self.jobs[jobname].status, mark))
        return "\n".join(job_strings)


def get_dump_status(
    wp_yyyymmdd: str,
    mirror_url: str = argconfig.DEFAULT_KWNLP_WIKI_MIRROR_URL,
    wiki: str = argconfig.DEFAULT_KWNLP_WIKI,
) -> WikimediaDumpStatus:
    url = "{}/{}/{}/dumpstatus.json".format(mirror_url, wiki, wp_yyyymmdd)
    wds = WikimediaDumpStatus.from_url(url)
    return wds
