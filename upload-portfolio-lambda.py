import boto3
from io import StringIO
import zipfile
import io
import mimetypes



def lambda_handler(event, context):

    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:818612457280:deployPortfolioTopic')

    try:
        s3 = boto3.resource('s3')

        portfolio_bucket = s3.Bucket('potfolio.static.info')
        build_bucket = s3.Bucket('portfoliobuild.test.info')

        portfolio_zip = io.BytesIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for name in myzip.namelist():
                obj = myzip.open(name)
                portfolio_bucket.upload_fileobj(obj, name)
                ExtraArgs={'ContentType': mimetypes.guess_type(name)[0]}
                portfolio_bucket.Object(name).Acl().put(ACL='public-read')


        topic.publish(Subject="Deploy Portfolio", Message="Portfolio Deployed Successfully")
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="The Portfolio was not Deployed Successfully")
        raise
