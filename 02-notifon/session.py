# coding: utf-8
import boto3
session = boto3.Session(profile_name='admin')
ec2 = session.resource('ec2')
key_name = 'python_automation_key'
key_path = key_name + '.pem'
key = ec2.create_key_pair(KeyName=key_name)
key.key_material
key.key_name
with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)
get_ipython().run_line_magic('ls', '-l python_automation_key.pem')
import os,stat
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
get_ipython().run_line_magic('ls', '-l python_automation_key.pem')
ec2.images.filter(Owners=['amazon'])
ec2.images.filter(Owners=['amazon'])
list(ec2.images.filter(Owners=['amazon']))
list(ec2.images.filter(Owners=['amazon']))
len(list(ec2.images.filter(Owners=['amazon'])))
img = ec2.Image('ami-00068cd7555f543d5')
img.name
filters = [{'Name':'name','Values':[ami_name]}]
list(ec2.images.filter(Owners=['amazon'],Filters=filters))
img.id
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
instances
inst = instances[0]
inst.public_dns_name
inst.wait_until_running()
inst.reload()
inst.public_dns_name
inst.security_groups
#print(inst)
#print(inst.__dict__)
sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
sg.authorize_ingress(IpPermissions=[{'FromPort':22,'ToPort':22,'IpProtocol': 'TCP','IpRanges':[{'CidrIp':'103.218.170.8/32','Description': 'Allow SSH to my IP'}]}])
inst.terminate()
