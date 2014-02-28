#!/usr/bin/env python
"""
folder2s3.py

Created by Bill Soistmann on 2014-02-27.

Requires boto and a properly formated boto.cfg file.
See README.md for more information.

Import Examples: ( using import folder2s3 )

    folder2s3.upload(mystuff)
    folder2s3.upload(path/to/mystuff)
    folder2s3.upload(/absolute/path/to/mystuff)

    All of the above will find the folder in question ( if it exists ) and upload it
    to a bucket named mystuff in your default profile.

    folder2s3.upload(/absolute/path/to/mystuff, profile="aprofile", bucket="abucket")

    Uploads folder mystuff to a bucket named abucket in profile aprofile.

    Local files with a modified time more recent than the S3 files will be uploaded
    to replace S3 files. Use replaceAll=True to copy regardless of mtime.

    In my experience, boto does a good job with the content-type, but this script
    does set any file without an extension to a default_content_type which is
    "text/html" by defult. Use keyword argument default_content_type="foo/bar" to
    specify a default.

Command Line Example

    ./folder2s3.py mystuff
    ./folder2s3.py path/to/mystuff
    ./folder2s3.py /absolute/path/to/mystuff

    All of the above will find the folder in question ( if it exists ) and upload it
    to a bucket named mystuff in your default profile.

    ./folder2s3.py --profile=aprofile --bucket=abucket /absolute/path/to/mystuff
    ./folder2s3.py --paprofile --babucket /absolute/path/to/mystuff

    Uploads folder to a bucket named abucket in profile aprofile.

    Local files with a modified time more recent than the S3 files will be uploaded
    to replace S3 files. Use -r or --replaceAll to copy regardless of mtime.

    In my experience, boto does a good job with the content-type, but this script
    does set any file without an extension to a default_content_type which is
    "text/html" by defult. Use -cfoo/bar or --default_content_type=foo/bar to
    specify a default.


"""

import os, sys, getopt
import time, datetime
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

DEBUG = None

replaceAll = False

def getConn(section='Credentials'):
    boto_config = boto.Config()
    return S3Connection(
            boto_config.get(section,'aws_access_key_id'),
            boto_config.get(section,'aws_secret_access_key')
    )

def getBucket(bucketname, profile="Credentials", connection=None):
    conn = connection or getConn(profile)
    return conn.get_bucket(bucketname)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def upload(folder, profile=None, bucket=None, default_content_type=None, replaceAll=False):
    args = []
    if profile: args.append("-p%s" % profile)
    if bucket: args.append("-b%s" % bucket)
    if default_content_type: args.append("-c%s" % default_content_type)
    if replaceAll: args.append("-r")
    args.append(folder)
    main(args)



def main(argv=None):
    global DEBUG
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hp:b:c:r", ["help", "profile=", "bucket=", "default_content_type=", "replaceAll"])
        except getopt.error, msg:
             raise Usage(msg)
        profile, bucket, content_type = None, None, None
        for option, value in opts:
            if option in ("-h", "--help"):
                print __doc__
                sys.exit()
            if option in ("-p", "--profile"):
                profile = value
            if option in ("-b", "--bucket"):
                bucket = value
            if option in ("-c", "--default_content_type"):
                default_content_type = value
            if option in ("-r", "--replaceAll"):
                replaceAll = True
        try:
            folder_name = args[0]
        except:
            raise Usage("Missing argument - folder to copy is required")
        bucket_name = bucket or os.path.basename(folder_name)
        profile_name = profile or "Credentials"
        default_content_type = content_type or "text/html"
        bucket = getBucket(bucket_name, profile_name)
        s3files= bucket.list()
        common_prefix = os.path.commonprefix([folder_name])
        localfileset = [os.path.relpath(os.path.join(dp, f),common_prefix) for dp, dn, filenames in os.walk(common_prefix) for f in filenames]
        for s3file in s3files:
            keyname = s3file.key
            filename = os.path.join(common_prefix,keyname)
            s3mod = boto.utils.parse_ts(s3file.last_modified)
            try:
                localmtime = os.stat(filename).st_mtime
            except OSError:
                print "local file", filename, "not found"
                continue
            localmod = datetime.datetime.utcfromtimestamp(localmtime)
            if replaceAll or localmod > s3mod:
                replacename = os.path.join(bucket_name,keyname)
                print "replacing", replacename
                s3file.set_contents_from_filename(filename)
                s3file.set_acl("public-read")
                try:
                    ext = s3file.name.split('/')[1].split('.')[1]
                except:
                    s3file.copy(bucket, s3file.name, preserve_acl=True, metadata={'Content-Type': default_content_type})
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())




