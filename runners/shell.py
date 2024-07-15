import logging
import shutil
import json
import os

# import pingparsing
from textwrap import dedent

from leotest.errors import RunnerError
from leotest.runner import LeotestRunner
from leotest.utils import execute

logger = logging.getLogger(__name__)

class ShellClient(LeotestRunner):
    """Run arbitrary shell scripts."""

    def __init__(self, testname, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            name = testname,
            title="Shell",
            description="Run arbitrary shell scripts",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id)


    def _start_test(self, artifact_name):
        logger.info("Starting shell test...")
        if shutil.which("bash") is not None:
            
            url = self._config["tests"][self.name]["url"]

            starttime, _, curl_output = execute("curl", "--output", "test.sh", url)
            _, endtime, bash_output = execute("bash", "test.sh")

            output = curl_output.stdout + bash_output.stdout
            self.write_raw_stdout(bash_output, self.artifact_path)

            leotest_output = {
                'TestName': self.name,
                'TestStartTime': starttime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'TestEndTime': endtime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'LeotestLocation': self._location,
                'LeotestConnectionType': self._connection_type,
                'LeotestNetworkType': self._network_type,
                'LeotestDeviceID': self._device_id,
                'Output': output
            }

            # write stdout
            metadata = os.path.join(self.artifact_path, "metadata.log")
            logger.info('Writing metadata to {}'.format(metadata))

            with open(metadata, 'w', encoding='utf-8') as f:
                json.dump(leotest_output, f, ensure_ascii=False, indent=4)

            return json.dumps(leotest_output)

        else:
            raise RunnerError(
                "bash",
                "Executable does not exist, please install bash.")
