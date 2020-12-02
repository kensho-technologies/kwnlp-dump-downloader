# Copyright 2020-present Kensho Technologies, LLC.
import logging

from kwnlp_dump_downloader import argconfig
from kwnlp_dump_downloader.downloader import download_jobs

logger = logging.getLogger(__name__)


def main() -> None:

    description = "download Wikimedia data"
    arg_names = [
        "wp_yyyymmdd",
        "wd_yyyymmdd",
        "data_path",
        "mirror_url",
        "wiki",
        "jobs",
        "loglevel",
    ]
    parser = argconfig.get_argparser(description, arg_names)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    logger.info(f"args={args}")
    jobs_to_download = args.jobs.strip().split(",")
    logger.info(f"jobs_to_download={jobs_to_download}")

    download_jobs(
        args.wp_yyyymmdd,
        args.wd_yyyymmdd,
        data_path=args.data_path,
        mirror_url=args.mirror_url,
        wiki=args.wiki,
        jobs_to_download=jobs_to_download,
    )


if __name__ == "__main__":
    main()
