from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=100,null=False,verbose_name="用户名",unique=True)
    password=models.CharField(max_length=100,null=False,verbose_name="密码")
    # tel=models.CharField(max_length=13,verbose_name="手机号")
    # address=models.CharField(max_length=100,verbose_name="联系地址")
    email=models.EmailField(verbose_name="邮箱",null=True,blank=True)
    class Meta:
        db_table="t_user"



class Address(models.Model):
    address=models.CharField(verbose_name="收货地址",max_length=100,null=False)
    tel = models.CharField(verbose_name="手机号", null=False, blank=True, max_length=11)
    name=models.CharField(verbose_name="收件人",null=False,blank=True,max_length=100)
    postcode= models.CharField(verbose_name="邮编", null=False, blank=True, max_length=100)
    # postcode=models.CharField(verbose_name='邮编',null=False,blank=True,max_length=10)
    user=models.ForeignKey(to=User,on_delete=models.CASCADE,blank=True,related_name="add")

    # order=models.OneToOneField(to=Order, on_delete=models.CASCADE,blank=True,related_name="add")
    class Meta:
        db_table="t_address"

class Order(models.Model):
    statue=models.CharField(max_length=10,verbose_name="订单状态",blank=True,null=True)
    price=models.FloatField(verbose_name="价格")
    time=models.DateTimeField(verbose_name="时间",auto_now=True,null=True,blank=True)
    type=models.CharField(verbose_name="支付方式",null=True,max_length=100,blank=True)
    user=models.ForeignKey(to=User,on_delete=models.CASCADE,blank=True,related_name="order")
    address=models.OneToOneField(to=Address,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        db_table="t_order"

class Commodity(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称", blank=True, null=True)

    amount = models.IntegerField(verbose_name="数量", blank=True, null=True)

    price = models.FloatField(verbose_name="价格", blank=True, null=True)

    type = models.CharField(max_length=100, verbose_name="类型", blank=True, null=True)

    intro = models.CharField(max_length=100, verbose_name="简介", blank=True, null=True)

    desc = models.CharField(max_length=500, verbose_name="详情", blank=True, null=True)

    photo = models.BinaryField(verbose_name="商品图片", blank=True, null=True)

    unit = models.CharField(max_length=100, verbose_name="单位",  blank=True, null=True)


    class Meta:
        db_table="t_Commodity"



class Comment(models.Model):
    content = models.CharField(max_length=1000, verbose_name="评论内容", blank=True, null=True)

    commodity = models.ForeignKey(to=Commodity, on_delete=models.CASCADE, related_name="comments",blank=True)

    class Meta:

        db_table = "t_comment"

class Or_goods(models.Model):
    count=models.IntegerField(verbose_name="数量", blank=True, null=True)
    price=models.FloatField(verbose_name="价格", blank=True, null=True)
    commodity=models.ForeignKey(to=Commodity, on_delete=models.CASCADE,blank=True,null=True)
    order=models.ForeignKey(to=Order, on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        db_table="t_or_goods"

