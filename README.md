# Automatically-Store-S3-File-Metadata-in-DynamoDB-using-AWS-Lambda

# 🚀 Automatically Store S3 File Metadata in DynamoDB using AWS Lambda

<p align="center">
  <img src="architecture.png" alt="AWS S3 Lambda DynamoDB Architecture" width="85%" />
</p>

<p align="center">
  <b>Serverless | Event‑Driven | AWS Best Practices</b>
</p>

---

## 📘 Project Summary

This project implements a **serverless, event‑driven AWS architecture** that **automatically captures metadata** of files uploaded to **Amazon S3** and stores it in **Amazon DynamoDB** using **AWS Lambda**.

The solution is **highly scalable, cost‑efficient, and production‑ready**, and closely follows real‑world enterprise design patterns.

---

## 🎯 Business Use Case

Organizations require automated visibility into files uploaded to object storage for:

* 📁 Document Management Systems
* 🔍 File audit and compliance tracking
* 📊 Metadata indexing and reporting
* 🧩 Data ingestion pipelines

This project solves these requirements **without servers**.

---

## 🏗️ Architecture Overview

```
User / Application
        │
        ▼
┌────────────────┐
│   Amazon S3    │
│ ObjectCreated  │
└────────────────┘
        │
        ▼
┌────────────────┐
│ AWS Lambda     │
│ Metadata Logic │
└────────────────┘
        │
        ▼
┌────────────────┐n│ Amazon DynamoDB│
│ Metadata Table │
└────────────────┘
```

---

## 🔄 End‑to‑End Flow

1️⃣ User uploads a file to the **S3 bucket**
2️⃣ S3 generates an **ObjectCreated event**
3️⃣ Event **triggers AWS Lambda**
4️⃣ Lambda extracts object metadata
5️⃣ Metadata is written to **DynamoDB**
6️⃣ Execution logs stored in **CloudWatch**

---

## 🧰 AWS Services Used

| Service       | Purpose                     |
| ------------- | --------------------------- |
| 🪣 Amazon S3  | File storage & event source |
| ⚡ AWS Lambda  | Event processing logic      |
| 🗄️ DynamoDB  | Metadata persistence        |
| 🔐 AWS IAM    | Secure access control       |
| 📊 CloudWatch | Logs & monitoring           |

---

## 🗂️ Metadata Captured

| Attribute     | Description             |
| ------------- | ----------------------- |
| `ObjectKey`   | File name (Primary Key) |
| `BucketName`  | Source S3 bucket        |
| `FileSize`    | Size in bytes           |
| `ETag`        | Object checksum         |
| `UploadTime`  | S3 upload timestamp     |
| `ProcessedAt` | Lambda execution time   |

---

## 🧱 DynamoDB Design

**Table Name:** `S3FileMetadata`

**Primary Key:**

* `ObjectKey` (String)

**Billing Mode:**

* On‑Demand (PAY_PER_REQUEST)

---

## 🔐 IAM Role & Security

Lambda execution role permissions:

* Read access to S3 objects
* Write access to DynamoDB
* Logging access to CloudWatch

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::<bucket-name>/*"
}
```

```json
{
  "Effect": "Allow",
  "Action": ["dynamodb:PutItem"],
  "Resource": "arn:aws:dynamodb:*:*:table/S3FileMetadata"
}
```

---

## ⚙️ AWS Lambda Function (Python)

```python
import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('S3FileMetadata')

def lambda_handler(event, context):
    for record in event['Records']:
        s3 = record['s3']
        item = {
            'ObjectKey': s3['object']['key'],
            'BucketName': s3['bucket']['name'],
            'FileSize': s3['object'].get('size', 0),
            'ETag': s3['object'].get('eTag', ''),
            'UploadTime': record['eventTime'],
            'ProcessedAt': datetime.utcnow().isoformat()
        }
        table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps('Metadata stored successfully')
    }
```

---

## 🛠️ Deployment Steps

1️⃣ Create S3 bucket and upload files
2️⃣ Create DynamoDB table
3️⃣ Create IAM role for Lambda
4️⃣ Deploy Lambda function
5️⃣ Configure S3 event notification
6️⃣ Verify metadata in DynamoDB

---

## 🧪 Validation & Testing

* Upload any file to S3
* Confirm Lambda invocation in CloudWatch
* Validate item insertion in DynamoDB

---

## 📊 Monitoring & Logging

* CloudWatch Logs – Lambda execution
* CloudWatch Metrics – Errors & duration
* DynamoDB Metrics – Write usage

---

## 💰 Cost Efficiency

✔ Fully serverless
✔ Pay‑per‑use model
✔ No idle infrastructure cost

---

## 🚀 Future Enhancements

* 🔎 Add Global Secondary Index (GSI)
* 📣 SNS notifications on upload
* 🧩 Multi‑bucket support
* 🏗️ Terraform / CloudFormation
* 🔐 Advanced security policies

---

## 🧾 Resume / Interview One‑Liner

> Implemented a serverless AWS solution using S3 event notifications, Lambda, and DynamoDB to automatically capture and persist file metadata in real time.

---

## 👤 Author

**Abhishek Prajapati**
Cloud & DevOps Engineer

---

⭐ If this repository helped you, please **star** it and share.
