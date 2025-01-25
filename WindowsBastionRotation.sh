#!/bin/bash

set -e

exec > >(tee -a WindowsBastionRotation.log) 2>&1

function my_regions(){
    env=$1
    account=$(aws sts get-caller-identity --query "Account" --output text)
    
    if [[ "$env" = "staging" && "$account" -eq 544836720487 ]]; then
        regions=("us-west-2" "ca-central-1")
    elif [[ "$env" = "production" && "$account" -eq 127450652264 ]]; then
        regions=("ap-southeast-2" "us-west-2" "us-east-1" "ca-central-1" "us-east-2" "eu-west-1" "eu-central-1" "eu-west-3")
    else
        echo "Please enter correct account"
        exit 1
    fi
    
    Identify_ASG "$regions"
    
}

function Identify_ASG(){    
    
    ASGs=()
    
    for region in "${regions[@]}"; do
        asg_names=$(aws autoscaling describe-auto-scaling-groups --region $region --query "AutoScalingGroups[?contains(AutoScalingGroupName, 'windows') && contains(AutoScalingGroupName, 'bastion')].AutoScalingGroupName" --output text)
    
        for asg_name in $asg_names; do
            ASG="$asg_name,$region"
            ASGs+="$ASG"
            ASGs+=" "
        done
    done
    
    echo "ASGs which are marked for rotation $ASGs"
    Double_Count "$ASGs"
    
}

function Double_Count(){
    
    for ASG in $ASGs; do
        auto_scaling_group="${ASG%%,*}"
        region="${ASG##*,}"
            
        current_desired_count=$(aws autoscaling describe-auto-scaling-groups --region $region --auto-scaling-group-names $auto_scaling_group --query "AutoScalingGroups[0].DesiredCapacity")
        echo "Current desired count $current_desired_count for ASG $auto_scaling_group"
        #echo "ASG: $auto_scaling_group , Region: $region"
        new_desired_count=$(( current_desired_count * 2))
        echo "New desired count $new_desired_count for ASG $auto_scaling_group"
        aws autoscaling update-auto-scaling-group --region $region --auto-scaling-group-name $auto_scaling_group --min-size $new_desired_count --max-size $new_desired_count
        echo "Updated ASG $auto_scaling_group with new desired count $new_desired_count"
    done
    
    echo "Updated all the ASGs $ASGs to new desired count"
    
    wait_for_20_mins "$ASGs"
}


function wait_for_20_mins(){

    for (( i=1; i<=20; i++ )); do
        echo "Minute $i: waiting for 20mins to complete..."
        sleep 60
    done
    
    echo "20 minutes have been passed."
    
    Start_Instance "$ASGs"

}

function Start_Instance(){

    for ASG in $ASGs; do
        auto_scaling_group="${ASG%%,*}"
        region="${ASG##*,}"
    
        instance_ids=$(aws autoscaling describe-auto-scaling-instances --region $region --query "AutoScalingInstances[?AutoScalingGroupName=='$auto_scaling_group'].[InstanceId]" --output text)
    
        for instance_id in $instance_ids; do
            instance_status=$(aws ec2 describe-instances --instance-ids $instance_id --region $region --query "Reservations[*].Instances[*].State.Name" --output text)
            if [ "$instance_status" = "stopped" ]; then
                aws ec2 start-instances --region $region  --instance-ids $instance_id
                echo "started instance $instance_id which is in stopped state"
            else
                echo "Instance $instance_id is in running state"
            fi
        done
    done
    
    echo "Started all the stopped machines... Sleeping for 60 seconds..."
    sleep 60
    
    Decrease_Machines "$ASGs"
}

function Decrease_Machines(){

    for ASG in $ASGs; do
        auto_scaling_group="${ASG%%,*}"
        region="${ASG##*,}"
            
        current_desired_count=$(aws autoscaling describe-auto-scaling-groups --region $region --auto-scaling-group-names $auto_scaling_group --query "AutoScalingGroups[0].DesiredCapacity")
        echo "Current desired count $current_desired_count for ASG $auto_scaling_group"

        new_desired_count=$(( current_desired_count / 2))
        if [ "$new_desired_count" -lt 1 ]; then
            echo " new desired count $new_desired_count for ASG $asg_name is less than one, will skip decreasing the machine count"
        else
            aws autoscaling update-auto-scaling-group --region $region --auto-scaling-group-name $auto_scaling_group --min-size $new_desired_count --max-size $new_desired_count
            echo "Updated ASG $asg_name with new desired count $new_desired_count"
        fi
    done

    echo "Updated all the ASGs $ASGs to regular count"

}

environment=$1

my_regions "$environment"