import logging
import shutil
import json
import os

from textwrap import dedent

from leotest.errors import RunnerError
from leotest.runner import LeotestRunner
from leotest.utils import execute

logger = logging.getLogger(__name__)

class IPerfClient(LeotestRunner):
    """Run iPerf tests."""

    def __init__(self, testname, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            name = testname, 
            title="iPerf",
            description="Run network bandwidth tests",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id)
    
    def run_iperf_test(self, server, port, cc, test_length, uplink=True):
        
        if uplink:
            print('Running iperf uplink test...')
        else:
            print('Running iperf downlink test...')

        if uplink:
            starttime, endtime, output = execute(
                "iperf3",
                "--json",
                c = server,
                p = port,
                C = cc,
                t = test_length
            )
        else:
            starttime, endtime, output = execute(
                "iperf3",
                "--json",
                "--reverse",
                c = server,
                p = port,
                C = cc,
                t = test_length
            )

        if uplink:
            raw_stdout_fname = "raw_stdout_uplink.log"
            test_meta_fname = "metadata_uplink.log"
        else:
            raw_stdout_fname = "raw_stdout_downlink.log"
            test_meta_fname = "metadata_downlink.log"

        self.write_raw_stdout(
            output, 
            self.artifact_path, 
            filename=raw_stdout_fname)

        leotest_output = {
            'TestName': self.name,
            'TestStartTime': starttime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
            'TestEndTime': endtime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
            'LeotestLocation': self._location,
            'LeotestConnectionType': self._connection_type,
            'LeotestNetworkType': self._network_type,
            'LeotestDeviceID': self._device_id,
        }

        metadata = os.path.join(self.artifact_path, test_meta_fname)
        logger.info('Writing metadata to {}'.format(metadata))
        with open(metadata, 'w', encoding='utf-8') as f:
            json.dump(leotest_output, f, ensure_ascii=False, indent=4)

        return leotest_output 


    def _start_test(self, artifact_name):
        logger.info("Starting iperf test...")
        if shutil.which("iperf3") is not None:
            #  # iperf3 -c localhost -p 5201 -C "cubic" -t 1000 --json
            test_length = self._config["tests"][self.name]["test_length"]
            server = self._config["tests"][self.name]["server"]
            port = self._config["tests"][self.name]["port"] 
            cc = self._config["tests"][self.name]["congesion_control"] 

            leotest_output_uplink = self.run_iperf_test(
                server,
                port,
                cc,
                test_length,
                uplink=True)

            leotest_output_downlink = self.run_iperf_test(
                server,
                port,
                cc,
                test_length,
                uplink=False)

            leotest_output = {
                'uplink': leotest_output_uplink,
                'downlink': leotest_output_downlink
            }
            return json.dumps(leotest_output)

        else:
            raise RunnerError(
                "iperf3",
                "Executable does not exist, please install iperf3.")