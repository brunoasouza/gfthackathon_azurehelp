# Hackathon GFT Canada - Azure Integration Tutorial

This repository is intended to help the hackathon teams with Azure integration. We are providing some functions that will make it easier to manipulate the data inside the notebooks.

## Getting starting

To setup this project it's necessary:
- To create a ressource group in Azure:

![Creating a resource group](assets/rg.png "Creating a resource group")

- Into this ressource group, it's necessary to create an azure machine learning service:

![Creating a machine learning service](assets/mlservice.png "Creating a machine learning service")

- In your workspace azure, you have access to a terminal with git support and there, you can clone your repository:

![Clonning the repository](assets/clone.png "Clonning the repository")

- To access the azure machine learning service in portal azure and download the config.json file:

![Download config.json file](assets/downloadconfigfile.png "Download config.json file")

- Put the config.json in baseproject/common/

![Put the config.json in baseproject/common/](assets/configfile.png "Put the config.json in baseproject/common/")

- To execute the read_data_from_blob function, it's necessary to add the connection string into the file config.json:
    1. In your ressource group, select the you store account
    2. Click in Access Keys
    3. Show keys
    4. Copy the connection string
    5. Open the config.json
    6. Create the key connection_string and paste your connection string value.

![Connection string](assets/connectstring.png "Connection string")

- Voilà!! You can continue others notebooks in the same level of the Testing_Template_Functions notebook

- If you prefer to use visual code, check this website: [link](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-setup-vs-code)


## Deployment and Registering a machine learning model

Before to register and deploy a machine learning models, it's necessary to register an experiment with your model. In our project, we are using MLflow to manage our experiments and models. 

To create an experiment you can use the **create_experiment_with_mlflow** function in the azuremlutils.py file

After creating the experiment, you need to perform a training of a machine learning model. In the code below you can find an example: 

```python

with mlflow.start_run() as run:
    try:
        # samples and labels
        X = df_data.iloc[:,7]
        y = df_data.iloc[:,8]

        # Applying LabelEncoder
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y)

        vectorizer = TfidfVectorizer(min_df = 2)

        X = vectorizer.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42) 
        print(X_train.shape, y_train.shape, X_test.shape, y_test.shape, sep = '\n')

        SVM_ = CalibratedClassifierCV(LinearSVC())

        SVM_.fit(X_train, y_train)

        pickle.dump(vectorizer, open('vectorizer.pkl',"wb"))

        pickle.dump(label_encoder, open('label_encoder.pkl',"wb"))
        # saving vectorizer
        mlflow.log_artifact("label_encoder.pkl", artifact_path="outputs/label_encoder/label_encoder.pkl")
        # saving vectorizer
        mlflow.log_artifact("vectorizer.pkl", artifact_path="outputs/vectorizer/vectorizer.pkl")
        # saving model
        mlflow.sklearn.log_model(SVM_, artifact_path="outputs")


        y_pred = SVM_.predict(X_test)

        cf_matrix = confusion_matrix(y_test, y_pred)
    
        metrics = classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True)
        
        mlflow.log_metric("accuracy", metrics["accuracy"])    
        mlflow.log_metrics({str(key1): float(value) for (key1, value) in metrics["Negative"].items()})
        mlflow.log_metrics({str(key1): float(value) for (key1, value) in metrics["Positive"].items()})
        mlflow.log_metrics({str(key1): float(value) for (key1, value) in metrics["Neutral"].items()})
        
        fig = plt.figure(1)
        image = ia_functions.plot_confusion_matrix(cf_matrix)
        fig.savefig("confusion_matrix.png")
        mlflow.log_artifact("confusion_matrix.png")
    except Exception as e:
        print('Experiment Failed:' + str(e))
        mlflow.end_run()

```

### Registering a machine learning model

To register a machine learning model, you can run the register_model method. This registered model can be viewed in the azure machine learning workspace.


**Important: Only register models that you are sure are functional.**

```python
result = mlflow_experiment.register_model(run_id, folder_path, model_name)
```


### Deployment 

To deploy your machine learning model you need to define the environment and the inference code. The environments can be created with Docker images, txt files with conda dependencies or manually as shown below:

```python
## Create env

import sklearn

from azureml.core.environment import Environment

environment = Environment("LocalDeploy")
environment.python.conda_dependencies.add_pip_package("inference-schema[numpy-support]")
environment.python.conda_dependencies.add_pip_package("joblib")
environment.python.conda_dependencies.add_pip_package("scikit-learn=={}".format(sklearn.__version__))
```

With inference code, the data scientist can customize the model output according to the needs of the project.

```python
# Inference code

from azureml.core.model import InferenceConfig

inference_config = InferenceConfig(entry_script="predict.py",
                                   environment=environment)

```
By providing the parameters with the model and the inference code it is possible to deploy the AI model in web service format. The time to perform the deployment is about 10 minutes.

```python
## Deploy 
from azureml.core.webservice import LocalWebservice
from azureml.core.model import Model

# This is optional, if not provided Docker will choose a random unused port.
deployment_config = LocalWebservice.deploy_configuration(port=6789)


local_service = Model.deploy(ws, "nlp-hackathon-model-2", [model], inference_config)

local_service.wait_for_deployment()
```


