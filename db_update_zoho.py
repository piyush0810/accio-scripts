# Importing module
import psycopg2
import requests
import json
# Creating connection object

conn = psycopg2.connect(
 	host = "accio-prod-do-user-9368613-0.b.db.ondigitalocean.com",
	user = "doadmin",
	password = "p2jvqo3303xxw9b3",
    database = "accio-app-prod",
    port = "25060"
)


conn2 = psycopg2.connect(
 	host = "accio-prod-do-user-9368613-0.b.db.ondigitalocean.com",
	user = "doadmin",
	password = "p2jvqo3303xxw9b3",
    database = "accio-app-prod",
    port = "25060"
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()
cursor2 = conn2.cursor()

#Executing an MYSQL function using the execute() method


cursor.execute("SELECT * from zoho_temp1 limit 10000")
while True:
    data = cursor.fetchone()
    if(data==None):
        break
    cursor2.execute(f"select \"leadId\" from sales_leads where \"userId\"='{data[16]}'")
    
    Leadid=cursor2.fetchone()
    if(Leadid==None):
        continue
    Leadid=Leadid[0]
    
    
    url = "https://www.zohoapis.in/crm/v2/leads"
    # print(data)
    payload = json.dumps({
    "data": [
        {
            "id":Leadid,
        "Last_Name": str(data[0]),
        "Mobile": str(data[1]),
        "description": str(data[2]),
        "Lead_Status": "Not Qualified",
        "Lead_Source":str(data[3]),
        "Coding_Test1_Date":data[4].strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-14] if data[4] != None else None,
        "Interview_Status":str(data[5]),
        "Coding_Test_Status":str(data[6]),
        "Coding_Test2_Date":data[7].strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-14] if data[7] != None else None,
        "Interview_Date":data[8].strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-14] if data[8] != None else None,
        "Email":str(data[9]),
        "CBR_Date_Time":str(data[10])[:-14],
        "Call_Back_Requested1":str(data[11]),
        "Graduation_Year":str(data[12]),
        "Progress_Status":str(data[13]),
        "Questions_Solved1":str(data[14]),
        "Last_Question_Solved":str(data[15])[:-14] if data[15]!=None else None,
        "IsAgreementSigned":str(data[17]),
        "Number_of_Lectures_attended_in_precourse":data[18],
        "Last_Lecture_Attended":str(data[19])[:-5] if data[19]!=None else None
        # "Created_Date_Time":str(data[16])
        }
    ],
    "trigger": [
        "approval",
        "workflow",
        "blueprint"
    ]
    })
    headers = {
    'Authorization': 'Zoho-oauthtoken 1000.f59e2f48fe75759a27f296d30c8a1cbb.b482a117a7e28a65e06fda09438392cf',
    'Content-Type': 'application/json',
    }
    # print(payload)
    
    response = requests.request("PUT", url, headers=headers, data=payload)
    if(json.loads(response.text)['data'][0]['message']=='the id given seems to be invalid'):
        cursor2.execute(f"delete from sales_leads where \"userId\"='{data[16]}'")
        conn2.commit()
    print(json.loads(response.text))
    
    
    

    


# Fetch a single row using fetchone() method.
# data = cursor.fetchall()
# print("Connection established to: ",data)

#Closing the connection
conn2.close()
conn.close()

# Printing the connection object

