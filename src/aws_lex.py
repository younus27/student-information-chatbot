import json
import requests
from requests_aws4auth import AWS4Auth

with open('aws_credentials.json',"r") as f:
	aws_credentials = json.loads(f.read())

endpoint = 'https://runtime.lex.us-east-1.amazonaws.com/bot/student_information/alias/student_information/user/younus27/text'
auth = AWS4Auth(aws_credentials['AWS_ACCESS_KEY'], aws_credentials['AWS_SECRET_ACCESSKEY'], aws_credentials['REGION'],'lex')


def get_response(inputText):
	# print("\nIn get_response -------------------------------------------")
	response = requests.post(endpoint, json={"inputText": inputText} , auth=auth)
	# print(response)
	# print(response.text)
	# print("Out -------------------------------------------------------\n")

	response = json.loads(response.text)
	if response['message'] == None:
		return resolve_response(response)
	return response['message'] 



def resolve_response(response):

	if response["intentName"] == "fees":
		course   = int(response["slots"]["CourseCategory"])
		category = int(response["slots"]["AdmissionCategory"])

		if course == 1 :
			if category==1:
				return "Fees for BE/B.Tech Open Category is INR 1,38,746"
			elif category==2:
				return "Fees for BE/B.Tech OBC Category is INR 76,892"
			elif category==3:
				return "Fees for BE/B.Tech SC/NT Category is INR 15,038"

		elif course == 2 :
			return "Fees for ME/M.Tech is 2.52 Lakhs for the course of 2 years."

		elif course == 3 :
			if category==1:
				return "Fees for MMS Open Category is 3.04 Lakhs for the course of 2 years."
			elif category==2:
				return "Fees for MMS OBC Category is 1.78 Lakhs for the course of 2 years."
			elif category==3:
				return "Fees for MMS SC/NT Category is 52.00 K for the course of 2 years."

	elif response["intentName"] == "syllabus":
		sem   = int(response["slots"]["sem"])
		stream = int(response["slots"]["stream"])
		dict_ = {1:"IT", 2:"CMPN", 3:"EXTC", 4:"ETRX", 5:"BioMEd"}
		if stream!= 2:
			return f"For {dict_[stream]} Sem {sem} Syllabus please reffer https://www.vidyalankar.org/engineering/syllabus"
		else:
			if sem ==1:
				return	"Subjects For Semester 1:\n\n1. Engineering Mathematics-I\n2. Engineering Physics-I \n3. Engineering Chemistry-I\n4. Engineering Mechanics\n5. Basic Electrical Engineering"
			elif sem ==2:
				return 	"Subjects For Semester 2:\n\n1. Engineering Mathematics-II\n2. Engineering Physics-II\n3. Engineering Chemistry-II\n4. Engineering Graphics\n5. Professional Communication and Ethics- I"

			elif sem ==3:
				return 	"Subjects For Semester 3:\n\n1. Engineering MathematicsIII\n2. Discrete Structures and Graph\n3. Data Structure\n4. Digital Logic & Computer Architecture\n5. Computer Graphics"

			elif sem ==4:
				return 	"Subjects For Semester 4:\n\n1. Engineering Mathematics IV\n2. Analysis of Algorithm \n3. Database Management System\n4. Operating System \n5. Microprocessor"

			elif sem ==5:
				return 	"Subjects For Semester 5:\n\n1. Microprocessor\n2. Database Management System\n3. Computer Network\n4. Theory of Computer Science\n\nDepartment Level Electives\n1. Multimedia System\n2. Advance Operating System\n3. Advance Algorithm"

			elif sem ==6:
				return 	"Subjects For Semester 6:\n\n1. Software Engineering\n2. System Programming & Complier Construction\n3. Data Warehousing & Mining \n4. Cryptography & System Security\n\nDepartment Level Electives\n1. Machine Learning\n2. Advance Database System\n3. Enterprise Resource Planning\n4. Advance Computer Network"

			elif sem ==7:
				return 	"Subjects For Semester 7:\n\n1. Digital Signal & Image Processing \n2. MobInstitute Level Electives Communication & Computing\n3. Artificial Intelligence & Soft Computing\n\nDepartment Level Electives\n1. Advance System Security & Digital Forensics\n2. Big Data & Analytics\n3. Robotics\n\nInstitute Level Electives\n1. Product Lifecycle Management\n2. Reliability Engineering\n3. Management Information System\n4. Design of Experiments\n5. Operation Research\n6. Cyber Security and Laws\n7. Disaster Management & Mitigation Measures\n8. Energy Audit and Management\n9. Development Engineering"

			elif sem ==8:
				return 	"Subjects For Semester 8:\n\n1. Human Machine Interaction\n2. Distributed Computing\n\n Department Level Electives\n1. High Performance Computing\n2. Natural Language Processing\n3. Adhoc Wireless Network\n\nInstitute Level Electives\n1. Project Management\n2. Finance Management\n3. Entrepreneurship Development and Management\n4. Human Resource Management\n5. Professional Ethics and CSR\n6. Research Methodology\n7. IPR and Patenting\n8. Digital Business Management\n9. Environmental Management"


	elif response["intentName"] == "placements":
		stats   = str(response["slots"]["stats"]).lower()

		if stats =="1" or stats =="general":
			return	"Vidyalankar Institute of Technology provides the best campus recruitment and has a well-trained program formulated for the students to prepare them for jobs at reputed organizations. The institute only aims to provide the market with the best of talent that would fit and fulfill the corporate world's needs. They have additional Training and Placement Cells exclusively for students that are run by experienced faculty."
		elif stats =="2" or stats == "statistics":
			return	"VIT, Mumbai has released the placement data of year 2018-2019.\n\n Check the placement data of the Institute for the year 2019 that includes number of students registered, number of students got placed, average salary offered, number of companies visited and some top recruiters.\n\n Number of companies participated - 11,\n Number of students registered -  770,\n Number of students got placed - 234,\n Average salary offered - 4.16 LPA"

		elif stats =="3" or stats == "top recruiters" or stats == "companies" or stats == "top companies":
			return	"Top Recuiters at VIT - Zeus Learning, Axis Bank, Nucsoft, Ugam Solutions, General Electric, TCS Ninja (Test), LTI, Justdial, MInstitute Level Electivess Software"
		
		elif stats =="4" or stats =="insights":
			return	"BE Computer Engineering at Vidyalankar Institute of Technology, Mumbai had the highest placement percentage of 79%,\n BE Biomedical Engineering at Vidyalankar Institute of Technology, Mumbai saw an increase in placements compared to previous year of 11%,\n BE Electronics Engineering has a placement percentage of 40%, and BE IT has a placement percentage of 78%"
		else:
			return	"Vidyalankar Institute of Technology provides the best campus recruitment and has a well-trained program formulated for the students to prepare them for jobs at reputed organizations. The institute only aims to provide the market with the best of talent that would fit and fulfill the corporate world's needs. They have additional Training and Placement Cells exclusively for students that are run by experienced faculty."
	
	

	elif response["intentName"] == "facilities":
		facility   = str(response["slots"]["facility"]).lower()

		if facility == "auditorium": 
			return "The College has an auditorium facility for the students where extracurricular activities, events, celebrations can be conducted."


		elif facility == "guest house": 
			return "VIT, Mumbai has a guest house inside the campus for the guests visiting the College for lectures, meetings, etc."

		elif facility == "gymkhana" or facility == "gym" or facility == "gymnasium" : 
			return "The College provides gym facility for the students with the latest machines. Students can make use of this facility to maintain their physical fitness."

		elif facility == "computer centre": 
			return "Computer centre of the College is equipped with latest hardware & software for the students."

		elif facility == "medical" or facility == "first aid": 
			return "The College provides medical facilities to the students and faculty. A doctor and a nurse are available for any emergency or first aid. The ambulance facility is also available at concessional rates."

		elif facility == "security" or facility == "surveillance": 
			return "The College has surveillance cameras installed in each building for the security of the students."

		elif facility == "hostel" or facility == "boys hostel" or facility == "girls hostel":
			return "A home away from home, for the benefit of OHU students, Vidyalankar has a private hostel facility (lodging only) with limited seats at Nerul, Navi Mumbai. Those interested may contact the hostel premises on 022 27704165 for checking availability and facilities."

		elif facility == "library" or facility == "college library":
			return "VIT has developed a central library which is a veritable treasure trove of knowledge, with more than 450 sq. m built up space and is stocked with text and reference books by reputed authors and well-known publishers. The Institute library has an organized collection of technical and management books (20000+ books), journals and e-journals."

		elif facility == "sports":
			return "The Institute has two multipurpose grounds that are used by students for outdoor sports and recreational activities and a Gymnasium for indoor sports. The grounds are suitable for popular sports such as football and cricket. There is also a multi-sports court which can be used for volleyball, basketball, etc. and a separate area is developed for badminton. Sports like Kabbadi, Kho-Kho, and athletics are organized in lush green grounds."

		elif facility == "cafeteria" or facility == "canteen":
			return "The Institute is committed to the provision of nutritious, high-quality and hygienic food to its members and constantly strives to identify avenues for improvement in its food services. There is access to wholesome food on the campus and the cafeteria and kitchen premises conform to high standards of cleanliness."

		elif facility == "wifi" or facility == "internet":
			return "Wi-fi provides a consistent, high quality connected experience, regardless of environmental factors. Wi-Fi setup for the entire Institute is controlled from the Data Center through firewall.Wi-Fi setup has over 30 access points strategically located across the Campus for access to Internet services. WiFi is authentication driven and is with restrictions as per user level for maximum security."

		elif facility == "infrastructure" or facility == "campus":
			return "Vidyalankar is not merely a technical institute; it is also a tech-savvy one. The Institute is equipped with IT infrastructure which meets industry standards. All possible steps are taken to ensure that it is constantly updated to offer the best of technology to our staff and students."

		elif facility == "laboratories" or facility == "labs" or facility == "computer labs":
			return "Institute has a dedicated laboratory with Apple iMac machines that allow students and faculty to work on Mac OS as well for the projects and creating digital content."

		elif facility == "store":
			return "The Institute has a well-stocked souvenir cum stationery store which sells Institute souvenirs and all stationery items required by students for routine academic needs. It provides photocopying facility as well."

		elif facility == "alumni":
			return "VIT Alumni association is the network where one alumni represents his/her batch and program of engineering. The alumni association managing committee is a subset of Alumni association."

		elif facility == "parking":
			return "The Institute campus has well-designated vehicle parking space. As per the parking rules, two-wheeled parking for students and four-wheeled parking for staff members is permitted. To encourage adherence to traffic rules and safe driving, students wearing helmets only are allowed to enter the campus to park their 2-wheeled vehicles. Students’ four-wheeled vehicles are allowed in the campus for drop and pick-up. A parking space is specially marked and designated for the physically challenged. Parking stickers and a parking plan are used for optimum utilization of parking space. The car parking arrangement is designed such that it aids in disaster management, should the need arise."

	elif response["intentName"] == "exams":
		year   = str(response["slots"]["year"]).lower()

		if year =="f.e." or year =="fe" or year =="f.e" or year =="first year" or year =="first" or year =="1":
			return "F.E exam schedule - https://vit.edu.in/images/downloads/exam/\nTT_R2019%20SEM1.pdf"

		elif year =="s.e." or year =="se" or year =="s.e" or year =="second year" or year =="second" or year =="2":
			return "Exams schedule not declared yet"

		elif year =="t.e." or year =="te" or year =="t.e" or year =="third year" or year =="third" or year =="3":
			return "Exams schedule not declared yet"

		elif year =="b.e." or year =="be" or year =="b.e" or year =="final year" or year =="final" or year =="4":
			return "Exams schedule not declared yet"

		elif year =="d.s.e." or year =="dse" or year =="d.s.e" or year =="direct second year" :
			return "D.S.E exam schedule - https://vit.edu.in/images/downloads/exam/\nTT_R2019_SEM3_DSE_April2021.pdf"


	return "Sorry! could not proccess the given input.. please try again."

