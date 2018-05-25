#!/usr/bin/env python3.6
""" 
HandleClusterData.py, is a python script, used to store the related data of a determined cluster.
    * This script is dedicated to design the corresponding functions to, which gonna be used to store the 
      related data of a cluster into json file (array of arrays), where each cluster gonna be represented
      by one of these arrays.
"""

__author__ = "Rshad Zhran"
__authors__ = ["Rshad Zhran", "Manuel Parra"]
__contact__ = "rashzk95gmail.com"
__email__ =  "rashzk95gmail.com"
__credits__ = ["Rshad Zhran", "Manuel Parra"]
__date__ = "2018/02/01"
__deprecated__ = False
__maintainer__ = "Rshad Zhran"
__status__ = "Production"
__version__ = "0.2"

#__license__ = ""
#__copyright__ = "Copyright 2018, University of Granada"

import json # used to operate with JSON, write or read from/to json files

# the corresponding json file
clustersFile = "C:\\Users\\rashz\\PycharmProjects\\Openstack-Virtualization\\src\\clusters.json"

def storeData(args,data_filename=clustersFile):
    """
    storeData, is used to store the related data of each cluster
    ------------------------------------------------------------

    :parameter: args, contains all the related fields related to the cluster
    :parameter: data_filename, the file to which we want add a new entry
    """

    # open the json file, in reading mode, to read it's content -> the content of the array
    with open(data_filename, mode='r', encoding='utf-8') as clustersjson:
        clusters_array = json.load(clustersjson)

    # open the json file, in writing mode, to store the new entry
    with open(data_filename, mode='w', encoding='utf-8') as clustersjson:
        # The new entry
        """
        The file structure:
        ------------------
        * We have a dictionary which contains a key called "clusters". This key has as a value, a dict-
          ionary of key:value, where each key:value corresponds to <cluster name>:entry.
        
        * Each entry is a dictionary where the key represents a cluster characteristic, and the value represe-
          nts the value, which correponds to each charactersitics.  

        ¿ Why we use a dictionary to store each cluster and its entry ?
        -----------------------------------------------------------------
        * That's to be more efficient when we want to recover or delete an cluster, so the orden of
          complexity is constant, O(1).
        """
        entry = {  
                    'cluster_name': args["name"],
                    'slaves_number': args["numslaves"],
                    'masters_number': args["nummasters"],
                    'flavor': args["flavor"],
                    'internal_network': args["internal_network"],
                    'external_network': args["external_network"],
                    'security_group': args["security"],
                    'image': args["image"],
                    "slaves":
                    [
                        { 
                            "slave_name": slave["slave_name"],
                            "slave_internal_IP":slave["slave_ip"]

                        # iterating over the list of dictionaries, where each dictionary corresponds to a slave instance           
                        }for slave in args["slaves"]
                    ],
                    "masters":
                    [
                        { 
                            "master_name": master["master_name"],
                            "master_IP":master["master_ip"]

                        # iterating over the list of dictionaries, where each dictionary corresponds to a slave instance           
                        }for master in args["masters"]
                    ]
                }
            
        # Adding the new entry to the array recovered from the corresponding json file
        clusters_array["clusters"][args["name"]] = entry
        # Writing the array to the file
        json.dump(clusters_array, clustersjson,indent=4)
        # Adding a new line after each entry
        clustersjson.write('\n')

def checkCluster(cluster_name,data_filename=clustersFile):
    """
    checkCluster, is used to get the data related to the cluster <cluster_name>
    ---------------------------------------------------------------------------

    :param cluster_name, represents the name of the cluster, to recover its related info.
    :param data_filename, the file from which we recover our information
    :return the related data of <cluster_name>
    """
    
    # open the json file, in reading mode, to read it's content -> the content of the array
    with open(data_filename, mode='r', encoding='utf-8') as clustersjson:
        clusters_array = json.load(clustersjson)
    
    # return the related data of <cluster_name>
    return clusters_array["clusters"][str(cluster_name)]


def deleteCluster(cluster_name,data_filename=clustersFile):
    """
    deleteCluster, used to delete the entry, related to the cluster <cluster_name> from the file <data_filename>
    ------------------------------------------------------------------------------------------------------------

    :param cluster_name, represents the name of the cluster, to be deleted from the file <data_filename>
    :param data_filename, the file from which we want to delete the entry of the cluster <cluster_name>
    """

    # open the json file, in reading mode, to read it's content -> the content of the array
    with open(data_filename, mode='r', encoding='utf-8') as clustersjson:
        clusters_array = json.load(clustersjson)
    
    # delete the corresponding entry for the ker <cluster_name>
    del clusters_array["clusters"][str(cluster_name)]
    
     
def cleanFile(data_filename=clustersFile):
    """
    cleanFile, clean the corresponding file, so it overwrites it and assign an empty array.
    --------------------------------------------------------------------------------------

    :param data_filename, the file to be overwritten
    """
    with open(data_filename, mode='w', encoding='utf-8') as f:
        json.dump({"clusters":{}}, f)


if __name__ == "__main__":
    # example of an entry
    args = {
        'name': "cluster_2",
        'numslaves': 2,
        'nummasters': 1,
        'flavor': "flavor_1",
        'internal_network': "rshad_network",
        'external_network': "external",
        'security': "default",
        'image': "CentOS7",
        "slaves": [
                    { 
                        "slave_name": "instance_1",
                        "slave_ip":"0.0.0.0"
                    },
                    { 
                        "slave_name": "instance_2",
                        "slave_ip":"1.1.1.1"
                   }
        ],
        "masters": [
                    { 
                        "master_name": "instance_1",
                        "master_ip":"0.0.0.0"
                    },
                    { 
                        "master_name": "instance_2",
                        "master_ip":"1.1.1.1"
                   }
        ]
    }
    
    
    
    # In case of treating an empty file, we have to initialize it with an empty array
    #cleanFile(clustersFile)
    
    # Call storeData to add the new entry to corresponding file
    storeData(args,clustersFile)
    
    # Example of how to check a determined cluster
    print(str(checkCluster("cluster_1",clustersFile)))
