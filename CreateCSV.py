#!/usr/bin/env python3
import argparse;
import configparser;
import operators.WILPSubmissions;
import operators.factory;

config = configparser.ConfigParser();
config.read('config.cfg');

argParser = argparse.ArgumentParser(description="Imports data from external source.");
argParser.add_argument('-c', "--config", help="Configuration key to be used", required=True);
argParser.add_argument('-o', "--output", help="Fully qualified output location. Timestamped files. Ex. [now].csv will generate file with current timestamp.", required=False);
argParser.add_argument('-f', "--file", help="Starts from relative path instead of downloading file. Timestamped files. Ex. [now].csv will generate file with current timestamp")

args = argParser.parse_args();

print (args);
# print (config.sections());
configuration = dict(config.items('WILPRegistration'));


def _processFileName(key):
    import time;
    internal = key.lower();
    if(internal.find('[now]', 0) > -1):
        return internal.replace('[now]', time.strftime("%Y%m%d-%H%M%S"));

    return key;



if(args.output):
    configuration["output"] = _processFileName(args.output);

if(args.file):
    configuration["file"] = _processFileName(args.file);

#print(configuration);

if __name__ == "__main__":
    worker = operators.Factory.getObject("WILPSubmissions", configuration);
    print(worker.getData());
else:
    print("Not designed for this!");
