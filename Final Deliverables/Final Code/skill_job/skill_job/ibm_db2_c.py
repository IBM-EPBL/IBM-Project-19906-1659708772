import ibm_db
import time
host_name = '55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud'
port = '31929'
uid = 'zxj93471'
passcode = 'R1fGU10DozFO0Yh2'
DRIVER ='{IBM DB2 ODBC DRIVER}'
database = 'bludb'
protocol = 'TCPIP'
SECURITY = 'SSL'
#'SSLServerCertificate='+SSLServerCertificate

print(conn_str)
start = time.time()
try:
	ibm_db_conn = ibm_db.connect(conn_str,'','')
except:
    print("Error in connection, sqlstate = ")
    errorState = ibm_db.conn_error()
    print(errorState)
    error_msg = ibm_db.conn_errormsg()
    print(error_msg)
print('Time:', time.time()-start)

try:
	server = ibm_db.server_info(ibm_db_conn)
	print(server)
	print('a1', server.DBMS_NAME, server.DBMS_VER, server.DB_NAME)
except Exception as e:
    print("? server", e)

try:
	stmt_select = ibm_db.exec_immediate(ibm_db_conn, 'select * from user')
	cols = ibm_db.fetch_tuple( stmt_select )
	print('cols', cols)
	query_string = "insert into user values (?,?,?,?,?,?,?,?)"
	params = ((1, 'shan', 'user_name', 'email', 'password', 'contact_no', 'gender', 'role'), ) 
	print(params)
	stmt_select = ibm_db.prepare(ibm_db_conn, query_string)
	ibm_db.execute_many(stmt_select,params)

except Exception as e:
    print("? ops", e)

ibm_db.close(ibm_db_conn)
