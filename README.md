# los angeles

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

This is your new Kedro project, which was generated using `kedro 0.19.12`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## 🔑 Kaggle API Token Setup

To download the dataset:

1. Visit https://www.kaggle.com/account
2. Scroll to "API" section and click "Create New Token"
3. Place the downloaded `kaggle.json` file in the `.kaggle/` directory at the root of the project
4. Make sure permissions are secure (optional but recommended):
    ```bash
   chmod 600 .kaggle/kaggle.json
    ```
   
## Install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## Download dataset with script
Run the following command from the root of the project directory:
```
python scripts/download_data.py
```

## How to run your Kedro pipeline
Move to the root of your Kedro project directory:
```
cd kedro
```
And run the project with:

```
kedro run
```

## How to run the FastAPI server
Move to the root of your backend project directory:
```
cd backend
```
And run the FastAPI server with:

```
uvicorn main:app --reload
```

## Swagger UI
To access the Swagger UI for your FastAPI application, open your web browser and navigate to:

```
http://127.0.0.1:8000/docs
```

## To update the project dependencies
To update the project dependencies, you can use `pip-tools` to manage your requirements. First, install `pip-tools`:

```
pip install pip-tools
```

Then, you can update the file `requirements.in` with your project dependencies. 
This file should contain the top-level dependencies you want to include in your project, for example:

```text
kedro
kedro-datasets[pickle]
pandas
scikit-learn
streamlit
fastapi
matplotlib
uvicorn[standard]
kaggle
```

Then, you can update your `requirements.txt` file by running:

```
pip-compile requirements.in
```


## How to test your Kedro project

Have a look at the files `src/tests/test_run.py` and `src/tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:

```
pytest
```

To configure the coverage threshold, look at the `.coveragerc` file.


[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can use tools like [`nbstripout`](https://github.com/kynan/nbstripout). For example, you can add a hook in `.git/config` with `nbstripout --install`. This will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html)
