from jinja2 import Template
import datetime
import sys

# Recogemos variables
environment = sys.argv[1]
projectName = sys.argv[2]
awsRegion = sys.argv[3]
instanceType = sys.argv[4]
versionTerraform = sys.argv[5]
versionAnsible = sys.argv[6]

t = Template("""
<html>
  <head>
    <title>
      Grafico generado para el proyecto {{ projectName }} y entorno {{ environment }}
    </title>
  </head>
  <body>
    <p>
      <center><h2>Infraestructura desplegada para el proyecto <u>{{ projectName }}</u> y entorno <u>{{ environment }}</u></h2></center>
    </p>
    <p>
      <table width="100%" border=1>
        <tr>
          <td width="20%" align=center>
            <table>
              <tr>
                <td><b>Region AWS</b></td><td width="15%"></td><td>{{ awsRegion }}</td>
              </tr>
              <tr>
                <td><b>Proyecto</b></td><td width="15%"></td><td>{{ projectName }}</td>
              </tr>
              <tr>
                <td><b>Entorno</b></td><td width="15%"></td><td>{{ environment }}</td>
              </tr>
              <tr>
                <td><b>Instancias EC2</b></td><td width="15%"></td><td>{{ instanceType }}</td>
              </tr>
              <tr>
                <td><b>Fecha</b></td><td width="15%"></td><td>{{ date }}</td>
              </tr>
              <tr>
                <td><b>Hora</b></td><td width="15%"></td><td>{{ hour }}</td>
              </tr>
            </table>
          </td>
          <td width="80%" align=center>
            <img src="graph.svg" width="80%">
          </td>
        </tr>

        <tr>
          <td width="20%" align=center>
          </td>
          <td width="80%" align=left>
            <b>Versión de infraestructura aplicacda: </b>{{ versionTerraform }}<br>
            <b>Versión de Playbooks de Ansible: </b>{{ versionAnsible }}<br>
          </td>
        </tr>
      </table>
    </p>
  </body>
</html>
""")
x = datetime.datetime.now()
htmlGenerated = t.render(
    projectName=projectName,
    environment=environment,
    awsRegion=awsRegion,
    instanceType=instanceType,
    date=x.strftime("%d/%m/%Y"),
    hour=x.strftime("%H:%M:%S"),
    versionTerraform = versionTerraform,
    versionAnsible = versionAnsible
    )
f = open("/var/www/html/{0}-{1}/index.html".format(projectName, environment), "w")
f.write(htmlGenerated)
f.close()
