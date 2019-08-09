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

# Funciones para la creación de recursos
def createDirectory(directory):
    if not repository.exists(directory):
        repository.create(factory.configurationItem(directory, 'core.Directory'))
        print("Directory {0} created".format(directory))
    else:
        print("Directory {0} existed".format(directory))

def createTerraformHost():
    hostName = "Infrastructure/Terraform/terraform-host-{0}".format(environment)
    if not repository.exists(hostName):
        myTerraformHost = factory.configurationItem(hostName, 'overthere.LocalHost', { 'os': 'UNIX'})
        repository.create(myTerraformHost)
        print("Host {0} created".format(hostName))
    else:
        print("Host {0} existed".format(hostName))

def createTerraformClient():
    clientName = "Infrastructure/Terraform/terraform-host-{0}/{1}-{0}".format(environment, projectName)
    workingDirectory = "/var/opt/xebialabs/terraform-states/{0}-{1}".format(projectName, environment)
    if not repository.exists(clientName):
        myTerraformClient = factory.configurationItem(clientName, 'terraform.TerraformClient', { 'workingDirectory': workingDirectory})
        repository.create(myTerraformClient)
        print("Client {0} created".format(clientName))
    else:
        print("Client {0} existed".format(clientName))

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
createDirectory("Infrastructure/Terraform")

# 2.- overthere.LocalHost de nombre 'terraform-host'
createTerraformHost()

# 3.- terraform.TerraformClient de nombre infrastructure-calculator-dev
createTerraformClient()

# 4.- Creating the environment stuff
createDirectory("Environments/infrastructure-{0}".format(projectName))
createDirectory("Environments/infrastructure-{0}/infrastructure-{0}-{1}".format(projectName, environment))

# 5.- Creating the dictionary
createOrUpdateDictionary()

# 6.- Creating the environment
createOrUpdateEnvironment()