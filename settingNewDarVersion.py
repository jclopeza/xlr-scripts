lastVersion="${lastVersion}"
array=lastVersion.split("-B")
newBuild=int(array[1])+1
releaseVariables['versionNumber']=array[0]+"-B"+str(newBuild)

