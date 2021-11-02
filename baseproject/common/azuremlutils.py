import azureml.core
from azureml.core import Workspace, Dataset, Datastore
from azureml.core.experiment import Experiment
from azure.storage.blob import BlobServiceClient
from azure.storage.blob.aio import BlobClient
import logging
import pandas as pd
import json
import os
import pathlib


class AzureMlUtils:

    """ Init constuctor to read the config file with the credentials"""
    def __init__(self):
        self.ws = Workspace.from_config()

        directory = pathlib.Path(__file__).parent.resolve()
        with open(str(directory) + '/config.json') as f:
            self.config = json.load(f)

    """ Create experiment on azure machine learning

        :param str  experiment_name: experiment name

        :return Experiment: experiment object with all information
    """
    def create_experiment(self, experiment_name: str):
        try:
            experiment = Experiment(self.ws, experiment_name)
            return experiment
        except Exception as e:
            logging.exception(e)

    """ Get experiment on azure machine learning

        :param str  experiment_name: experiment name

        :return link to access the experiment
    """
    def get_experiment(self, experiment_name: str):
        try:
            return self.ws.experiments[experiment_name]
        except Exception as e:
            logging.exception('Exception get_experiment: ')

    
    """ Read file dataset from Azure datastore 

        :param str  dataset_name: dataset name
        :param str  path: path to save the file
        :param bool overwrite_file: overwrite the local file
        :param int  dataset_version: dataset version

        :return file object to read the file 
    """
    def read_file_dataset_from_azure(self, dataset_name: str, path:str ='.', overwrite_file: bool=True, dataset_version:int = 1):
        try:
            dataset = Dataset.get_by_name(self.ws, name=dataset_name, version=dataset_version)
            return dataset.download(target_path='.', overwrite=overwrite_file)
        except Exception as e:
           logging.exception('Exception read_file_dataset_from_azure: ')
    
    """ Read tabular dataset from Azure datastore 

        :param str  dataset_name: dataset name
        :param int  dataset_version: dataset version

        :return pandas dataframe
    """
    def read_tabular_dataset_from_azure(self, dataset_name: str, dataset_version:int = 1):
        try:
            dataset = Dataset.get_by_name(self.ws, name=dataset_name, version=dataset_version)
            return dataset.to_pandas_dataframe()
        except Exception as e:
            logging.exception('Exception read_tabular_dataset_from_azure:')
    
    """ Save pandas dataframe in Azure datastore 

        :param str  dataset_name: dataset name
        :param int  dataset_version: dataset version

        :return pandas dataframe
    """
    def save_pandas_dataframe_in_azure_datastore(self, store_name:str, file_name:str, pandas_dataframe: pd.core.frame.DataFrame, show_progress_console:bool = True):
        try:
            datastore = Datastore.get(self.ws, store_name)
            return Dataset.Tabular.register_pandas_dataframe(pandas_dataframe, datastore, file_name, show_progress=show_progress_console)
        except Exception as e:
            logging.exception('Exception save_pandas_dataframe_in_azure_datastore:')

    """ Read data from blob
        :param str  container_name: container name
        :param int  blob_name: blob name

        :return byte
    """
    async def read_data_from_blob(self, container_name:str, blob_name:str):
        connection_string = self.config['connection_string']

        blob = BlobClient.from_connection_string(connection_string, container_name, blob_name)

        stream = await blob.download_blob()
        data = await stream.readall()

        return data

