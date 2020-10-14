#!/usr/bin/python3

import argparse
import requests
import json

service = 'https://api.anonfiles.com/upload'

# START argparse 

parser = argparse.ArgumentParser(
            description='Anonfile upload command line tool'
                                ) # Creating parser

parser.add_argument('-f',
                    action = 'store',
                    dest = 'file',
                    required = True,
                    help = 'file(s) for uploading'
                    ) # Catching file name

parser.add_argument('-l',
                    action = 'store_true',
                    default = False,
                    dest = 'logging',
                    required = False,
                    help = 'Log info into file'
                    ) # Log flag

args = parser.parse_args() # Parsing arguments to object

file = args.file # Setting file name to variable
logging = args.logging # Setting log bool to variable

# END argparse

# Request function
def post(filename):
    files = {'file': (filename, open(filename, 'rb'))}
    return requests.post(service, files=files).json()

# User output handler
def output(response, doLog):
    statusCode = bool(response['status'])

    if not statusCode:
        errorObj = response['error']
        return (f'The server returned an error: {errorObj["code"]} - {errorObj["message"]}')

    # START Log file
    if doLog:
        logFile = open('log.txt', 'w+')
        
        logContent = (
"""Filename: {}

Full URL: {}
Short URL: {}

ID: {}

Size: {}
""".format(
        response['data']['file']['metadata']['name'],
        response['data']['file']['url']['full'],
        response['data']['file']['url']['short'],
        response['data']['file']['metadata']['id'],
        response['data']['file']['metadata']['size']['readable'],
    ))

        logFile.write(logContent)
        logFile.close()
    # END Log file
    
    return response['data']['file']['url']['short']


print(output(post(file), logging))
