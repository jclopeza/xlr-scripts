# Este script se invoca de forma remota desde el template de creación de infraestructuras con Terraform en AWS
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -username admin -password ***** -f /home/jcla/Projects/xlr-scripts/createXLDResourcesK8sCanaryDeploy.py vota-mi-pelota 90 10 1.0.0 2.0.0

import sys
application = sys.argv[1]
trafficPercentageForService1 = sys.argv[2]
trafficPercentageForService2 = sys.argv[3]
versionService1 = sys.argv[4]
versionService2 = sys.argv[5]

print("Application = {0}".format(application))
print("Percentage for service 1 = {0}".format(trafficPercentageForService1))
print("Percentage for service 2 = {0}".format(trafficPercentageForService2))
print("Version service 1 = {0}".format(versionService1))
print("Version service 2 = {0}".format(versionService2))

# Function for updating the dictionary
def createOrUpdateDictionary():
    dictEntries = {
        "environment": "pro",
        "traffic-percentage-for-service-{0}".format(versionService1): trafficPercentageForService1,
        "traffic-percentage-for-service-{0}".format(versionService2): trafficPercentageForService2,
    }
    dictionaryName = "Environments/dictionaries-{0}-k8s/dictionary-application-{0}-k8s-pro".format(application)
    if not repository.exists(dictionaryName):
        myDict = factory.configurationItem(dictionaryName, 'udm.Dictionary', {'entries': dictEntries})
        repository.create(myDict)
        print("Dictionary {0} created".format(dictionaryName))
    else:
        myDict = repository.read(dictionaryName)
        myDict.entries = dictEntries
        repository.update(myDict)
        print("Dictionary {0} updated".format(dictionaryName))

# Updating the dictionary
createOrUpdateDictionary()