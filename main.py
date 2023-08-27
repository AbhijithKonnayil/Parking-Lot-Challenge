import json
import os
import random

import boto3
from botocore.client import ClientError

FileName="parking_data.json"
class ParkingLot:
    def __init__(self,area,parking_slot_area) -> None:
        self.area = area
        self.slots_count=self.area//parking_slot_area
        self.slots = [None]* self.slots_count
    
    @property
    def is_full(self):
        return None not in self.slots

    def slot_map(self):
        return {str(car):index for index,car in enumerate(self.slots) if car is not None}
    
    def write_to_file(self,):
        file_path = FileName
        with open(file_path, 'w') as file:
            json.dump(self.slot_map(), file)

    
class Car:
    def __init__(self,license_no) -> None:
        self.license_no = license_no

    def __repr__(self):
        return f"Car {self.license_no}"
    
    def park(self,parking_lot:ParkingLot,slot):
        if(parking_lot.slots[slot]):
            return False
        parking_lot.slots[slot]=self
        return True

def upload_file(file_name, bucket, object_name=None):
    s3_client = boto3.client('s3')
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        print(e)
        return False
    print("File Uploaded to S3")

def main():
    parking_lot = ParkingLot(area=2000,parking_slot_area=96)
    no_of_car= int(input("Enter the number of cars :"))
    cars=[]
    for i in range (no_of_car):
        no_plate = random.randint(1000000,9999999)
        cars.append(Car(license_no=no_plate))
    
    while cars and not parking_lot.is_full:
        car = cars.pop()
        slot = random.randint(0,parking_lot.slots_count-1)
        while True:
            if car.park(parking_lot,slot):
                print(f"Car with license plate {car.license_no} parked successfully in spot {slot}")
                break
            else:
                print(f"Car with license plate {car.license_no} was not parked in spot {slot}")
            slot = random.randint(0,parking_lot.slots_count-1)

    parking_lot.write_to_file()
    inp = input("Do you want to upload the result to S3 ? (y/n)")

    if(inp.lower()=="y"):
        bucket = input("Enter the S3 Bucket ?")
        upload_file(FileName,bucket=bucket)

if __name__ == '__main__':
    main()