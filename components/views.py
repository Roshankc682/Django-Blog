from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from components.forms import BloggersForm
from components.models import Bloggers
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import re
import os
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.db import connection
import hashlib
import html
import html.parser
import base64
from django.core.files.storage import FileSystemStorage
from mimetypes import MimeTypes
import os.path
from PIL import Image
import PIL
import random
import glob



# Create your views here.
def index_page(request):
    # This will check whether true or false
    session_key = request.session.has_key('is_loogged_as_user')
    if request.session.has_key('is_loogged_as_user'):
        uid_name_of_user_logged = request.session['uid_name_of_user_logged']
        name_of_user = request.session['name']

        pass_uid_serial_no = 1
        wordFreqDic_iid = {}
        wordFreqDic_title = {}
        wordFreqDic_blog_post = {}
        wordFreqDic_uiid_name = {}
        wordFreqDic_date = {}

        Bloggers_ = Bloggers.objects.all()
        # print("==============================This is start=================================================")
        for Bloggers_check in Bloggers_:
            # print(Bloggers_check.uid_name)
            uid_name_of_user_to_print_data = Bloggers_check.uid_name
            # print(uid_name_of_user_to_print_data)
            # print(wordFreqDic_uid_of_all)
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {uid_name_of_user_to_print_data};')
                for row in cursor.fetchall():
                    # print(row[0])
                    # print(row[1])
                    # print(row[2])
                    # print(row[3])
                    # print(row[5])
                    base64_bytes_ = row[1].encode('ascii')
                    title_bytes_ = base64.b64decode(base64_bytes_)
                    decoded_title = title_bytes_.decode('ascii')

                    base64_bytes__ = row[2].encode('ascii')
                    blog_bytes_ = base64.b64decode(base64_bytes__)
                    decoded_blog = blog_bytes_.decode('ascii')

                    wordFreqDic_iid.update({f'blogging_{pass_uid_serial_no}': row[0]})
                    wordFreqDic_title.update({f'blogging_{pass_uid_serial_no}': decoded_title})
                    wordFreqDic_blog_post.update({f'blogging_{pass_uid_serial_no}': decoded_blog})
                    wordFreqDic_uiid_name.update({f'blogging_{pass_uid_serial_no}': row[3]})
                    wordFreqDic_date.update({f'blogging_{pass_uid_serial_no}': row[5]})
                    pass_uid_serial_no = pass_uid_serial_no + 1;
        # print(wordFreqDic_iid)
        # print(wordFreqDic_title)
        # print(wordFreqDic_blog_post)
        # print(wordFreqDic_date)
        # print(wordFreqDic_uiid_name)
        # print("====================This is end===========================================================")
        return render(request, "index.html", {'session_key': session_key,'name_of_user':name_of_user,'iid_post': sorted(wordFreqDic_iid.items()),'title_': sorted(wordFreqDic_title.items()),'blog_post': sorted(wordFreqDic_blog_post.items()),'uiid_name': sorted(wordFreqDic_uiid_name.items()),'data_post': sorted(wordFreqDic_date.items())})
        # return render(request, "index.html")
    else:
        pass_uid_serial_no = 1
        wordFreqDic_iid = {}
        wordFreqDic_title = {}
        wordFreqDic_blog_post = {}
        wordFreqDic_uiid_name = {}
        wordFreqDic_date = {}

        Bloggers_ = Bloggers.objects.all()
        # print("==============================This is start=================================================")
        for Bloggers_check in Bloggers_:
            # print(Bloggers_check.uid_name)
            uid_name_of_user_to_print_data = Bloggers_check.uid_name
            # print(uid_name_of_user_to_print_data)
            # print(wordFreqDic_uid_of_all)
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {uid_name_of_user_to_print_data};')
                for row in cursor.fetchall():
                    # print(row[0])
                    # print(row[1])
                    # print(row[2])
                    # print(row[3])
                    # print(row[5])
                    base64_bytes_ = row[1].encode('ascii')
                    title_bytes_ = base64.b64decode(base64_bytes_)
                    decoded_title = title_bytes_.decode('ascii')

                    base64_bytes__ = row[2].encode('ascii')
                    blog_bytes_ = base64.b64decode(base64_bytes__)
                    decoded_blog = blog_bytes_.decode('ascii')

                    wordFreqDic_iid.update({f'blogging_{pass_uid_serial_no}': row[0]})
                    wordFreqDic_title.update({f'blogging_{pass_uid_serial_no}': decoded_title})
                    wordFreqDic_blog_post.update({f'blogging_{pass_uid_serial_no}': decoded_blog})
                    wordFreqDic_uiid_name.update({f'blogging_{pass_uid_serial_no}': row[3]})
                    wordFreqDic_date.update({f'blogging_{pass_uid_serial_no}': row[5]})
                    pass_uid_serial_no = pass_uid_serial_no + 1;
        # print(wordFreqDic_iid)
        # print(wordFreqDic_title)
        # print(wordFreqDic_blog_post)
        # print(wordFreqDic_date)
        # print(wordFreqDic_uiid_name)
        # print("====================This is end===========================================================")
        return render(request, "index.html", {'iid_post': sorted(wordFreqDic_iid.items()),
                                              'title_': sorted(wordFreqDic_title.items()),
                                              'blog_post': sorted(wordFreqDic_blog_post.items()),
                                              'uiid_name': sorted(wordFreqDic_uiid_name.items()),
                                              'data_post': sorted(wordFreqDic_date.items())})
        # return render(request, "index.html")
