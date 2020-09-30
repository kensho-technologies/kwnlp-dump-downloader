# Copyright 2020-present Kensho Technologies, LLC.
from kwnlp_dump_downloader import argconfig
from kwnlp_dump_downloader.dump_status import get_dump_status


def main() -> None:

    description = "get Wikipedia dump status"
    arg_names = ["wp_yyyymmdd", "mirror_url", "wiki", "loglevel"]
    parser = argconfig.get_argparser(description, arg_names)

    args = parser.parse_args()
    dump_status = get_dump_status(args.wp_yyyymmdd, mirror_url=args.mirror_url, wiki=args.wiki)
    print(dump_status.report())
