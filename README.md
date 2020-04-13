### CureHona



# Prequisites - Python 3.5+
1. Install Pip - sudo apt install python3-pip
2. git clone this respository
3. create a virtual environment and activate it
4. Install all the required dependencies and libraries - pip3 install -r requirements.txt
5. Install dlib : 
    $ sudo apt-get install build-essential cmake
    $ sudo apt-get install libgtk-3-dev
    $ sudo apt-get install libboost-all-dev

# Prequisites CureHone_WebApp - Postgres, Django Server
1. sudo apt install postgresql 
2. It is necessary that you execute the commands below and create a user:
      1.  sudo su - postgres 
      2. postgres@ubuntu:~$ psql 
      3. postgres=# create role <username> with password '<password>' createdb login;
    
## Object Detection & Tracking : 
1. cd CureHone
2. configure the inference_graph file path, video-file path and track-length in Config/Main_Config.ini file
3. For running Object Detection on images present inside data directory, run : python3 Main_tf2.py
4. For running Object Detection & Tracking on the configured video_path/camera path run : python3 Main_tf_video.py

## CureHona WebApp :
1. cd revisions
2. createdb code19
3. psql -d code19 -f 0001.sql
4. cd CureHona_WebApp
5. python3 manage.py makemigrations
6. python3 manage.py migrate
7. python3 manage.py runserver

After running all the above mentioned commands, you will be able to access the webapp in your browser,
Go to the url : http://127.0.0.1:8000
The webapp is created for easy demo purpose of object detector code, where a user can sign-in and upload multiple images to the server, where object detection will be done on them and resultant images with roi drawn will be saved and returned back to the user.

# DB Schema : 

![image](https://user-images.githubusercontent.com/21499789/79097322-1a121c80-7d7d-11ea-931c-b6f778d64479.png)

# Screenshots : 

