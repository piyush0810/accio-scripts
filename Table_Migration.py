# Importing module
import psycopg2
import requests
import json
# Creating connection object

src_conn = psycopg2.connect(
 	host = "accio-staging-26-05-22-do-user-9368613-0.b.db.ondigitalocean.com",
	user = "doadmin",
	password = "p2jvqo3303xxw9b3",
    database = "accio-app-prod",
    port = "25060"
)


target_conn = psycopg2.connect(
 	host = "accio-school-18-apr-2022-do-user-9368613-0.b.db.ondigitalocean.com",
	user = "doadmin",
	password = "AVNS_pOygW8yny903ulM",
    database = "accioschool-staging",
    port = "25060"
)
#Creating a cursor object using the cursor() method
src_cur = src_conn.cursor()
target_cur = target_conn.cursor()

#Executing an MYSQL function using the execute() method


src_cur.execute("SELECT * from coding_question")
while True:
    data = src_cur.fetchone()
    if(data==None):
        break
    
    jsondata=json.dumps(data[7])
    data_string=f"""'{data[0]}','{data[1]}','{data[2]}','{data[3]}',{data[4]},'{data[5]}','{data[6]}','{jsondata}','{data[8]}','{data[9]}','MODULE',%s"""
    
    query="""Insert into coding_question (id,statement,title,difficulty,score,question_type,\"javaPreDriverCode\",\"testCase\",\"createdAt\",\"updatedAt\",\"parentType\",solution) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) On CONFLICT(id) DO NOTHING;"""
    
    target_cur.execute(query,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],jsondata,data[8],data[9],'MODULE',data[11]))
    

    target_conn.commit()

    


# Fetch a single row using fetchone() method.
# data = cursor.fetchall()
# print("Connection established to: ",data)
#Closing the connection
src_conn.close()
target_conn.close()

# Printing the connection object

