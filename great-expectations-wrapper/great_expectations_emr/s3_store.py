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
