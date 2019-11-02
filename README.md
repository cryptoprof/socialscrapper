# socialscrapper
The main target of this project is to collect posts from different social networks pages and groups to database
install instructions:  
```
git clone https://github.com/cryptoprof/socialscrapper.git  
pip install -r requirments 
```
Rename file in **setting.py.sample**(folder scrappers) to **settings.py** and **specify your tokens**  
Run the server for testing:  
```
cd scrappers
python manage.py runserver
```
Go to http://127.0.0.1:8000/hello/ and it's will output data from test vk group.
![alt screen](https://raw.githubusercontent.com/cryptoprof/socialscrapper/master/2019-11-02_18-43-06.png)
