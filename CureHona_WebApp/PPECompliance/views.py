from django.shortcuts import render, redirect
import os
# from PIL import Image, ImageOps
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from CureHona_WebApp import settings
from django.views import View
from django.contrib.auth.decorators import login_required
# from .tasks import SendImageToServer
from .Code.PPE_ObjectDetector import PPE_ObjectDetector
import time
import threading
from django.http import JsonResponse

from datetime import datetime


#################### Authentication  ################

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = Users()
            user.username = form.cleaned_data.get('username')
            user.password = form.cleaned_data.get('password1')
            user.save()
            request.session['user'] = user.pk_user
            request.session['username'] = user.username
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, 'PPECompliance/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        # model_name = request.POST['model_type']

        try:
            user = Users.objects.get(username=username)
            if user.password == password:
                request.session['user'] = user.pk_user
                request.session['username'] = user.username
                model_redirect_url = 'home_page_ppe'
                # request.session['model_type'] = model_name

                return redirect(model_redirect_url)
            else:
                print("Login Failed - Password don't match")
                return render(request, 'registration/login.html')

        except Exception as e:
            print(e)
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


def user_logout(request):
    try:
        del request.session['user']
        del request.session['username']
        del request.session['model_type']
        del request.session['current_uploaded_image']
        # for key in request.session.keys():
        #     del request.session[key]
    except Exception as e:
        print('--------', e)
    finally:
        request.session.modified = True

    return redirect('login')


def auth_check(request):
    if request.session.has_key('user'):
        return True
    else:
        return False


#################### Main #########################

class UploadImage(View):
    template_name = 'PPECompliance/upload_image.html'

    def get(self, request):
        if auth_check(request):
            return render(request, self.template_name)

        return redirect("login")

    def post(self, request):

        if auth_check(request):

            # Fetching all Images from the client side
            images = request.FILES.getlist('img')

            object_detector = PPE_ObjectDetector()
            object_detector.read_graph(settings.PPECompliance_Model_Path)

            current_uploaded_image = []
            active_prop = ImagesPropertiesTypes.objects.get(key='image_processed')
            model_type = Models.objects.get(type='mobilenet_ssd_v2_coco')

            for image in images:
                image_object = Images()
                image_object.image = image
                image_object.fk_user_id = request.session['user']
                image_object.fk_model = model_type
                image_object.created = datetime.now()
                image_object.save()
                PPE_compliance_dir = "media/{}/PPE/{}".format(request.session['username'], image_object.pk_image)
                if not os.path.exists(PPE_compliance_dir):
                    os.makedirs(PPE_compliance_dir)

                ppe_compliance_object = PPECompliances()
                ppe_compliance_object.fk_image = image_object
                ppe_compliance_object.created = datetime.now()
                ppe_compliance_object.save()
                # t = threading.Thread(target=object_detector.preprocess_image, args=(str(ppe_compliance_object.pk_ppe_compliance),))
                # t.start()

                result_filename = object_detector.preprocess_image(str(ppe_compliance_object.fk_image.image))

                ppe_compliance_object.result_image = result_filename
                ppe_compliance_object.save()

                image_prop = ImagesProperties(fk_image=image_object, fk_image_property_type=active_prop, value='True')
                image_prop.save()

                current_uploaded_image.append(image_object.pk_image)

            request.session['current_uploaded_image'] = current_uploaded_image
            return redirect("show_all_images_ppe")

        return redirect('login')


def gallery(request):
    if auth_check(request):
        active_prop = ImagesPropertiesTypes.objects.get(key='image_processed')
        active_images = ImagesProperties.objects.filter(fk_image__fk_user=request.session['user'],
                                                          fk_image_property_type=active_prop, value='True',
                                                          fk_image__fk_model__type='mobilenet_ssd_v2_coco')
        print(active_images)
        allImages = PPECompliances.objects.filter(fk_image__in=[im.fk_image for im in active_images]).order_by(
            '-pk_ppe_compliance')
        return render(request, "PPECompliance/gallery.html", {'Images': allImages})

    return redirect('login')


def ShowAllImages(request):
    if auth_check(request):
        active_prop = ImagesPropertiesTypes.objects.get(key='image_processed')
        active_images = ImagesProperties.objects.filter(fk_image__fk_user=request.session['user'],
                                                          fk_image_property_type=active_prop, value='True',
                                                          fk_image__fk_model__type='mobilenet_ssd_v2_coco',
                                                          fk_image__pk_image__in=request.session[
                                                              'current_uploaded_image'])
        print(active_images)
        allImages = PPECompliances.objects.filter(fk_image__in=[im.fk_image for im in active_images])

        return render(request, "PPECompliance/show_image.html", {"allImages": allImages})

    return redirect('login')


def delete_image_list(request, id, url):
    if auth_check(request):
        active_prop = ImagesPropertiesTypes.objects.get(key='image_processed')
        imageList = ImagesProperties.objects.get(fk_image_id=id, fk_image_property_type=active_prop)
        if 'current_uploaded_image' in request.session:
            if id in request.session['current_uploaded_image']:
                request.session['current_uploaded_image'].remove(id)
                request.session.modified = True
        imageList.value = False
        imageList.save()
        return redirect(url)

    return redirect('login')


def delete_all_image(request):
    if auth_check(request):
        imageList = ImagesProperties.objects.filter(fk_image__fk_user=request.session['user'],
                                                      fk_image__fk_model__type='mobilenet_ssd_v2_coco')
        if 'current_uploaded_image' in request.session:
            del request.session['current_uploaded_image']
            request.session.modified = True
        for image in imageList:
            image.value = False
            image.save()
        return redirect("gallery_ppe")

    return redirect('login')








