from flask import Flask, jsonify
from flask import request
import sys,os,boto3
import logging,json
import pymysql, base64
import random,string
import hashlib,uuid,datetime

import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

app = Flask(__name__)
@app.route('/status', methods=['GET'])
def status():
    successmessage={"status": 200}
    return(successmessage)
        
@app.route('/api/v1.0/checkout', methods=['POST'])
def checkout():
    iop={"cart":[
                {"productid":"","price":"","productname":""}
                ],
        "address":{},
        "user":"",
        "paymentoption":{}
    }
    awsregion=os.environ['AWS_REGION']
    CheckoutTableName=os.environ['CHECKOUT_TABLE_NAME']
    dynamodb=boto3.resource('dynamodb',region_name=awsregion)
    checkoutdb=dynamodb.Table(CheckoutTableName)
    
    user = request.json['user']
    
    usercart=checkoutdb.get_item(Key={"user":user})
    if 'Item' not in usercart:
        usercart={"user":user,
                  "address":request.json['address'],
                  "paymentoption":request.json['paymentoption'],
                  "cart":request.json['cart'],
                  "status":"initiated"
        }
        
    else:
        usercart=usercart['Item']
    for prod in request.json['cart']:
        if prod not in usercart['cart']:
            usercart['cart'].append(prod)
    total=0
    for prod in usercart['cart']:
        total=total+int(prod['price'])
    usercart['total']=total
    checkoutdb.put_item(Item=usercart)
    successmessage={
      "status": 200,
      "statusmessage": "Order Placed",
      "total":total
    }
    return(successmessage)
    
    
@app.route('/api/v1.0/getorder', methods=['POST'])
def getorder():
    iop={
        "user":""
    }
    awsregion=os.environ['AWS_REGION']
    CheckoutTableName=os.environ['CHECKOUT_TABLE_NAME']
    dynamodb=boto3.resource('dynamodb',region_name=awsregion)
    checkoutdb=dynamodb.Table(CheckoutTableName)
    
    user = request.json['user']
    
    usercart=checkoutdb.get_item(Key={"user":user})['Item']
    usercart=json.loads(json.dumps(usercart,cls=DecimalEncoder))
    
    successmessage={
      "status": 200,
      "statusmessage": "Order Placed",
      "response":usercart
    }
    return(successmessage)
    
@app.route('/api/v1.0/confirmorder', methods=['POST'])
def confirmorder():
    iop={
        "user":""
    }
    awsregion=os.environ['AWS_REGION']
    CheckoutTableName=os.environ['CHECKOUT_TABLE_NAME']
    dynamodb=boto3.resource('dynamodb',region_name=awsregion)
    checkoutdb=dynamodb.Table(CheckoutTableName)
    
    user = request.json['user']
    
    usercart=checkoutdb.get_item(Key={"user":user})['Item']
    usercart=json.loads(json.dumps(usercart,cls=DecimalEncoder))
    usercart['status']="Placed"
    checkoutdb.put_item(Item=usercart)
    successmessage={
      "status": 200,
      "statusmessage": "Order Confirmed",
      "response":usercart
    }
    return(successmessage)
