# Este script se invoca de forma remota desde el template de creación de infraestructuras con Terraform en AWS
# En este script tenemos que crear una serie de containers en XLD para poder desplegar la aplicación de calculadora.
# La invocación se debe realizar de la siguiente forma:
# ./bin/cli.sh -username admin -password ***** -f createXLDResourcesTerraformModuleJavaBddProjectContainers.py dev calculator 1.2.3.4 1.2.3.4

import sys
environment = sys.argv[1]
projectName = sys.argv[2]
ipFront = sys.argv[3]
ipBdd = sys.argv[4]

print("Environment = {0}".format(environment))
print("Project Name = {0}".format(projectName))
print("IP Front = {0}".format(ipFront))
print("IP Bdd = {0}".format(ipBdd))

hostFront = "Infrastructure/{0}-{1}-front".format(projectName, environment)
hostBdd = "Infrastructure/{0}-{1}-bdd".format(projectName, environment)

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

# Creación del axis2
createResource("{0}/axis2".format(hostFront), "axis2.Deployer", {'axis2ServicesDirectory': '/opt/apache-tomcat-8.5.8/webapps/axis2/WEB-INF/services'})
# Creación del tomcat
tomcatProps = {
    'home': '/opt/apache-tomcat-8.5.8',
    'startCommand': 'sudo service tomcat start',
    'stopCommand': 'sudo service tomcat stop',
    'statusCommand': 'sudo service tomcat status'
}
createResource("{0}/tomcat".format(hostFront), "tomcat.Server", tomcatProps)
# Creación del virtual host
virtualHostProps = {
    'appBase': 'webapps',
    'hostname': 'localhost'
}
createResource("{0}/tomcat/vh-{1}".format(hostFront, projectName), "tomcat.VirtualHost", virtualHostProps)
# Creación del smokeTest
createResource("{0}/smokeTest".format(hostFront), "smoketest.Runner", {'powershellInstalled': False})
# Creación de la base de datos
bddProps = {
    'username': 'cng_user',
    'password': 'cng_password',
    'mySqlHome': '/usr',
    'databaseName': 'congruencias'
}
createResource("{0}/mysql-cli".format(hostBdd), "sql.MySqlClient", bddProps)

# |  _ \(_) ___| |_(_) ___  _ __   __ _ _ __(_) ___  ___ 
# | | | | |/ __| __| |/ _ \| '_ \ / _` | '__| |/ _ \/ __|
# | |_| | | (__| |_| | (_) | | | | (_| | |  | |  __/\__ \
# |____/|_|\___|\__|_|\___/|_| |_|\__,_|_|  |_|\___||___/

createResource("Environments/dictionaries-{0}".format(projectName), "core.Directory", None)

def createOrUpdateDictionary():
    dictEntries = {
        'ip_front': ipFront,
        'ip_bdd': ipBdd
    }
    dictionaryName = "Environments/dictionaries-{0}/dictionary-infrastructure-{0}-{1}".format(projectName, environment)
    if not repository.exists(dictionaryName):
        myDict = factory.configurationItem(dictionaryName, 'udm.Dictionary', {'entries': dictEntries})
        repository.create(myDict)
        print("Dictionary {0} created".format(dictionaryName))
    else:
        myDict = repository.read(dictionaryName)
        myDict.entries = dictEntries
        repository.update(myDict)
        print("Dictionary {0} updated".format(dictionaryName))


# Creating the dictionary
createOrUpdateDictionary()

# | ____|_ ____   _(_)_ __ ___  _ __  _ __ ___   ___ _ __ | |_ ___ 
# |  _| | '_ \ \ / / | '__/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __/ __|
# | |___| | | \ V /| | | | (_) | | | | | | | | |  __/ | | | |_\__ \
# |_____|_| |_|\_/ |_|_|  \___/|_| |_|_| |_| |_|\___|_| |_|\__|___/

def createOrUpdateEnvironment():
    environmentName = "Environments/application-{0}/application-{0}-{1}/application-{0}-{1}".format(projectName, environment)
    dictionaryInfrastructureName = "Environments/dictionaries-{0}/dictionary-infrastructure-{0}-{1}".format(projectName, environment)
    dictionaryApplicationName = "Environments/dictionaries-{0}/dictionary-application-{0}-{1}".format(projectName, environment)
    dictionaries = [dictionaryInfrastructureName]
    if repository.exists(dictionaryApplicationName):
        dictionaries = dictionaries + [dictionaryApplicationName]
    myContainers = [
        "{0}/axis2".format(hostFront),
        "{0}/tomcat/vh-{1}".format(hostFront, projectName),
        "{0}/smokeTest".format(hostFront),
        "{0}/mysql-cli".format(hostBdd)
    ]
    if not repository.exists(environmentName):
        myEnvironment = factory.configurationItem(environmentName, 'udm.Environment', {'members': myContainers, 'dictionaries': dictionaries})
        repository.create(myEnvironment)
        print("Environment {0} created".format(environmentName))
    else:
        myEnvironment = repository.read(environmentName)
        myEnvironment.members = myContainers
        myEnvironment.dictionaries = dictionaries
        repository.update(myEnvironment)
        print("Environment {0} updated".format(environmentName))

# Necesitamos crear un entorno que agrupe los distintos elementos que hemos creado antes
# Primero creamos la estructura de directorios
createResource("Environments/application-{0}".format(projectName), "core.Directory", None)
createResource("Environments/application-{0}/application-{0}-{1}".format(projectName, environment), "core.Directory", None)
createOrUpdateEnvironment()