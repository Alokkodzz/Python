import boto3

def lambda_handler(event, context):

    ec2 = boto3.client('ec2')
    response = ec2.describe_snapshots(OwnerIds=['self'])

    Instance_response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name','Values': ['running']},])
    snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

    active_instance_ids = set()


    for Reservation in Instance_response['Reservations']:
        for Instance in Reservation['Instances']:
            active_instance_ids.add(Instance['InstanceId'])
            for Snapshot in snapshot_response['Snapshots']:
                Snapshot_Id = Snapshot['SnapshotId']
                Volume_Id = Snapshot.get('VolumeId')
                print(Snapshot)

                if not Volume_Id:
                    ec2.delete_snapshot(Snapshot_Id)
                    print(f"deleted snapshot {Snapshot_Id} as it was not attached to any volume")
                else:
        
                    try:
                        volume_response = ec2.describe_volumes(VolumeIds=[Volume_Id])
                        if not volume_response['Volumes'][0]['Attachments']:
                            ec2.delete_snapshot(SnapshotId=Snapshot_Id)
                            print(f"deleted snapshot {Snapshot_Id} as it was taken from a volume not attched to any instance")
                    except ec2.exceptions.ClientError as e:
                        if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                            ec2.delete_snapshot(SnapshotId=Snapshot_Id)
                            print(f"deleted snapahot {Snapshot_Id} as its associated volume was not found")