import logging
import json
import os

from leotest.errors import RunnerError
from leotest.runner import LeotestRunner
from leotest.utils import execute

logger = logging.getLogger(__name__)

class IGIPTRClient(LeotestRunner):
    """Run igi-ptr tests (another bandwidth probing test)."""

    def __init__(self, testname, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            name = testname, 
            title="IGI-PTR",
            description="Run igi-ptr tests (another bandwidth probing test).",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id)


    def _start_test(self, artifact_name):
        logger.info("Starting IGI test...")
        if os.path.exists("/leotest/leotest/bin/ptr-client"):

            ip = self._config["tests"][self.name]["ip"]
            # port = str(self._config["tests"][self.name]["port"])


            starttime, endtime, output = execute("/leotest/leotest/bin/ptr-client", "-v", ip)
            # write stdout
            self.write_raw_stdout(output, self.artifact_path)
            
            leotest_output = {
                'TestName': self.name,
                'TestStartTime': starttime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'TestEndTime': endtime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'LeotestLocation': self._location,
                'LeotestConnectionType': self._connection_type,
                'LeotestNetworkType': self._network_type,
                'LeotestDeviceID': self._device_id,
            }

            # write stdout
            metadata = os.path.join(self.artifact_path, "metadata.log")
            logger.info('Writing metadata to {}'.format(metadata))

            with open(metadata, 'w', encoding='utf-8') as f:
                json.dump(leotest_output, f, ensure_ascii=False, indent=4)
            
            return json.dumps(leotest_output)

        else:
            raise RunnerError(
                "stab",
                "Executable does not exist, please check whether leotest/runners/ptr-client is executable. (Try sudo chmod +x ptr-client.)")