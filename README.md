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