def register(request):
    if request.session.has_key('is_loogged_as_user'):
        return redirect("/dashboard")
    else:
        return render(request, "register.html")

def register_add(request):
    if request.method == "POST":
        email = request.POST['email']
        uname = request.POST['name']
        table_name_as_per_hash_username = hashlib.sha256(str(f"{email}").encode('utf-8')).hexdigest()
        user_folder = 'static/' + f"{table_name_as_per_hash_username}"
        if not os.path.exists(user_folder):
            os.mkdir(user_folder)
        password_ = request.POST['password']
        repeat_password_ = request.POST['repeat_password']
        hashed_pwd = make_password(password_)
        # check the repeat_password and password are same
        length_of_password = len(password_)
        # if (length_of_password <= 7):
        #     messages.add_message(request, messages.ERROR, 'Password must be at Leat 7 character')
        #     return redirect("/register")
        #     exit()

        # check username only contains characters
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if (regex.search(uname) == None):
            print("Username is accepted")
        else:
            print("Username is not accepted.")
            messages.add_message(request, messages.ERROR, 'Username should only contains character')
            return redirect("/register")
            exit()
        if (password_ != repeat_password_):
            # print("The password is not same")
            messages.add_message(request, messages.ERROR, 'Password and Repeat password are not same')
            return redirect("/register")
            exit()
        Bloggers_ = Bloggers.objects.all()
        for Bloggers_check in Bloggers_:
            print(Bloggers_check.eemail)
            if (Bloggers_check.ename == uname):
                # print('name taken')
                messages.add_message(request, messages.ERROR, 'Username Already taken')
                return redirect("/register")
                exit()

            if (Bloggers_check.eemail == email):
                # print('name taken')
                messages.add_message(request, messages.ERROR, 'Email Already used')
                return redirect("/register")
                exit()
        ins = Bloggers(ename=uname,eemail=email,password=hashed_pwd,uid_name=table_name_as_per_hash_username)
        # print(ins)
        ins.save()
        # This will create a table of username to save blog
        # print(table_name_as_per_hash_username)
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE TABLE `{table_name_as_per_hash_username}` (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, tittle VARCHAR(300) NOT NULL, blog_content VARCHAR(30000) NOT NULL, udi_name VARCHAR(500) NOT NULL, time_first VARCHAR(50), time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);')
        # return render(request,"register.html",{'Bloggers_':Bloggers_})
        messages.add_message(request, messages.ERROR, 'Succesfully created account')
        return redirect("/register")

    else:
        return redirect("/register")


def login(reqeust):
    if reqeust.session.has_key('is_loogged_as_user'):
        return redirect("/dashboard")
    else:
        return render(reqeust, "login.html")

