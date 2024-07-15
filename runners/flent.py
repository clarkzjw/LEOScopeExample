import logging
import shutil
import json
import os

from textwrap import dedent

from leotest.errors import RunnerError
from leotest.runner import LeotestRunner
from leotest.utils import execute

logger = logging.getLogger(__name__)

class FlentClient(LeotestRunner):
    """Run Flent tests."""

    def __init__(self, testname, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            name = testname, 
            title="Flent",
            description="Flent: The FLExible Network Tester",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id)
        
    def _start_test(self, artifact_name):
        logger.info("Starting flent test...")
        if shutil.which("flent") is not None:

            type = self._config["tests"][self.name]["type"]
            test_length = self._config["tests"][self.name]["test_length"]
            server = self._config["tests"][self.name]["server"]
            control_port = self._config["tests"][self.name]["control_port"]
            plot_text = self._config["tests"][self.name]["plot_text"]
            plot_type = self._config["tests"][self.name]["plot_type"]
            output_filename = self._config["tests"][self.name]["output_filename"]
            
            data_path_list = [
                self._config["artifacts"]["path_local"], 
                self.name,
                artifact_name
            ]

            data_dir = os.path.join(*data_path_list)
            output_filename = os.path.join(
                data_dir, 
                self._config["tests"][self.name]["output_filename"])

            starttime, endtime, output = execute("flent", type,
                                            p=plot_type,
                                            l=str(test_length),
                                            H=server,
                                            t=plot_text,
                                            o=output_filename,
                                            D=data_dir)
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
                "flent",
                "Executable does not exist, please install flent.")