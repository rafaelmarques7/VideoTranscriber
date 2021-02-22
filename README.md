# Video Transcriber

The goal of this project is to create a simple website that allows you to:
  * input a youtube link
  * output the video caption/transcription
  * (extra) create summary of the text

## Proposed approach

* Use [pytube](https://github.com/pytube/pytube) to extract the relevant information of the video
* Extract (and process, if necessary) the caption, if available 
* If caption is not available, download video and use some speech-to-text service to extract the text
* (extra) use a summary API to create a summary of the text

## Proposed architecture

* Use AWS lambda functions and API Gateway to power the API
* Use React to build a simple frontend
* Use AWS S3 and Cloudformation to create a static hosted and distribute it

## Issues

* Youtube captions don't have ponctuation
    * can we use an API to solve this issue? Example https://github.com/ottokart/punctuator2
    
## Useful links

* CDK setup was powered by https://github.com/aws-samples/aws-cdk-examples

## Adding dependencies 

In order to support third-party libraries in Python, with packaging and deployments handled by CDK, 
there are some manual steps required.
* The end-goal is to add a `package.zip` file, with the third-party source code, into the `layers` folder.
* This package can then be added as a lambda layer, using CDK, f.e.: 
    ```python
    requests_layer = _lambda.LayerVersion(
        self, 
        "pytube",
        code=_lambda.AssetCode('layers/pytube.zip')
    )
    ``` 
* This layer can then be used by the lambda function, f.e.:
    ```python
    base_lambda = _lambda.Function(
        self, 
        APP_NAME,
        layers=[requests_layer],
    )
    ```
    
To create a `package.zip` file for a particular dependency, follow the following steps:
  * create a `temp` folder and move into it, `mkdir temp && cd temp`
  * install a desired third-party library, and unpack it in the folder, under a `python` subfolder 
  (note: it is very important that it is under a python subfolder): `pip install requests -t ./python`
  * zip the folder `zip -r ./requests.zip .`
  * now move the zipped folder into the layers directory, and delete the temp directory altogether
  * voilá