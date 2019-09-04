lastVersion="${last-version}"
if lastVersion == "":
    lastVersion = "App/1.0.0-B0"
array=lastVersion.split("/")
array=array[-1].split("-B")
newBuild=int(array[1])+1
darVersion="${component-version}"+"-B"+str(newBuild)
releaseVariables['next-version']=darVersion
