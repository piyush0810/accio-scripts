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


cursor.execute("SELECT * from zoho_temp2 limit 10000")
while True:
    data = cursor.fetchone()
    if(data==None):
        break
    

    url = "https://www.zohoapis.in/crm/v2/leads"
    # print(data)
    payload = json.dumps({
    "data": [
        {
        "Last_Name": str(data[0]),
        "Mobile": str(data[1]),
        "description": str(data[2]),
        "Lead_Status": "Not Qualified",
        "Lead_Source":str(data[3]),
        "Coding_Test1_Date":data[4].strftime("%Y-%m-%dT%H:%M:%S.%fZ") if data[4] != None else str(None),
        "Interview_Status":str(data[5]),
        "Coding_Test_Status":str(data[6]),
        "Coding_Test2_Date":data[7].strftime("%Y-%m-%dT%H:%M:%S.%fZ") if data[7] != None else str(None),
        "Interview_Date":data[8].strftime("%Y-%m-%dT%H:%M:%S.%fZ") if data[8] != None else str(None),
        "Email":str(data[9]),
        "CBR_Date_Time":str(data[10]),
        "Call_Back_Requested1":str(data[11]),
        "Graduation_Year":str(data[12]),
        "Progress_Status":str(data[13]),
        "Questions_Solved1":str(data[14]),
        "Last_Question_Solved":str(data[15])
        }
    ],
    "trigger": [
        "approval",
        "workflow",
        "blueprint"
    ]
    })
    headers = {
    'Authorization': 'Zoho-oauthtoken 1000.3d2cb479e9c5a57cf36e4e24b18911b9.63819baabca7cb920faeb35901788d68',
    'Content-Type': 'application/json',
    }
    # print(payload)
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(json.loads(response.text))
    leadid= json.loads(response.text)['data'][0]['details']['id']
    userid=data[16]
    
    cursor2.execute(f"insert into sales_leads (\"userId\",\"leadId\") values ('{userid}','{leadid}')")
    conn2.commit()

    


# Fetch a single row using fetchone() method.
# data = cursor.fetchall()
# print("Connection established to: ",data)
print(cursor.fetchone())
#Closing the connection
conn2.close()
conn.close()

# Printing the connection object

