import psycopg2
import pandas as pd
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
        
user_id = []
user_img_url = []
confidence = []
        
#connect to datasbaset
try:
    conn = psycopg2.connect(
        dbname='socialmining',
        user='power_user',
        password='$poweruserpassword',
        host='ec2-13-58-84-129.us-east-2.compute.amazonaws.com',
        port='5432',
    )
    cursor = conn.cursor()

#query data
    select_user = """
        select user_id, user_image_url from users 
        where user_id not in (select user_id from users_analysis) 
    """
    cursor.execute(select_user)
    
    print("Selecting rows from table")
    user_records = cursor.fetchall() 
   
    print("Print each row and it's columns values")
    
    for row in user_records:
        try:
            object1 = []
            # print("user_id = ", row[0])       
            # print("user_image_url = ", row[1])
            user_id = row[0]
            user_img_url = row[1]
            
            #import os
            endpoint = "https://westcentralus.api.cognitive.microsoft.com/"
            key = "8cf13aca74734e2b8be4f84207ea2a82"
            credentials = CognitiveServicesCredentials(key)
            client = ComputerVisionClient(endpoint, credentials)
            # print('just before url')
            
            #ANALYZE AN IMAGE
            image_analysis = client.analyze_image(user_img_url, visual_features=[VisualFeatureTypes.tags])
            # print('just before tag')
            for tag in image_analysis.tags:
                # print("TAG: ", tag, dir(tag))
                object1.append({"name": tag.name, "conf": tag.confidence})
            #create result dataframe
            # user_id = result["user_id"]
            user_id = int(user_id)
            
            #insert result into database  
            INSERT_QUERY = f"""
                INSERT INTO users_analysis(user_id, objects, confidence)
                VALUES(%s, %s, %s)
            """
    
            for obj in object1:
                print(user_id,obj["name"],obj["conf"])
                cursor.execute(INSERT_QUERY, (user_id,obj["name"],obj["conf"]))
            conn.commit()
        except Exception as e:
            print("Got: ", e)
            

        
except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

cursor.close()
conn.close()