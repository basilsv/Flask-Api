Greetings Hiring Team

Notes

1. I have used port 7000 just as to avoid a conflict there seemed to be some process kept interrupting my session So the sample link on running is :

http://127.0.0.1:7000/api/posts
http://127.0.0.1:7000/api/ping
http://127.0.0.1:7000/api/posts?tags=science,tech
http://127.0.0.1:7000/api/posts?tags=science,tech&sortBy=reads&direction=desc

2.The version of python is Python 3.8.3. I have added a requirement txt but basically only

Pip install flask
Pip install requests

Rest should be included in python library

Thanks for the challenge it was fun.

3. To run the server just use 'python flask_api.py'

4. I used a virtual env so steps for that are before installing requirements.txt as below:

1. virtualenv [name]
2. source [name]/bin/activate
3. python flask_api.py
4. Check API
5. Deactivate