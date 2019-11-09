# Para invocar a este script hay que ejecutar lo siguiente
# python3 generateDestinationRules.py vote 32.0.0-B01

from jinja2 import Template
import sys

# Recogemos variables
serviceName = sys.argv[1]
serviceVersion = sys.argv[2]
destinationRuleName = "{0}-{1}-destination-rule".format(serviceName, serviceVersion.replace(".", "-").lower())
destinationRuleSubsetName = "{0}-{1}".format(serviceName, serviceVersion.replace(".", "-"))

t = Template("""
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: {{ destinationRuleName }}
spec:
  host: {{ serviceName }}-service
  subsets:
  - name: {{ destinationRuleSubsetName }}
    labels:
      version: "{{ serviceVersion }}"
""")

yamlGenerated = t.render(
    destinationRuleName=destinationRuleName,
    serviceName=serviceName,
    destinationRuleSubsetName=destinationRuleSubsetName,
    serviceVersion=serviceVersion
    )

f = open("/tmp/{0}-{1}.yaml".format(serviceName, serviceVersion), "w")
f.write(yamlGenerated)
f.close()
