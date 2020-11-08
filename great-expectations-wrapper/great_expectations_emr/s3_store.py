from typing import List

import boto3
import logging

DEFAULT_VALIDATION_STORE_PREFIX = "validations/store/"
client = boto3.client("s3")

logger = logging.getLogger("great_expectations_wrapper")


class GEClassNames(object):
    """Great Expectation config classes.
    """

    tuple_s3_store_backend = "TupleS3StoreBackend"
    validations_store = "ValidationsStore"
    site_builder = "SiteBuilder"


def store_backend(bucket_name: str, prefix: str = None) -> dict:
    """Generate store backend config for great expectations.

    :param bucket_name: store bucket name.
    :type bucket_name: str
    :param prefix: object prefix to use for object path storage.
    :type prefix: str
    """
    response = {
        "class_name": GEClassNames.tuple_s3_store_backend,
        "bucket": bucket_name
    }

    if prefix:
        response["prefix"] = prefix

    return response


def validation_store(
    bucket_name: str, validation_store_prefix: str = DEFAULT_VALIDATION_STORE_PREFIX
) -> dict:
    """Generate validation store config for great expectations.

    :param bucket_name: store bucket name.
    :type bucket_name: str
    :param validation_store_prefix: object prefix to use for object path storage.
    :type validation_store_prefix: str
    """
    response = {
        "class_name": GEClassNames.validations_store,
        "store_backend": store_backend(bucket_name, validation_store_prefix),
    }

    return response


def s3_site(bucket_name: str, site_name: str, s3_prefix: str = None) -> dict:
    """Generate s3 site config for great expectations.

    :param bucket_name: site bucket name.
    :type bucket_name: str
    :param site_name: site name.
    :type site_name: str
    :param s3_prefix: S3 prefix name.
    :type s3_prefix: str
    """
    response = {
        site_name: {
            "class_name": GEClassNames.site_builder,
            "store_backend": store_backend(bucket_name, s3_prefix),
        }
    }

    return response


def move_previous_validations(
    bucket_name: str = "carnext-datalake-dashboards-sandbox",
    source_prefix: str = "data_doc",
    dest_prefix: str = "previous_validations",
):
    s3 = boto3.resource("s3")
    print(f"Moving previous validations from {bucket_name}/{source_prefix} to {bucket_name}/{dest_prefix}")

    items = _retrieve_previous_validations(bucket_name, source_prefix)
    bucket = s3.Bucket(bucket_name)
    for item in items:
        print(f"Moving {item}")
        copy_source = {"Bucket": bucket_name, "Key": item["Key"]}
        bucket.copy(copy_source, f"{dest_prefix}/{item['Key']}")
        bucket.Object(item["Key"]).delete()


def _retrieve_previous_validations(bucket_name: str, source_prefix: str) -> List[dict]:
    items = []

    def retrieve_validations(next_marker: str = None):
        if next_marker:
            return client.list_objects(
                Bucket=bucket_name, Prefix=source_prefix, NextMarker=next_marker
            )
        else:
            return client.list_objects(Bucket=bucket_name, Prefix=source_prefix)

    response = retrieve_validations()

    while response["IsTruncated"]:
        items += response["Contents"]

    if response.get("Contents"):
        items += response["Contents"]

    return items
