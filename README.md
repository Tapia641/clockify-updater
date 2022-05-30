# clockify-updater

Share your daily hours with your team and your project manager

# Introduction

Well, Clockify is a timer to estimate your current hours working, but sometimes is not possible to load your hours
because you are working or you are busy all day, but that is not a reason to don't upload your hours, that is the reason
for this script, only you need to execute lo load hours similar to past weeks or modify to load your right hours.

# How to install

```
 python3 -m venv venv
 source /venv/bin/activate
 pip install -r requirements.txt
```

Configure the `config.yaml`

```
API_KEY:
ENDPOINT: https://api.clockify.me/api/v1
```

# How to use it

To generate one template example you can use the following command, and You will see one XLSX in **tmp/files/**:

`python3 main.py --generate_example`

# See detail information
