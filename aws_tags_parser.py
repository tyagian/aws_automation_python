import sys
import boto3

# python aws_tags.py ec2,rds eu-central-1,us-east-1

def get_rds_tags(region):
    rds = boto3.client('rds', region_name=region)
    response = rds.describe_db_instances()
    if response: 
        for db_instance in response['DBInstances']:
            db_instance_Arn = db_instance['DBInstanceArn']
            tags = rds.list_tags_for_resource(ResourceName=db_instance_Arn)['TagList']
            print(f"Tags for RDS instance {db_instance_Arn} in region {region}: {tags}")

def get_ec2_tags(region):
    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.all()

    for instance in instances:
        tags = instance.tags or []
        print(f"Tags for EC2 instance {instance.id} in region {region}: {tags}")

def get_s3_tags(region):
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_buckets()

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        tags = s3.get_bucket_tagging(Bucket=bucket_name)['TagSet']
        print(f"Tags for S3 bucket {bucket_name} in region {region}: {tags}")

def get_msk_tags(region):
    msk = boto3.client('kafka', region_name=region)
    clusters = msk.list_clusters()['ClusterInfoList']

    for cluster in clusters:
        cluster_arn = cluster['ClusterArn']
        tags = msk.list_tags_for_resource(ResourceArn=cluster_arn)['Tags']
        print(f"Tags for MSK cluster {cluster_arn} in region {region}: {tags}")

def get_elemental_live_tags(region):
    elemental = boto3.client('medialive', region_name=region)
    channels = elemental.list_channels()['Channels']

    for channel in channels:
        channel_arn = channel['Arn']
        tags = elemental.list_tags_for_resource(ResourceArn=channel_arn)['Tags']
        print(f"Tags for Elemental Live channel {channel_arn} in region {region}: {tags}")

def get_vpc_tags(region):
    ec2 = boto3.client('ec2', region_name=region)
    vpcs = ec2.describe_vpcs()['Vpcs']

    for vpc in vpcs:
        vpc_id = vpc['VpcId']
        tags = ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [vpc_id]}])['Tags']
        print(f"Tags for VPC {vpc_id} in region {region}: {tags}")

def get_cloudfront_tags(region):
    cloudfront = boto3.client('cloudfront', region_name=region)
    distributions = cloudfront.list_distributions()['DistributionList']['Items']

    if distributions: 
        for distribution in distributions:
            #print (distribution)
            distribution_arn = distribution['ARN']
            tags = cloudfront.list_tags_for_resource(Resource=distribution_arn)['Tags']
            print(f"Tags for CloudFront distribution {distribution_arn} in region {region}: {tags}")

def get_cloudwatch_tags(region):
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    alarms = cloudwatch.describe_alarms()['MetricAlarms']

    for alarm in alarms:
        alarm_name = alarm['AlarmName']
        tags = cloudwatch.list_tags_for_resource(ResourceARN=alarm['AlarmArn'])['Tags']
        print(f"Tags for CloudWatch alarm {alarm_name} in region {region}: {tags}")

def get_elb_tags(region):
    elbv2 = boto3.client('elbv2', region_name=region)
    load_balancers = elbv2.describe_load_balancers()['LoadBalancers']

    for load_balancer in load_balancers:
        load_balancer_arn = load_balancer['LoadBalancerArn']
        tags = elbv2.describe_tags(ResourceArns=[load_balancer_arn])['TagDescriptions'][0]['Tags']
        print(f"Tags for Elastic Load Balancer {load_balancer_arn} in region {region}: {tags}")

def get_eks_tags(region):
    eks = boto3.client('eks', region_name=region)
    clusters = eks.list_clusters()['clusters']

    for cluster_name in clusters:
        cluster_arn = eks.describe_cluster(name=cluster_name)['cluster']['arn']
        tags = eks.list_tags_for_resource(resourceArn=cluster_arn)['tags']
        print(f"Tags for Elastic Container Service for Kubernetes (EKS) cluster {cluster_name} in region {region}: {tags}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <service_names> <regions>")
        sys.exit(1)

    service_names = sys.argv[1].split(',')
    regions = sys.argv[2].split(',')

    for service_name in service_names:
        for region in regions:
            if service_name.lower() == 'rds':
                get_rds_tags(region)
            elif service_name.lower() == 'ec2':
                get_ec2_tags(region)
            elif service_name.lower() == 's3':
                get_s3_tags(region)
            elif service_name.lower() == 'msk':
                get_msk_tags(region)
            elif service_name.lower() == 'elemental':
                get_elemental_live_tags(region)
            elif service_name.lower() == 'vpc':
                get_vpc_tags(region)
            elif service_name.lower() == 'cloudfront':
                get_cloudfront_tags(region)
            elif service_name.lower() == 'cloudwatch':
                get_cloudwatch_tags(region)
            elif service_name.lower() == 'elb':
                get_elb_tags(region)
            elif service_name.lower() == 'eks':
                get_eks_tags(region)
            else:
                print(f"Invalid service name: {service_name}. Supported services: rds, ec2, s3, msk, elemental, vpc, cloudfront, cloudwatch, elb, eks")
                sys.exit(1)
