# appetize-utils

This repo contains utilities used for the project appetize.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need the following to run this project:
- python 3
- pip resources installed
- env.py file containing an api key string (place-scrapper)
- env.json file containing api private key (translator)

### Installing

A step by step series of examples that tell you how to get a development env running

1. Install python requirements.

```
pip install -r requirements.txt
```

2. Get access to the env.py file from this repos maintainer and place it in `<pathToDir>/appetize-utils/place-scrapper`. Alternately you can create your own env.js and use your own api key. Note that this requires you to setup your own Google Cloud project with the 'Places API' enabled, see [here](https://developers.google.com/places/web-service/intro) to get started. The env.py has the following expected format:

```
def apiKey():
    return("<YOUR-API-KEY>")
```

3. Get access to the env.json file from this repos maintainer and place it in `<pathToDir>/appetize-utils/translator`. Alternately you can create your own env.json and use your own private key. Note that this requires you to setup your own Google Cloud project with the 'Cloud Translation API' enabled, see [here](https://cloud.google.com/translate/docs/quickstarts) to get started. Follow the steps [here](https://cloud.google.com/translate/docs/basic/setup-basic) to get the private key as a json, rename this file to env.json place in project as described above.

### Running place-scrapper

In the folder '<pathToDir>/appetize-utils/place-scrapper' run the command:

`python main.py`

This util will fetch place data from the 'Places API' as an object. Stored images from Google will also be scrapped for each unique place fetched. There are a few configurations variables you can edit within the code for this process, see main.py for more info.

### Running translator

In the folder '<pathToDir>/appetize-utils/place-scrapper' run the command:
  
`python main.py`

This util will run through the translation demo using Google Translation API.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
