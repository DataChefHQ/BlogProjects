import os

from great_expectations_emr.config import GreatExpectationConfig

GE_CONFIG_FILE_NAME = "great_expectations.yml"


def get_ge_config_path(context_root_dir: str) -> str:
    """Return great expectation config path relative to context_root_dir.

    :param context_root_dir: Great Expectations context root directory.
    :type context_root_dir: str
    """
    return os.path.join(context_root_dir, GE_CONFIG_FILE_NAME)


def update_ge_config(
        context_root_dir: str,
        s3_bucket: str = None,
        keep_s3_history: bool = False,
        s3_prefix: str = "",
) -> None:
    """Update Great Expectation's config file in context_root_dir based on the input
    values.

    :param context_root_dir: Great Expectations context root directory.
    :param s3_bucket: Use S3 bucket to deploy data docs when validation finished.
    :param keep_s3_history: If True, will add any validation result (the json
      object, not the HTML output) that is available on S3 bucket, to data docs
      index page. This also needs s3_bucket to be defined.
    :param s3_prefix: S3 prefix string.
    """
    config_path = get_ge_config_path(context_root_dir)
    gce = generate_ge_config(s3_bucket, keep_s3_history, s3_prefix, context_root_dir)
    gce.save(config_path)


def generate_ge_config(
        s3_bucket: str = None,
        keep_s3_history: bool = False,
        s3_prefix: str = None,
        context_root_dir: str = None
) -> GreatExpectationConfig:
    """Generate great expection's config based on the input values.

    :param s3_bucket: Use S3 bucket to deploy data docs when validation finished.
    :param keep_s3_history: If True, will add any validation result (the json
      object, not the HTML output) that is available on S3 bucket, to data docs
      index page. This also needs s3_bucket to be defined.
    :param s3_prefix: S3 prefix string.
    :param context_root_dir: Great Expectations context root directory.
    """
    default_config_path = get_ge_config_path(context_root_dir)
    gce = GreatExpectationConfig(default_config_path)

    if s3_bucket:
        gce.set_s3_site(s3_bucket, s3_prefix=s3_prefix)

    if s3_bucket and keep_s3_history:
        gce.set_s3_validation_store(s3_bucket)

    return gce
