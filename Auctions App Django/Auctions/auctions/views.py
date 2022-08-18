
from unicodedata import category
from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from PIL import Image
from django.contrib.auth.decorators import login_required
from sqlalchemy import desc

from .models import *




def index(request):
    l = List.objects.all()
    list_of_lists = [ i for i in l]
    # print(list_of_lists)
    
    return render(request, "auctions/index.html",{
        "list_of_lists":list_of_lists
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "tag":"warning"
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "status":"warning"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "status":"warning"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def create(request):
    if request.method=="POST":
        user = request.user
        title= request.POST["title"]
        category=request.POST['category']
        image = request.POST["image"]
        description=request.POST["description"]
        starting_price=float(request.POST["starting_price"])
        if starting_price <= 0:
            return render(request,"auctions/create_list.html",{
                "message":"Please provide a valid Starting price",
                "status":"danger"
            })
        print(user,title,category,image,description,starting_price)
        list = List(owner=user,title=title,category=category,description=description,image_url=image,starting_bid=starting_price)
        print(list)
        list.save()
        return render(request,"auctions/create_list.html",{
            "message":"List have been saved successfully",
            "status":"success"
        })
        
    return render(request,"auctions/create_list.html")


#unfinshed
@login_required(login_url="login")
def category(request,category_name=None):
    if request.method=="POST":
        category_list = List.objects.all(category=category_name)
        return render(request,"auctions/sort_category",{
            "category_list":category_list
        })
    return render(request,"auctions/category.html")


#post to add list to watched list /// get to get user watched list
@login_required(login_url="login")
def watch(request,list_id=None):
    user = User.objects.get(id=request.user.id)
    return render(request,"auctions/watch.html",{
        "user_watched_list":user.watched_list.all()
    })


    # my_watched_list = List.objects.all(watched_list=request.user.id)
    # return render(request,"auctions/watch.html",{
    #     "my_watched_list":my_watched_list
    # })

#my list that i share it
@login_required(login_url="login")
def mylist(request):
    user = User.objects.get(id=request.user.id)
    user_shared_list = user.owned_list.all()
    return render(request,"auctions/mylist.html",{
        "user_list":user_shared_list
    })



@login_required(login_url="login")
def item(request,list_id,list_status=-4):
    message=None
    status=None
    try:
        list = List.objects.get(id=list_id)
    except:
        pass
    if list_id == -1:
        return render(request,"auctions/item.html",{
        "list":list,
        "message":"item added to your watched list",
        "status":"success"
    })
    if list_id == -2:
        return render(request,"auctions/item.html",{
        "list":list,
        "message":"item removed to your watched list",
        "status":"success"
    })
    if list_id == -3:
        return render(request,"auctions/item.html",{
        "list":list,
        "message":"something went wrong",
        "status":"warning"
    })

    if request.method == "POST":
        list = List.objects.get(id=list_id)
        aurthor = User.objects.get(id=request.user.id)
        bid = float(request.POST["bid"])
        # print(list.starting_bid)
        # print(bid)
    try:
        if bid > list.starting_bid:
            new_starting_bid=List.objects.get(id=list_id)
            new_starting_bid.starting_bid = bid
            new_starting_bid.save()
            print(new_starting_bid)
            update_bid=Bids(list=list,aurthor=aurthor,bid_offer=bid)
            update_bid.save()
            print(update_bid)
            message="Your bid have been update Successfully"
            status="success"
            
        else:
            message="Please provide a valid Bid"
            status="danger"
    except:
        message="Please provide a valid Bid"
        status="danger"
            
    
    list = List.objects.filter(id=list_id)
    return render(request,"auctions/item.html",{
        "list":list,
        "message":message,
        "status":status
    })
@login_required(login_url="login")
def comment(request,list_id):
    message=None
    status=None
    if request.method =="POST":
        list = List.objects.get(id=list_id)
        user = User.objects.get(id=request.user.id)
        comment = request.POST["comment"]
        comments_by_users = list.comments_have.all()
        if len(comment) > 64:
            message="Your comment is too long"  
            status = "danger"  
            return render(request,"auctions/comment.html",{
                "comments_by_users":comments_by_users,
                "list":list,
                "message":message,
                "status":status
                })

        list = List.objects.get(id=list_id)
        user = User.objects.get(id=request.user.id)
        #print(comment,user,list)
        add_comment=Comments(user=user,list=list,comments=comment)
        add_comment.save()
        message="You comment added Successfully"  
        status = "success"
    list = List.objects.get(id=list_id)
    # test=[1,2,3,4,5,6,7,8,9,12,21,2,3,4,5,6,7,3,2,1,3,4,5,5,5,5,5,55,5,5,5,5]
    comments_by_users = list.comments_have.all()
    return render(request,"auctions/comment.html",{
        "comments_by_users":comments_by_users,
        "list":list,
        "message":message,
        "status":status
    })

@login_required(login_url="login")
def category_sort(request,category_kind=None):
    list_by_category = List.objects.filter(category=category_kind)
    
    return render(request,"auctions/category_sort.html",{
        "list_by_category":list_by_category,
        "category_name":category_kind
    })

@login_required(login_url="login")
def put_to_watch_list(request,list_id):
    if request.method =="POST":
        try:
            user = User.objects.get(id = request.user.id)
            item = List.objects.get(id=list_id)
            if item  in user.watched_list.all():
                user.watched_list.remove(item)
                return HttpResponseRedirect(reverse('item', kwargs={'list_id':list_id }))
            else:
                user.watched_list.add(item)
                return HttpResponseRedirect(reverse('item', kwargs={'list_id': list_id}))
        except:
            return HttpResponseRedirect(reverse('item', kwargs={'list_id': list_id}))


