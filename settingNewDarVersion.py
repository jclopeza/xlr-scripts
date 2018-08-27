lastVersion="${lastVersion}"
array=lastVersion.split("-B")
newBuild=int(array[1])+1
darVersion=array[0]+"-B"+str(newBuild)
releaseVariables['versionNumber']=darVersion

