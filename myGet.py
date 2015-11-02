#!/usr/bin/python3
'''
Python Version of wget

Makes POST or GET requests to specified url and writes contents to a file.

Optionally can send custom POST data strings and custom user-agents.

Author: Hunter Gregal
'''
import argparse
import requests
import os.path
import sys
import re

#check for file
def checkFile(outFile):
    #if file already exists exit
    if os.path.exists(outFile) == True:
        print("Output file already exists! \nExiting...")
        sys.exit()

#check url
def checkUrl(url):
    #regex
    good = re.match("^(http|https)://", url)
    #if no match exit with error
    if not good:
        print("URL must begin with http:// or https:// ! \nExiting...")
        sys.exit()

#define GET function
def get(url, agent, outFile):
    print('Making GET request to:', url, 'with user agent:', agent)
    #make request
    r = requests.get(url, headers={'user-agent': agent}, verify=False)
    #exit on bad response
    if r.status_code != 200:
        print("Error, URL returned", r.status_code, "\nExiting...")
        sys.exit()
    #else write contents to file
    else:
        print('Request succesful. \nWriting response to output file...')
        f = open(outFile, 'wb')
        f.write(r.content)
        f.close()

#define POST function
def post(url, agent, outFile, data):
    #if POST data prepare the request with it
    if data:
        print('Making POST request to:', url, 'with user agent:', agent, 'and data:', data)
        data = dict(item.split("=") for item in data.split("&"))
        r = requests.post(url, headers={'user-agent': agent}, data=data, verify=False)
    #else if no POST data, make request without it
    else:
        print('Making POST request to:', url, 'with user agent:', agent)
        r = requests.post(url, headers={'user-agent': agent}, verify=False)
    #exit on bad response
    if r.status_code != 200:
        print("Error, URL returned", r.status_code, "\nExiting...")
        sys.exit()
    #else write contents to file
    else:
        print('Request succesful. \nWriting response to output file...')
        f = open(outFile, 'wb')
        f.write(r.content)
        f.close()

if __name__ == '__main__':

    '''ARGUMENTS'''
    #init parser with description
    parser = argparse.ArgumentParser(description="Grabs a webpage!")
    ##add arguments
    #output file
    parser.add_argument('-f', '--file', dest='outFile', help='Specify an output file', required=True)
    #url
    parser.add_argument('-u', '--url', dest='url', help='Specify URL to get', required=True)
    #user-agent
    parser.add_argument('-a', '--agent', dest='agent', help='Specify a user agent to use', default="myGet 0.0.1a; NET320-20151014")
    #Method
    parser.add_argument('-m', '--method', dest='method', help='Specify a HTTP method to use [default GET]', choices=["GET", "POST"], default="GET")
    #data
    parser.add_argument('-d', '--data', dest='data', help='Specify POST data to send', default=None)
    #parse args
    args = parser.parse_args()

    '''PRIMARY PROGRAM'''
    #Check if file already exists
    checkFile(args.outFile)
    #Check that user added http(s):// to the url
    checkUrl(args.url)
    #If method is GET...
    if args.method == "GET":
        get(args.url, args.agent, args.outFile)
    #If method is POST
    elif args.method == "POST":
        post(args.url, args.agent, args.outFile, args.data)
    #Woot! We did it with no errors!
    print('Complete! \nResponse written to', args.outFile)
