import boto3
from io import StringIO
import zipfile
import io
import mimetypes

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
