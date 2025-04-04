def metaPath = "iam/security-credentials"
def fullPath = "http://169.254.169.254/latest/meta-data/${metaPath}"

def cmdString = """
TOKEN=\$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
echo "Token: \$TOKEN"

VALUE=\$(curl -s -H "X-aws-ec2-metadata-token: \$TOKEN" "${fullPath}")
echo "Metadata (${metaPath}): \$VALUE"

if [ -n "\$VALUE" ]; then
  echo "Full Response:"
  curl -s -H "X-aws-ec2-metadata-token: \$TOKEN" "${fullPath}/\$VALUE"
else
  echo "No value returned for metadata path: ${metaPath}"
fi
"""

def cmd = ['bash', '-c', cmdString]

def proc = cmd.execute()
def output = new StringBuffer()
def error = new StringBuffer()

proc.consumeProcessOutput(output, error)
proc.waitFor()

println "STDOUT:\n${output.toString()}"
println "STDERR:\n${error.toString()}"
