# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.template import RequestContext
from django.conf import settings
from cStringIO import StringIO
from random import choice
from PIL import Image
from lookbook.look.models import Look, LookUploadForm, LookColor
from util import ImageProcessing

def upload(request):
    color_dict = {9:"r", 8:"rp", 7:"p", 6:"pb", 5:"b", 4:"bg", 3:"g", 2:"gy", 1:"y", 0:"yr"}
    
    if request.method == 'GET':
        form = LookUploadForm()
        return render_to_response('looks/upload.html',
                                  {'form': form },
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        form = LookUploadForm(request.POST, request.FILES)    
        if form.is_valid():
            lookfile = request.FILES['look_photo']
            filename = settings.MEDIA_ROOT + '%s/%s' % ( 'looks', lookfile.name)
            #resize file
            resizedfile = resize_image(lookfile)
            #save to db
            look = form.save(commit=False)
            if len(form.data['look_description']) > 100:
                look.look_short_desc = form.data['look_description'][:97] + '...'
            else:
                look.look_short_desc = form.data['look_description']
            look.look_photo_path = filename
            look.look_photo_upload_IP_addr = get_client_ip(request)
            look.look_photo.save(filename, resizedfile)
            look.save()
            #upload file
            fd = open(filename, 'wb')
            for chunk in resizedfile.chunks():
                fd.write(chunk)
            fd.close()
            #detect img color
            colors = ImageProcessing.best_matched_colors(filename)
            for c in colors:
                color = LookColor()
                color.belong_to_look = look
                color.color_category = color_dict[c]
                color.red = 0
                color.green = 0
                color.blue = 0
                color.hue = 0
                color.save()
            
            #(red, green, blue) = average_image_color(filename)
            #color = LookColor()
            #color.belong_to_look = look
            #color.red = red
            #color.green = green
            #color.blue = blue
            #color.hue = hue
            #color.color_category = 'b' #choice(LookColor.COLOR_LIST)[0]
            #color.save()
            return HttpResponseRedirect(reverse('lookbook.look.views.detail', args=(look.id,)))
        else:
            return render_to_response('looks/upload.html',
                                      {'form': form},
                                      context_instance=RequestContext(request))

def resize_image(f):
    size = [500, 500]
    # create PIL Image instance
    image = Image.open(f)
    image.thumbnail(size)

    resized = StringIO()
    image.save(resized, image.format)
    resized.seek(0)

    return ContentFile(resized.getvalue())

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def average_image_color(filepath):
    img = Image.open(filepath)
    h = img.histogram()
    
    # split into red, green, blue
    r = h[0:256]
    g = h[256:256*2]
    b = h[256*2: 256*3]
    
    # perform the weighted average of each channel:
    # the *index* is the channel value, and the *value* is its weight
    return (
    sum( i*w for i, w in enumerate(r) ) / sum(r),
    sum( i*w for i, w in enumerate(g) ) / sum(g),
    sum( i*w for i, w in enumerate(b) ) / sum(b)
    )
    

