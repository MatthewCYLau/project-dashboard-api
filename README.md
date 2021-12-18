# Python Flask GCP Cloud Run

A reference project to deploy a Python Flask app onto GCP Cloud Run

![cicd cloud run workflow](https://github.com/MatthewCYLau/python-flask-gcp/actions/workflows/cicd-cloud-run.yml/badge.svg)

An app which track skills used in various projects

## Pre-requisite

- Make sure you have installed Python 3, and [pip](https://pip.pypa.io/en/stable/installing/)

```bash
python3 --version # prints Python 3 version
pip3 --version # prints pip version
```

## Run app locally

```bash
virtualenv -p /usr/bin/python3 venv # create new virtual environment venv
source venv/bin/activate # activate venv
pip3 install -r requirements.txt # installs python packages
python3 manage.py # visit app at http://localhost:8080/ping
deactivate # deactivates venv
```

### Install new packages

```bash
pip3 install boto # installs new Python package
pip3 freeze > requirements.txt # updates requirements.txt
```

## Build

```bash
gcloud builds submit --tag gcr.io/<PROJECT-ID>/python-flask-gcp
```

## Deploy

- Create two secrets on [Secrets Manager](https://cloud.google.com/secret-manager) named `jwt-secret`, and `mongo-db-connection-string`

- Deploy to Cloud Run by running:

```bash
gcloud run deploy --image gcr.io/<PROJECT-ID>/python-flask-gcp --platform managed
```

- Allow Cloud Run service access to the secrets as secret environment variables. See GCP Cloud Run documentation [here](https://cloud.google.com/run/docs/configuring/secrets#mounting-secrets)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate

If you find this project helpful, please give a :star: or even better buy me a coffee :coffee: :point_down: because I'm a caffeine addict :sweat_smile:

<a href="https://www.buymeacoffee.com/matlau" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## License

[MIT](https://choosealicense.com/licenses/mit/)
