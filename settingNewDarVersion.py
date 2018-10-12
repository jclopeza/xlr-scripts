lastVersion="${last-version}"
array=lastVersion.split("/")
array=array[-1].split("-B")
newBuild=int(array[1])+1
darVersion="${component-version}"+"-B"+str(newBuild)
releaseVariables['next-version']=darVersion
