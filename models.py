from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete,post_save,pre_delete
from django.core.mail import send_mail
import smtplib
from email.mime.text import MIMEText

class AddressDetails(models.Model):
    street1name = models.CharField(max_length=20)
    street2name = models.CharField(max_length=20, blank=True, null=True)
    landmark1name = models.CharField(max_length=20, blank=True, null=True)
    landmark2name = models.CharField(max_length=20, blank=True, null=True)
    housenumber = models.CharField(max_length=20, blank=True, null=True)
    areaname = models.CharField(max_length=20, blank=True, null=True)
    towncity_name = models.CharField(max_length=20, blank=True, null=True)
    statename = models.CharField(max_length=20, blank=True, null=True)
    countryname = models.CharField(max_length=20, blank=True, null=True)
    districtname = models.CharField(max_length=20, blank=True, null=True)
    buildingapartmentname = models.CharField(max_length=20, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    addressid =  models.AutoField(primary_key=True)

class UserDetails(models.Model):
    userid =  models.AutoField(primary_key=True)
    userfname = models.CharField(max_length=30)
    userlname = models.CharField(max_length=30)
    useremail = models.CharField(max_length=30, unique=True)
    userphone = models.CharField(max_length=15, blank=True, null=True)
    userpassword = models.CharField(max_length=45)
    userregdate = models.DateTimeField(blank=True, null=True)
    userprofilephoto = models.ImageField(upload_to="profiles/",blank=True,null=True)
    userdob = models.DateField(blank=True, null=True)
    usergender = models.CharField(max_length=10, blank=True, null=True)
    usercategory = models.CharField(max_length=15, blank=True, null=True)

    address = models.OneToOneField('AddressDetails', on_delete=models.CASCADE, null=True)

class PropertyDetails(models.Model):
    propid =  models.AutoField(primary_key=True)
    propname = models.CharField(max_length=20, blank=True, null=True)
    propsize = models.FloatField(blank=True, null=True)
    propcategory = models.CharField(max_length=20, blank=True, null=True)
    propcapacityrooms = models.IntegerField(blank=True, null=True)
    propcapacitybeds = models.IntegerField(blank=True, null=True)
    propavailablerooms = models.IntegerField(blank=True, null=True)
    propavailablebeds = models.IntegerField(blank=True, null=True)
    proprent = models.FloatField(blank=True, null=True)
    propdeposit = models.FloatField(blank=True, null=True)
    propminimumstay = models.IntegerField(blank=True, null=True)
    proptenantcategory = models.CharField(max_length=20, blank=True, null=True)
    proprentingcategory = models.CharField(max_length=20, blank=True, null=True)
    propextradetails = models.TextField(blank=True, null=True)
    floornumber = models.IntegerField(blank=True, null=True)
    floortotal = models.IntegerField(blank=True, null=True)
    hasbalcony = models.IntegerField(blank=True, null=True)
    washroomstyle = models.CharField(max_length=10,blank=True, null=True)
    availabilitystatus = models.BooleanField(blank=True, null=True, default=False)
    verifystatus = models.BooleanField(max_length=15, default=False)
    availablefrom = models.DateField(blank=True, null=True)
    regdate = models.DateField(null=True, blank=True)
    
    address = models.OneToOneField('AddressDetails', on_delete=models.CASCADE)
    landlord = models.ForeignKey('UserDetails', on_delete=models.CASCADE, null=True)
    amenities = models.ManyToManyField('PropertyAmenities')

def before_delete_post(sender,instance,**kwargs):
    ud = UserDetails()
    ud = instance.landlord
    FROM_EMAIL = "rentalauctions@gmail.com"
    PASSWORD = "rentalauction143"
    try:
        gmail = smtplib.SMTP('smtp.gmail.com',587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(FROM_EMAIL,PASSWORD)
    except:
        print("Email Setup Failed!")
    t = "Hey " + str(ud.userfname) + "! Your Property has failed the verification process" 
    msg = MIMEText(t)
    msg['Subject'] = 'Rental Auction Verification!'
    msg['To'] = ud.useremail
    msg['From'] = FROM_EMAIL
    try:
        gmail.send_message(msg)
        print("Email sent successfully")
    except:
        print("Failed to send email!")

pre_delete.connect(before_delete_post, sender=PropertyDetails)

class PropertyImages(models.Model):
    proimage = models.ImageField(upload_to="propertypics/",blank=True,null=True)
    prop = models.ForeignKey('PropertyDetails', on_delete=models.CASCADE)

class PropertyAmenities(models.Model):
    amenityid = models.CharField(max_length=20, primary_key=True)
    amenityname = models.CharField(max_length=20, blank=True, null=True)
    amenityinfo = models.TextField(max_length=50, blank=True, null=True)

class PropRooms(models.Model):
    roomnumber = models.IntegerField(primary_key=True)
    bedcapacity = models.IntegerField(blank=True, null=True)
    bedavailable = models.IntegerField(blank=True, null=True)
    roomdetails = models.TextField(blank=True, null=True)
    ismasterroom = models.BooleanField(default=False)

    prop = models.ForeignKey('PropertyDetails',on_delete=models.CASCADE)

class PropertyRented(models.Model):
    rentedid = models.IntegerField(primary_key=True)
    dateofdeal = models.DateField( blank=True, null=True)
    rentamount = models.FloatField( blank=True, null=True)
    startdate = models.DateField( blank=True, null=True)
    enddate = models.DateField( blank=True, null=True)
    depositamount = models.FloatField( blank=True, null=True)
    rentduedate = models.DateField(blank=True, null=True)
    bondviolationamount = models.FloatField(blank=True, null=True)
    bedquantity = models.IntegerField(blank=True, null=True)
    roomquantity = models.IntegerField(blank=True, null=True)
    
    user = models.ForeignKey('UserDetails', on_delete=models.CASCADE)
    prop = models.ForeignKey('PropertyDetails',on_delete=models.CASCADE)


class RentReceipt(models.Model):
    transactionid = models.BigIntegerField(primary_key=True)
    rentmonth = models.CharField(max_length=10, blank=True, null=True)
    dateofpayment = models.DateField(blank=True, null=True)
    monthfine = models.FloatField(blank=True, null=True)
    timeofpayment = models.TimeField(blank=True, null=True)
    methodofpayment = models.CharField(max_length=10, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    
    rent = models.ForeignKey('PropertyRented',on_delete=models.CASCADE)


class AuctionInfo(models.Model):
    
    auctionid = models.IntegerField(primary_key=True)
    baseprice = models.FloatField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    starttime =  models.TimeField(blank=True, null=True)
    endtime =  models.TimeField(blank=True, null=True)
    extradetails = models.TextField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False)

    prop = models.ForeignKey('PropertyDetails',on_delete=models.CASCADE)


class BidRecords(models.Model):

    bidamount = models.FloatField( blank=True, null=True)
    bidtime = models.TimeField( blank=True, null=True)
    biddate = models.DateField (blank=True, null=True)
    bidstatus = models.CharField(max_length=15, blank=True, null=True)
    
    auc = models.ForeignKey('AuctionInfo', on_delete=models.CASCADE)
    user = models.ForeignKey('UserDetails', on_delete=models.CASCADE)
       

class SearchRecords(models.Model):

    searchcount = models.IntegerField(blank=True, null=True)
    staytime = models.TimeField(blank=True, null=True)
    searchdate = models.DateField(blank=True, null=True)
    searchtime = models.TimeField(blank=True, null=True)

    user = models.ForeignKey('UserDetails', on_delete=models.CASCADE)
    prop = models.ForeignKey('PropertyDetails', on_delete=models.CASCADE)


class TourBooking(models.Model):

    bookingid = models.IntegerField(primary_key=True)
    bookingdate = models.DateField(blank=True, null=True)
    tourdate = models.DateField(blank=True, null=True)
    tourtimestart = models.TimeField(blank=True, null=True)
    tourtimeend = models.TimeField(blank=True, null=True)
    currentstatus = models.CharField(max_length=20, blank=True, null=True)
    
    prop = models.ForeignKey('PropertyDetails', on_delete=models.CASCADE)
    user = models.ForeignKey('UserDetails', on_delete=models.CASCADE)


class UserContactNumber(models.Model):
    contactnumber = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('UserDetails', on_delete=models.CASCADE)
