from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.views.decorators.http import require_http_methods

from .models import Gallery

import os 

# Create your views here.
def home(request):

    rq_old_input = ''

    if 'old_input' in request.session.keys():
        rq_old_input = request.session['old_input']

    context = {
        'rvalues': rq_old_input
    }

    if 'old_input' in request.session.keys():
       del request.session['old_input']

    return render(request, 'home.html')

@require_http_methods(["POST"])
def create(request):

    title = request.POST['title'].strip()
    description = request.POST['description'].strip()
    images  = request.FILES.getlist('images')

    if not title or not description or not images:
        request.session['old_input'] = request.POST
        messages.error(request, 'You need to fill all the necessary fields!')
        return redirect('home')

    for image in images:
        gallery = Gallery(
            title=title,
            description=description,
            image=image
        )
        gallery.save()

    messages.success(request, 'You just uploaded successfully!')
    return redirect('home')

def edit(request, pk):

    obj = get_object_or_404(Gallery, pk=pk)

    if request.method == 'POST':

        rq_image = Gallery.objects.get(pk=pk)

        update_image = get_object_or_404(Gallery, pk=pk)

        title = request.POST['title'].strip()
        description = request.POST['description'].strip()
        image  = request.FILES.get('image')

        if not title or not description:
            request.session['old_input'] = request.POST
            messages.error(request, 'You need to fill all the necessary fields!')
            return redirect('/edit/'+ pk)

        if image:

                # deleting old uploaded image.
                image_path = rq_image.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)

                update_image.title = title 
                update_image.description = description
                update_image.image = image
                update_image.save()

        else:
            update_image.title = title 
            update_image.description = description
            update_image.save()


        messages.success(request, 'You just edited successfully!')
        return redirect('image_list')

    
    rq_old_input = ''

    if 'old_input' in request.session.keys():
        rq_old_input = request.session['old_input']
    
    context = {
        'photo': obj,
        'rvalues': rq_old_input
    }

    if 'old_input' in request.session.keys():
       del request.session['old_input']

    return render(request, 'edit.html', context)

def image_list(request):

    photos = Gallery.objects.all()

    context = {
        'photos': photos
    }
    return render(request, 'list.html', context)

def gallery(request):

    photos = Gallery.objects.all()

    context = {
        'photos': photos
    }
    return render(request, 'gallery.html', context)

def delete(request, pk):

    obj = get_object_or_404(Gallery, pk=pk)

    # deleting old uploaded image.
    image_path = obj.image.path
    if os.path.exists(image_path):
        os.remove(image_path)

    obj.delete()

    messages.success(request, 'Ohh! You just deleted successfully!')
    return redirect('image_list')
