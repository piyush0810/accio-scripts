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

i=0
cursor.execute("SELECT * from zoho_temp1 limit 10000")
while True:
    data = cursor.fetchone()
    if(data==None):
        break
    
    i=i+1
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
        "Last_Lecture_Attended":str(data[19])[:-5] if data[19]!=None else None,
        "Registration_Date":data[20].strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-2] if data[20] != None else None
        }
    ],
    "trigger": [
        "approval",
        "workflow",
        "blueprint"
    ]
    })
    headers = {
    'Authorization': 'Zoho-oauthtoken 1000.1012435be0b83d3588c79b5b24c24a20.988fdd4d6853bab99f978444ce671046',
    'Content-Type': 'application/json',
    }
    # print(payload)
    
    response = requests.request("POST", url, headers=headers, data=payload)
    print(i)
    print(json.loads(response.text))
    try:
        leadid= json.loads(response.text)['data'][0]['details']['id']
        userid=data[16]
    
        cursor2.execute(f"insert into sales_leads (\"userId\",\"leadId\") values ('{userid}','{leadid}')")
        conn2.commit()
    except:
        print("Variable x is not defined")

    


# Fetch a single row using fetchone() method.
# data = cursor.fetchall()
# print("Connection established to: ",data)
print(cursor.fetchone())
#Closing the connection
conn2.close()
conn.close()

# Printing the connection object

