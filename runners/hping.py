import logging
import shutil
import json
import os

from textwrap import dedent

from leotest.errors import RunnerError
from leotest.runner import LeotestRunner
from leotest.utils import execute

logger = logging.getLogger(__name__)

class HPingClient(LeotestRunner):
    """Run hping tests."""

    def __init__(self, testname, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            name = testname, 
            title="hping3",
            description="Measure rtt using TCP syn-ack",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id)
                
    def _start_test(self, artifact_name):
        logger.info("Starting hping3 test...")
        if shutil.which("hping3") is not None:
            ip = self._config["tests"][self.name]["ip"]
            port = self._config["tests"][self.name]["port"]
            num_pings = self._config["tests"][self.name]["num_pings"]
            timeout = self._config["tests"][self.name]["test_length"]
            
            # sudo hping3 netperf-eu.bufferbloat.net -S -p 80 -c 5
            if num_pings:
                starttime, endtime, output = execute(
                    "hping3", 
                    ip,
                    "-S",
                    p = str(port),
                    c = str(num_pings) 
                )
            else:
                starttime, endtime, output = execute(
                    "hping3", 
                    ip,
                    "-S",
                    p = port,
                    t = timeout 
                )
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

            metadata = os.path.join(self.artifact_path, "metadata.log")
            logger.info('Writing metadata to {}'.format(metadata))
            with open(metadata, 'w', encoding='utf-8') as f:
                json.dump(leotest_output, f, ensure_ascii=False, indent=4)
            
            return json.dumps(leotest_output)

        else:
            raise RunnerError(
                "hping3",
                "Executable does not exist, please install ping.")