# coding: utf-8
import sys
print(sys.prefix)
import boto3

session = boto3.Session(profile_name='admin')
key_name = 'python_automation_key.pem'
'''This block is just to spin up an ec2 instance'''
img = ec2.Image('ami-00068cd7555f543d5')
ec2 = session.resource('ec2')
ec2 = session.resource('ec2')
img = ec2.Image('ami-00068cd7555f543d5')
img.id
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key_name)
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName='python_automation_key')
clear
get_ipython().run_line_magic('cls', '')
instances
'''This block is the end of ec2 instance spin up'''
asg_client  = session.client('autoscaling')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cls', '')
ec2
asg_client
instances
#asg = asg_client.create_auto_scaling_group(AutoScalingGroupName='NotifonASG',MinSize=1,MaxSize=2,DesiredCapacity=1,DefaultCooldown=15)
asg = asg_client.create_auto_scaling_group(AutoScalingGroupName='NotifonASG',InstanceId='i-0ea4dcaa83cf00d71',MinSize=1,MaxSize=2,DesiredCapacity=1,DefaultCooldown=15)
asg
asg_client.attach_instances(InstanceIds=['i-0ea4dcaa83cf00d71'],AutoScalingGroupName='NotifonASG')
ec2.meta.client.terminate_instances(InstanceIds=['i-07d24ebcaabb09c2a'])
get_ipython().run_line_magic('history', '')
asg_client.delete_auto_scaling_group(AutoScalingGroupName='NotifonASG',ForceDelete=True)
