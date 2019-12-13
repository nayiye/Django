from django.shortcuts import render,redirect
from django.forms.forms import Form
from . import forms
from .models import *
from .models import *
from hashlib import md5
from django.db import transaction
from hashlib import md5
from django.http.response import HttpResponse,JsonResponse
from .models import User,Address
from cart.models import Cart


@transaction.atomic
def find_pass(request):

    param = request.POST

    type = request.POST.get("type")


    username = request.POST.get("username")


    key = request.POST.get("key")


    if type == "1":


        user = User.objects.filter(username=username).first()


        if user is None:
            return render(request, "findpass.html", {"msg": """您的账号不正确"""})



        if key != user.email:
            return render(request, "findpass.html", {"msg": "请使用注册时绑定的邮箱找回密码"})



        key_s = [str(a) for a in range(10)]

        key_s1 = [chr(a) for a in range(65, 92)]  # 大写

        key_s2 = [chr(a) for a in range(97, 123)]  # 小写

        key_s = key_s + key_s1 + key_s2



        import random


        password = random.choices(key_s, k=6)


        password = "".join(password)

        # 进行加密
        _password = md5(password.encode()).hexdigest()

        user.password = _password

        user.save()



        from django.core.mail import EmailMessage
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body = f"""尊敬的{username}，您于{now}找回密码，新密码是<span style="color:red;">{password}</span>,请登录后尽快修改密码，
                    以确保您的账户安全~
                    <br>
                    <br>
                    天天生鲜 祝您生活愉快！
                """

        message = EmailMessage(subject="天天生鲜-密码找回", body=body, to=(key,))
        message.content_subtype = "html"

        message.send()

        return redirect(to="/login")

    else:
        pass


@transaction.atomic
def register(request):
    user_form = forms.UserForm(request.POST)
    param = request.POST
    allow=request.POST.get("allow")
    username=request.POST.get("username")
    try:
        user=User.objects.get(username=username)
    except User.DoesNotExist:
        user=None
    if user:
        return render(request,"register.html",{"msg":"用户名已经存在"})
    if allow !="on":
        return render(request,"register.html",{"msg":"您需要同意协议"})
    if user_form.is_valid():
        user = user_form.instance
        m = md5(user.password.encode())
        user.password = m.hexdigest()
        user_form.save()
    return redirect(to="/index")

@transaction.atomic
def login(request):
    param=request.POST.dict()
    user=User.objects.filter(username=param.get("username")).first()
    if user is None:
        msg="用户不存在，请重新输入"
        return render(request,"login.html",{"msg":msg})
    m=md5(param.get("password").encode()).hexdigest()
    # password=User.objects.filter(password=m).first()
    if m != user.password:
        msg="密码输入错误，请重新登陆"
        return render(request,"login.html",{"msg":msg})
    # param['id']=User.objects.get(username=param["username"]).id
    # username=user.username
    request.session["username"]={"id":user.id,"username":user.username}
    id=request.session["username"].get("id")
    return redirect(to="/index")

def detail(request, id):
    comm = Commodity.objects.filter(id=id).first()
    type = comm.type

    reco=Commodity.objects.filter(type=type).all()
    reco=reco.exclude(id=id).all()[0:2]
    pk=0
    if request.session.get("username"):
        pk = request.session.get("username").get("id")
    data = Cart.objects.filter(user_id=pk).all()
    user_id = request.session.get("username").get("id")

    data = Cart.objects.filter(user_id=user_id).all()
    sum = 0
    if data != None :
        for i in data:
            sum += i.count


    # 获取Cookie 对象
    cookies = request.COOKIES

    # 遍历所有的cookie. 获取指定的Cookie
    value = ""
    for name , val in cookies.items() :
        if name == "goods_history" :
            value = val

    resp =  render(request, "detail.html", {"comm": comm, "comms": comm, "sum":sum ,"reco":reco})
    # 把 获取的所有的商品ID,在当前当前的商品ID
    if value != "":
        goods = set(value.split(","))
        goods.add(str(id))
        # 转成字符串
        value = ",".join(list(goods))
    else:
        value = f"{id}"

    # 存储到浏览器中
    resp.set_cookie("goods_history", value,  path="/")

    return resp


@transaction.atomic
def site(request):
    address=request.POST.get("address")
    tel = request.POST.get("tel")
    name = request.POST.get("name")
    postcode = request.POST.get("postcode")
    user_id= request.session.get("username").get("id")
    info=Address.objects.create(address=address,tel=tel,name=name,postcode=postcode,user_id=user_id)
    info.save()
    return redirect(to="/user_center_info")

def logout(request):
    request.session.flush()
    return redirect(to="/index")








