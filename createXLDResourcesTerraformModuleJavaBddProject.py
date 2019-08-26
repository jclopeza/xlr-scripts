# Este script se invoca de forma remota desde el template de creación de infraestructuras con Terraform en AWS
# La invocación se debe realizar de la siguiente forma:
# ./bin/cli.sh -username admin -password ***** -f prueba.py dev calculator eu-west-3 t2.small ~/.ssh/id_rsa ~/.ssh/id_rsa.pub

import sys
environment = sys.argv[1]
projectName = sys.argv[2]
awsRegion = sys.argv[3]
instanceType = sys.argv[4]
privateKeyPath = sys.argv[5]
publicKeyPath = sys.argv[6]

print("Environment = {0}".format(environment))
print("Project Name = {0}".format(projectName))
print("AWS Region = {0}".format(awsRegion))
print("Instance Type = {0}".format(instanceType))
print("Private Key Path = {0}".format(privateKeyPath))
print("Public Key Path = {0}".format(publicKeyPath))

#        / ___|___  _ __ | |_ __ _(_)_ __   ___ _ __ ___ 
#        | |   / _ \| '_ \| __/ _` | | '_ \ / _ \ '__/ __|
#        | |__| (_) | | | | || (_| | | | | |  __/ |  \__ \
#         \____\___/|_| |_|\__\__,_|_|_| |_|\___|_|  |___/

def createResource(name, type, props):
    if not repository.exists(name):
        if props:
            myCI = factory.configurationItem(name, type, props)
        else:
            myCI = factory.configurationItem(name, type)
        repository.create(myCI)
        print("CI {0} created".format(name))
    else:
        print("CI {0} existed".format(name))

# Funciones para la creacion de environments
def createOrUpdateDictionary():
    dictEntries = {
        'aws_region': awsRegion,
        'environment': environment,
        'instance_type': instanceType,
        'private_key_path': privateKeyPath,
        'public_key_path': publicKeyPath
    }
    dictionaryName = "Environments/infrastructure-{0}/infrastructure-{0}-{1}/infrastructure-{0}-{1}-dict".format(projectName, environment)
    if not repository.exists(dictionaryName):
        myDict = factory.configurationItem(dictionaryName, 'udm.Dictionary', {'entries': dictEntries})
        repository.create(myDict)
        print("Dictionary {0} created".format(dictionaryName))
    else:
        myDict = repository.read(dictionaryName)
        myDict.entries = dictEntries
        repository.update(myDict)
        print("Dictionary {0} updated".format(dictionaryName))

def createOrUpdateEnvironment():
    environmentName = "Environments/infrastructure-{0}/infrastructure-{0}-{1}/infrastructure-{0}-{1}".format(projectName, environment)
    myContainer = "Infrastructure/Terraform/terraform-host-{0}/{1}-{0}".format(environment, projectName)
    myDict = "Environments/infrastructure-{0}/infrastructure-{0}-{1}/infrastructure-{0}-{1}-dict".format(projectName, environment)
    if not repository.exists(environmentName):
        myEnvironment = factory.configurationItem(environmentName, 'udm.Environment', {'members': [myContainer], 'dictionaries': [myDict]})
        repository.create(myEnvironment)
        print("Environment {0} created".format(environmentName))
    else:
        myEnvironment = repository.read(environmentName)
        myEnvironment.members = [myContainer]
        myEnvironment.dictionaries = [myDict]
        repository.update(myEnvironment)
        print("Environment {0} updated".format(environmentName))

# Creación de los CIs bajo Infrastructure
# 1.- Carpeta de nombre 'Terraform'
createResource("Infrastructure/Terraform", "core.Directory", None)

# 2.- overthere.LocalHost de nombre 'terraform-host'
hostName = "Infrastructure/Terraform/terraform-host-{0}".format(environment)
createResource(hostName, "overthere.LocalHost", {'os': 'UNIX'})

# 3.- terraform.TerraformClient de nombre infrastructure-project-dev
clientName = "Infrastructure/Terraform/terraform-host-{0}/{1}-{0}".format(environment, projectName)
workingDirectory = "/var/opt/xebialabs/terraform-states/{0}-{1}".format(projectName, environment)
createResource(clientName, "terraform.TerraformClient", {'workingDirectory': workingDirectory})

# 4.- Creating the environment stuff
createResource("Environments/infrastructure-{0}".format(projectName), "core.Directory", None)
createResource("Environments/infrastructure-{0}/infrastructure-{0}-{1}".format(projectName, environment), "core.Directory", None)

# 5.- Creating the dictionary
createOrUpdateDictionary()

# 6.- Creating the environment
createOrUpdateEnvironment()