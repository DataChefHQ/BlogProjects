from typing import Any, Dict

import yaml

from great_expectations_emr import s3_store


class GreatExpectationConfig:
    """GreatExpectationConfig is a helper which loads default great expectation
    config and dynamically changes based on the provided input. The default
    config is configured to run on local machine. However using this dynamic
    config interface, it's possible to automatically change the config file on
    the run time.

    :param path: The default config file path.
    :type path: str

    Usage::
      >>> gce = GreatExpectationConfig("/path/to/default_ge.conf")
      >>> gce.set_s3_site("bucket_name", "site_name")
      >>> gce.save()
    """

    def __init__(self, path: str):
        self.path = path
        self.config = self.__read_config__(self.path)

    @staticmethod
    def __read_config__(path: str) -> Dict[Any, Any]:
        """Read config file and parse it from YAML to a Python dict.

        :param path: The config file's path to read.
        :type path: str
        """

        with open(path) as fp:
            content = yaml.load(fp, Loader=yaml.FullLoader)

        return content

    @staticmethod
    def __write_config__(data: dict, path: str) -> None:
        """Write config file in yaml format to the given path.

        :param data: The data object to write.
        :type data: dict
        :param path: The config file's path to write data to.
        :type path: str
        """

        with open(path, "w") as fp:
            yaml.dump(data, fp)

    def set_s3_site(self, bucket: str, site_name: str = "s3_site", s3_prefix: str = None) -> None:
        """Configure the loaded config to use an S3 site to deploy data docs to.

        :param bucket: The S3 bucket name.
        :type bucket: str
        :param site_name: The deployed data docs site name.
        :type site_name: str
        :param s3_prefix: S3 bucket name.
        :type s3_prefix: str
        """

        self.config["data_docs_sites"] = s3_store.s3_site(bucket, site_name, s3_prefix)

    def set_s3_validation_store(self, bucket: str) -> None:
        """Set s3 bucket to store validation results.

        :param bucket: The S3 bucket name.
        :type bucket: str
        """
        self.config["stores"]["validations_store"] = s3_store.validation_store(bucket)

    def save(self, path: str = None) -> None:
        """Save current config object into the given path in proper format.

        :param path: The path to store the config in.
        :type path: str
        """

        self.__write_config__(self.config, path or self.path)
