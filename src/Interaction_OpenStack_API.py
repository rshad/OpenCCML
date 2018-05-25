from openstack import connection # used to establish a connection to openstack $
import json # used to pretty print a json output
import base64 # used to encode strings, to be passed as user data files when creating servers


def js_read(filename):
   """
   js_read, reads a json file

   :param filename: the json file name to be read
   :return: a json object
   """
   with open(filename) as f_in:
       return(json.load(f_in))

def get_json_object(object):
    """
    get_json_object, used to convert an non json data to a json object

    :param object: it can any compute element in our case, like sever, network ....
    :return: json_object, the final json object

    """
    # convert object to dictionary.
    object_dict = object.to_dict()

    # Serialize ``object`` to a JSON formatted ``str``.
    object_json_serialized = json.dumps(object_dict, indent=4, sort_keys=True)

    # load object_json_serialized as json object.
    json_object = json.loads(object_json_serialized)

    return json_object

def get_server_field(compute,servar_name,field):
    """
    get_server_id, used to get the field value of a server, known its name

    :param servar_name: the name of the server to get its id
    :param field: the field value to be returned
    :return: server_field, is the value of the field, field of the server, server_name
    """

    # Finding a server by its name, using find_server(server name or ID) function.
    server = (compute.find_server(servar_name))

    # convert server to a json object
    server_json_object = get_json_object(server)

    # get the server field, field
    server_field = server_json_object[field]

    return server_field


def create_server(conn,instance_name,image_name,flavor_name,network_name,keypair_name,key_file_path,user_data_file):
    """
    create_server, is a function used to create a new instance or virtual server in our platform

    :param conn: the connection object, which represents the port to many elements of the api, in this case is compute
    :param image_name: the image of the instance " The operative system " .. Ubuntu, Fedora, ....
    :param flavor_name: a flavor defines the compute, memory, and storage capacity of a virtual server, also known as an instance.
    :param network_name: the network name
    :param keypair_name: the keypair name to establish the authority
    :param key_file_path: the path of the key keypair_name
    :param user_data_file: the user-data file. must be Base64 encoded.

    """
    print("Creating a Server:")

    """ getting the image object, which corresponds to image_name """
    image = conn.compute.find_image(image_name) # Example: Fedora27

    """ getting the flavor object, which corresponds to the flavor_name """
    flavor = conn.compute.find_flavor(flavor_name) # Example: m1.high

    """ getting the network object, which corresponds to network_name """
    network = conn.network.find_network(network_name) # Example: provider

    """ getting the keypair object, which corresponds to keypair_name """
    keypair = conn.compute.get_keypair(keypair_name) # Example: key-one


    """ Once we get our required parameters prepared, we can proceed to create the new instance """
    server = conn.compute.create_server(
        name=instance_name,
        image_id=image.id,
        flavor_id=flavor.id,
        networks=[{"uuid": network.id}],
        key_name=keypair.name,
        # adresses=[{"public":{'version':4,'addr':'192.168.0.92'}}],
        user_data=json.dumps(user_data_file.decode("utf-8"))
    )

    """ wait till the server finish of creating the instance """
    server = conn.compute.wait_for_server(server)

    """ establishing the connection to our main instance """
    print("ssh -i {key} root@{ip}".format(key=key_file_path,
                                          ip=server.access_ipv4))




#def delete_server():



# main
if __name__ == "__main__":
    """
    the json file where the authentication arguments are stored.
    ------------------------------------------------------------
    
    this file contains the following data:
    {
        "auth_url": "***",
        "project_name": "***",
        "project_id": "***",
        "username": "***",
        "password": "***",
        "user_domain_id": "***"
    }
    
    * fill the stars with your data 
    
    """
    auth_args_file_path = "../data/authentication-files/auth_arguments.json"

    # an dictionary used to store the read authentication arguments
    auth_args = js_read(auth_args_file_path)

    # establish a connection top Openstack, using auth_args as authentication set of arguments
    conn = connection.Connection(**auth_args)

    # Compute object
    compute = conn.compute

    # get the id of master-instance server
    #print(get_server_field(compute,'master-instance','id'))

    # get the floating ip of the master
    # print((get_json_object(compute.get_server(get_server_field(compute,'master-instance','id')))))#['addresses'])#['provider'][0]['addr'])

    # An example to create a user-data file
    basic_cloud_init = "#!/bin/sh\n"
    basic_cloud_init = basic_cloud_init + "yum update\n" \
                                          "sudo yum install httpd\n" \
                                          "sudo service httpd start\n"

    # an user-data object must be Base64 encoded.
    b64str = base64.b64encode(basic_cloud_init.encode())


    # calling create_server to create a one ...
    create_server(conn,
                  instance_name="slave_instance_2",
                  image_name="Fedora27",
                  flavor_name="m1.high",
                  network_name="provider",
                  keypair_name="key-one",
                  key_file_path="../data/key-files/key-one.pem",
                  user_data_file=b64str
                 )
