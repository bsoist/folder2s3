folder2s3.py
============
A Python script for uploading a folder to an S3 bucket.
Created by Bill Soistmann on 2014-02-27.

Requires boto and a properly formated boto.cfg file.

Import Examples
---------------

    import folder2s3

then ...

    folder2s3.upload(mystuff)
    folder2s3.upload(path/to/mystuff)
    folder2s3.upload(/absolute/path/to/mystuff)

All of the above will find the folder in question ( if it exists ) and upload it to a bucket named mystuff in your default profile.

    folder2s3.upload(/absolute/path/to/mystuff, profile="aprofile", bucket="abucket")

Uploads folder to a bucket named abucket in profile aprofile.


Command Line Examples
---------------------
    ./folder2s3.py mystuff
    ./folder2s3.py path/to/mystuff
    ./folder2s3.py /absolute/path/to/mystuff

All of the above will find the folder in question ( if it exists ) and upload it to a bucket named mystuff in your default profile.

    ./folder2s3.py --profile=aprofile --bucket=abucket /absolute/path/to/mystuff 
    ./folder2s3.py --paprofile --babucket /absolute/path/to/mystuff

Uploads folder to a bucket named abucket in profile aprofile.

Other Options
-------------
Local files with a modified time more recent than the S3 files will be uploaded to replace S3 files. Use replaceAll=True ( -r or --replaceAll from the command line ) to copy regardless of mtime.

In my experience, boto does a good job with the content-type, but this script does set any file without an extension to a default_content_type which is "text/html" by defult. Use keyword argument default_content_type="foo/bar" ( -cfoo/bar or --default_content_type=foo/bar from the command line ) to specify a default.

Boto Configuration
------------------
This script used the boto module and assumes a configuration file. See boto
documentation for more infromation.

Example /etc/boto.cfg
----------------------
[aprofile]
aws_access_key_id = ACCESS_KEY
aws_secret_access_key = SECRET_KEY


[Credentials]
aws_access_key_id = ACCESS_KEY
aws_secret_access_key = SECRET_KEY