def login_data_check(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # print(email)
        # print(password)
        Bloggers_ = Bloggers.objects.all()
        for Bloggers_check in Bloggers_:
            print(Bloggers_check.eemail)
            if(Bloggers_check.eemail == email):
                print("---------------The matched email-------------------")
                print("Email matched")
                print(Bloggers_check.eemail)
                print("----------------------------------")
                # unhasing password
                password_unhashed_true_or_false = check_password(password, Bloggers_check.password)  # returns True
                if (password_unhashed_true_or_false):
                    print("The password matched")
                    request.session['is_loogged_as_user'] = Bloggers_check.eemail
                    request.session['uid_name_of_user_logged'] = Bloggers_check.uid_name
                    request.session['logged_email'] = email
                    request.session['name'] = Bloggers_check.ename
                    return redirect("/dashboard")
                    exit()
    else:
        messages.add_message(request, messages.ERROR, 'Invalid credentials')
        return redirect("/login")
        exit()
    messages.add_message(request, messages.ERROR, 'Invalid credentials')
    return redirect("/login")
    exit()
def dashboard_user(request):
    if request.session.has_key('is_loogged_as_user'):
        uid_name_of_user_logged = request.session['uid_name_of_user_logged']
        image_name_in_list = os.listdir(f'static/{uid_name_of_user_logged}')

        print(type(image_name_in_list))
        pass_image_name = 1
        wordFreqDic_image_thing = {}
        for i in image_name_in_list:
            # print(i)
            wordFreqDic_image_thing.update({f'image_{pass_image_name}': i})
            pass_image_name = pass_image_name + 1;
        # print(wordFreqDic_image_thing)

        session_key = request.session.has_key('is_loogged_as_user')
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM blog WHERE uid_name="{uid_name_of_user_logged}";')
            for row in cursor.fetchall():
                image_name = row[5]
                # print(row[5])
        print("=======================This is name of user=========================")
        logged_email = request.session['logged_email']
        # print(logged_email)
        # print(uid_name_of_user_logged)
        # print("================================================")
        # Dictionary of strings and ints
        wordFreqDic_post = {}
        wordFreqDic_title = {}
        wordFreqDic_unique_id = {}
        # print(wordFreqDic)
        first = 1
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM `{uid_name_of_user_logged}`;')
            for row in cursor.fetchall():
                # print("================This is row data=========")
                # print(row[1])
                # print(row[2])
                base64_bytes = row[2].encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                message_post = message_bytes.decode('ascii')
                # print(message_post)

                unique_id = row[0]

                base64_bytes_ = row[1].encode('ascii')
                message_bytes_ = base64.b64decode(base64_bytes_)
                message_title = message_bytes_.decode('ascii')
                # print(message_title)
                wordFreqDic_post.update({f"{first}": message_post})
                wordFreqDic_title.update({f"{first}": message_title})
                wordFreqDic_unique_id.update({f"{first}": unique_id})
                # print(text_print_after_unescape)
                first = first + 1;
                # print("================This is row data=========")
        # print("=======================This is the user blog data===========================")
        # wordFreqDic.update({"session_key": session_key})
        # print(wordFreqDic)
        # print(wordFreqDic_unique_id)
        # print("============================================================================")
        # return render(request, "dashboard.html",{'data': sorted(wordFreqDic.items())})
        name_of_user = request.session['name']
        # print(name_of_user)
        return render(request, "dashboard.html", {'session_key': session_key,'logged_email':logged_email,'data_post': sorted(wordFreqDic_post.items()),'data_title': sorted(wordFreqDic_title.items()),'data_uid': sorted(wordFreqDic_unique_id.items()),'data_image_name': sorted(wordFreqDic_image_thing.items()),'name_of_user' : name_of_user,'image_name':image_name,'uid_name_of_user_logged':uid_name_of_user_logged})
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    messages.error(request,"Logged out")
    return redirect("/")


def blog_user_saved(request):
    if request.method == "POST":
        print("================================================")
        textarea_to_save = request.POST['textarea_to_save']
        textarea_to_save_title = request.POST['Title_of_post']

        textarea_to_save_title = textarea_to_save_title.encode('ascii')
        textarea_to_save_title = base64.b64encode(textarea_to_save_title)
        textarea_to_save_title = textarea_to_save_title.decode('ascii')

        # print(textarea_to_save)
        message_bytes = textarea_to_save.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_content = base64_bytes.decode('ascii')
        uid_name_of_user_logged = request.session['uid_name_of_user_logged']
        # print(uid_name_of_user_logged)
        print(textarea_to_save)
        with connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO `{uid_name_of_user_logged}` (tittle , blog_content , udi_name)VALUES ("{textarea_to_save_title}", "{base64_content}", "{uid_name_of_user_logged}");')

        print("===================the unescape character is=============================")
        # text_print_after_unescape  =  html.parser.HTMLParser().unescape(textarea_to_save)
        # print(text_print_after_unescape)
        return redirect("/write_a_blog")
    else:
        print("the request is get")
        return redirect("/dashboard")
    return redirect("/dashboard")

def Read_more_by_user(request):
    if request.method == "GET":
        post_id = request.GET['post_id']
        # print(post_id)
        session_key = request.session.has_key('is_loogged_as_user')
        uid_name_of_user_logged = request.session['uid_name_of_user_logged']
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM blog WHERE uid_name="{uid_name_of_user_logged}";')
            for row in cursor.fetchall():
                image_name = row[5]
                # print("=======asdklfaklsdf="+image_name+"==========")
        wordFreqDic_post = {}
        wordFreqDic_title = {}
        first = 1
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {uid_name_of_user_logged} WHERE id={post_id};')
            for row in cursor.fetchall():
                # print(row[1])
                time_time = row[5]

                base64_bytes = row[2].encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                message_post = message_bytes.decode('ascii')
                # print(message_post)
                base64_bytes_ = row[1].encode('ascii')
                message_bytes_ = base64.b64decode(base64_bytes_)
                message_title = message_bytes_.decode('ascii')
                # print(message_title)
                wordFreqDic_post.update({f"{first}": message_post})
                wordFreqDic_title.update({f"{first}": message_title})
                # print(text_print_after_unescape)
                first = first + 1;
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM blog;')
            for row in cursor.fetchall():
                if(uid_name_of_user_logged == row[4]):
                    print("=====")
                    read_more_name = row[1]
                    read_more_email = row[2]
                    read_more_img = row[5]
                    print("=====")
        return render(request, "read_more.html",{'uid_name_of_user_logged' : uid_name_of_user_logged,'data_post': sorted(wordFreqDic_post.items()),'data_title': sorted(wordFreqDic_title.items()),'session_key': session_key,'post_id': post_id,'read_more_name':read_more_name,'read_more_email':read_more_email,'image_name':image_name,'time_time':time_time})
    # else:
    #     return redirect("/dashboard")

        # return render(request, "read_more.html")
    else:
        return redirect("/dashboard")


def upload_profile_pic(request, template_name="dashboard.html"):
    if request.session.has_key('is_loogged_as_user'):
        if request.method == "POST":
            uid_name_of_user_logged = request.session['uid_name_of_user_logged']
            img_details = request.FILES['img']
            # print(img_details.name)
            # print(img_details.size)
            # img_details.name = uid_name_of_user_logged
            fs = FileSystemStorage()
            filter_extension = os.path.splitext(img_details.name)
            fs = FileSystemStorage()
            print(filter_extension[-1])
            if(filter_extension[-1] == ".jpg" or filter_extension[-1] == ".png" or filter_extension[-1] == ".jpeg" or filter_extension[-1] == ".gif"):
                print("yes")
                with connection.cursor() as cursor:
                    cursor.execute(f'UPDATE blog SET img = "{img_details.name}" WHERE uid_name = "{uid_name_of_user_logged}"')
                messages.error(request, "Uploaded successfully")
                # with connection.cursor() as cursor:
                #     cursor.execute(f'SELECT * FROM blog WHERE uid_name="{uid_name_of_user_logged}";')
                #     for row in cursor.fetchall():
                        # print(row[5])
                        # if os.path.exists("image_for_blog/"+row[5]):
                        #     print("\nIt is a normal file")
                        # else:
                        #     print("Not Not Not")
                        # if(os.remove("image_for_blog/"+row[5])):
                        #     os.remove("image_for_blog/"+row[5])
                        # else:
                        #     print("no no no no no")
                fs.save(img_details.name, img_details)
            else:
                print("sorry")
                messages.error(request, "Invalid file")
            return redirect("/settings")
        else:
            return redirect("/settings")
    else:
        return redirect("/")

def Delete(request):
    if request.session.has_key('is_loogged_as_user'):
        if request.method == "POST":
            id_details = request.POST['post_id']
            # print(type(id_details))
            print("-=====================")
            id_details = int(id_details)
            print(id_details)
            print("-=====================")
            uid_name_of_user_logged = request.session['uid_name_of_user_logged']
            # print(uid_name_of_user_logged)
            with connection.cursor() as cursor:
                cursor.execute(f'DELETE FROM {uid_name_of_user_logged} WHERE id = {id_details};')
            messages.error(request, "Blog Deleted")
            return redirect("/dashboard")
        else:
            return redirect("/dashboard")
    else:
        return redirect("/dashboard")

def Edit(request):
    if request.session.has_key('is_loogged_as_user'):
        session_key = request.session.has_key('is_loogged_as_user')
        uid_name_of_user_logged = request.session['uid_name_of_user_logged']
        post_id = request.POST['post_id']
        print(post_id)
        wordFreqDic_post = {}
        wordFreqDic_title = {}
        first = 1
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {uid_name_of_user_logged} WHERE id={post_id};')
            for row in cursor.fetchall():
                # print(row[0])
                base64_bytes = row[2].encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                message_post = message_bytes.decode('ascii')
                # print(message_post)
                base64_bytes_ = row[1].encode('ascii')
                message_bytes_ = base64.b64decode(base64_bytes_)
                message_title = message_bytes_.decode('ascii')
                # print(message_title)
                wordFreqDic_post.update({f"{first}": message_post})
                wordFreqDic_title.update({f"{first}": message_title})
                # print(text_print_after_unescape)
                first = first + 1;
        return render(request, "edit_blog.html", {'uid_name_of_user_logged': uid_name_of_user_logged,
                                                  'data_post': sorted(wordFreqDic_post.items()),
                                                  'data_title': sorted(wordFreqDic_title.items()),
                                                  'session_key': session_key, 'post_id': post_id})

        # return render(request, "edit_blog.html",{'session_key': session_key})
    else:
        return redirect("/dashboard")


def finally_edited(request):
    if request.session.has_key('is_loogged_as_user'):
        uid_name_of_user_logged = request.session['uid_name_of_user_logged']
        session_key = request.session.has_key('is_loogged_as_user')
        textarea_to_save = request.POST['textarea_to_save']
        textarea_to_save_title = request.POST['Title_of_post']
        post_id = request.POST['post_id']
        # print(textarea_to_save)
        # print(textarea_to_save_title)

        textarea_to_save_title = textarea_to_save_title.encode('ascii')
        textarea_to_save_title = base64.b64encode(textarea_to_save_title)
        textarea_to_save_title = textarea_to_save_title.decode('ascii')
        print("================================================")
        print(textarea_to_save_title)
        print("================================================")

        message_bytes = textarea_to_save.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_content = base64_bytes.decode('ascii')
        print("================================================")
        print(base64_content)
        print("================================================")
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE {uid_name_of_user_logged} SET tittle = "{textarea_to_save_title}" , blog_content = "{base64_content}" , udi_name = "{uid_name_of_user_logged}"  WHERE id = {post_id} ')
        messages.error(request, "Edited succesfully")
        return redirect("/dashboard")

    else:
        return redirect("/dashboard")


def upload_profile_media(request):
    if request.session.has_key('is_loogged_as_user'):
        if request.method == "POST":
            uid_name_of_user_logged = request.session['uid_name_of_user_logged']
            img_details = request.FILES['img']
            # img_details.name = uid_name_of_user_logged+"test"
            # print(img_details.name)
            # print(img_details.size)
            # fs = FileSystemStorage()
            # fs.save(img_details.name,img_details)
            img = request.FILES['img']
            img_extension = os.path.splitext(img.name)[1]

            filter_extension = os.path.splitext(img_details.name)
            print(filter_extension[-1])
            if (filter_extension[-1] == ".jpg" or filter_extension[-1] == ".png" or filter_extension[-1] == ".jpeg" or
                    filter_extension[-1] == ".gif"):
                    user_folder = 'static/' + f"{uid_name_of_user_logged}"
                    if not os.path.exists(user_folder):
                        os.mkdir(user_folder)

                    # creating a image object (main image)
                    im1 = Image.open(request.FILES['img'])
                    # save a image using extension
                    n = random.randint(0,1000)
                    n = str(n)
                    im1 = im1.save(fr"static\{uid_name_of_user_logged}\{n + img_extension}")
                    messages.error(request, "uploaded succesfully")
                    return redirect("/media")
            else:
                print("sorry invalid format")
                messages.error(request, "Invalid file")
                return redirect("/media")
        else:
            return redirect("/media")


def delete_image(request):
    if request.session.has_key('is_loogged_as_user'):
        if request.method == "POST":
            name_of_image = request.POST['name_of_image']
            uid_name_of_user_logged = request.session['uid_name_of_user_logged']
            print(name_of_image)
            os.remove("static/"+uid_name_of_user_logged+"/"+name_of_image)
            messages.error(request, "File Deleted")
            return redirect("/media")
        else:
            return redirect("/media")

def readmore_details_blog(request):
    if request.session.has_key('is_loogged_as_user'):
        session_key = request.session.has_key('is_loogged_as_user')
        post_id = request.GET['post_id']
        post_uid = request.GET['post_uid']
        wordFreqDic_post = {}
        wordFreqDic_title = {}
        first = 1
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM blog WHERE uid_name="{post_uid}";')
            for row in cursor.fetchall():
                image_name = row[5]
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM blog;')
            for row in cursor.fetchall():
                if(post_uid == row[4]):
                    print("=====")
                    read_more_name = row[1]
                    read_more_email = row[2]
                    read_more_img = row[5]
                    print("=====")
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {post_uid} WHERE id={post_id};')
            for row in cursor.fetchall():
                time_time = row[5]

                base64_bytes = row[2].encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                message_post = message_bytes.decode('ascii')
                # print(message_post)
                base64_bytes_ = row[1].encode('ascii')
                message_bytes_ = base64.b64decode(base64_bytes_)
                message_title = message_bytes_.decode('ascii')
                # print(message_title)
                wordFreqDic_post.update({f"{first}": message_post})
                wordFreqDic_title.update({f"{first}": message_title})
                # print(text_print_after_unescape)
                first = first + 1;
        return render(request, "read_more_.html", {'session_key': session_key,'data_post': sorted(wordFreqDic_post.items()),
                           'data_title': sorted(wordFreqDic_title.items()),'read_more_name':read_more_name,'read_more_email':read_more_email,'image_name':image_name,'time_time':time_time})
    else:
        post_id = request.GET['post_id']
        post_uid = request.GET['post_uid']
        wordFreqDic_post = {}
        wordFreqDic_title = {}
        first = 1
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM blog WHERE uid_name="{post_uid}";')
            for row in cursor.fetchall():
                image_name = row[5]
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM blog;')
            for row in cursor.fetchall():
                if(post_uid == row[4]):
                    print("=====")
                    read_more_name = row[1]
                    read_more_email = row[2]
                    read_more_img = row[5]
                    print("=====")
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {post_uid} WHERE id={post_id};')
            for row in cursor.fetchall():
                time_time = row[5]

                base64_bytes = row[2].encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                message_post = message_bytes.decode('ascii')
                # print(message_post)
                base64_bytes_ = row[1].encode('ascii')
                message_bytes_ = base64.b64decode(base64_bytes_)
                message_title = message_bytes_.decode('ascii')
                # print(message_title)
                wordFreqDic_post.update({f"{first}": message_post})
                wordFreqDic_title.update({f"{first}": message_title})
                # print(text_print_after_unescape)
                first = first + 1;
            return render(request, "read_more_.html",
                          {'data_post': sorted(wordFreqDic_post.items()),
                           'data_title': sorted(wordFreqDic_title.items()),'read_more_name':read_more_name,'read_more_email':read_more_email,'image_name':image_name,'time_time':time_time})
    redirect("/")