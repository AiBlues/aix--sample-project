# Sample AI Explainability Project

... works with Maquette MLFlow Stack

## Install dependencies

We use Poetry for dependency management, however it is best practice to create a basic conda environment before:

```
conda create -p ./env python=3.8
conda activate ./env
poetry install -vvv
```

## Setup and run MlFlow

```bash
$ export MLFLOW_TRACKING_URI=http://localhost:5000 && \
    export AWS_ACCESS_KEY_ID=access && \
    export AWS_SECRET_ACCESS_KEY=secret1234 && \
    export AWS_DEFAULT_REGION=mzg && \
    export MLFLOW_S3_ENDPOINT_URL=http://localhost:9000

$ mlflow run .
```

Or with Maquette ...

```bash
$ mq project activate ${PROJECT_NAME}
$ mlflow run .
```

Make sure that Maquette Configuration is placed at `~/.mq/config.yaml`. Sample file is located here `.mq.config.yaml`.
