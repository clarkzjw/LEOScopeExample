# LEOScope Example

Example Docker image for [LEOScope](https://leoscope.surrey.ac.uk/) experiments.

## Build

See the [Dockerfile](./Dockerfile) and [build.sh](./build.sh) for the build instructions.

## Usage

See [experiment-config.yaml](./example/experiment-config.yaml) for an example experiment configuration.

```bash
docker: 
  image: 'clarkzjw/leoscope_example:latest'
  deploy: 
  execute:
    name: "leo-measurement"
  finish:
cloud_config:
  # set up an azure storage account https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal
  # create a container in the storage account 
  # get the storage account key: https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal
  # example: DefaultEndpointsProtocol=https;AccountName=...;AccountKey=.....
  connection_string: <azure_connection_string>
  # storage container name
  container: <container_name_on_azure_storage>
  weather_apikey: <not_used>

tests:
  shell-1:
    entry_point: "ShellClient"
    runner: "shell"
    # url to a shell script
    url: "https://gist.githubusercontent.com/clarkzjw/eec52cd2612fc7d38409b5c8e7c4c6cf/raw/ec46f17237c35ce90043b6031fa02d51f5c03cd6/run.sh"

artifacts:
  path_local: "/artifacts"

```