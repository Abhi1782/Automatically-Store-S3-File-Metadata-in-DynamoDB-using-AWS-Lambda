# 🚀 Automatically Store S3 File Metadata in DynamoDB using AWS Lambda

## 📘 Project Summary

This project implements a **serverless, event‑driven AWS architecture** that **automatically captures metadata** of files uploaded to **Amazon S3** and stores it in **Amazon DynamoDB** using **AWS Lambda**.

The solution is **highly scalable, cost‑efficient, and production‑ready**, and closely follows real‑world enterprise design patterns.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🎯 Business Use Case

Organizations require automated visibility into files uploaded to object storage for:

* 📁 Document Management Systems
* 🔍 File audit and compliance tracking
* 📊 Metadata indexing and reporting
* 🧩 Data ingestion pipelines

This project solves these requirements **without servers**.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🔄 End‑to‑End Flow

* 1️⃣ User uploads a file to the **S3 bucket**
* 2️⃣ S3 generates an **ObjectCreated event**
* 3️⃣ Event **triggers AWS Lambda**
* 4️⃣ Lambda extracts object metadata
* 5️⃣ Metadata is written to **DynamoDB**
* 6️⃣ Execution logs stored in **CloudWatch**

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🧰 AWS Services Used

| Service       | Purpose                     |
| ------------- | --------------------------- |
| 🪣 Amazon S3  | File storage & event source |
| ⚡ AWS Lambda  | Event processing logic      |
| 🗄️ DynamoDB  | Metadata persistence        |
| 🔐 AWS IAM    | Secure access control       |
| 📊 CloudWatch | Logs & monitoring           |

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🗂️ Metadata Captured

| Attribute     | Description             |
| ------------- | ----------------------- |
| `ObjectKey`   | File name (Primary Key) |
| `BucketName`  | Source S3 bucket        |
| `FileSize`    | Size in bytes           |
| `ETag`        | Object checksum         |
| `UploadTime`  | S3 upload timestamp     |
| `ProcessedAt` | Lambda execution time   |

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🧱 DynamoDB Design

**Table Name:** `S3FileMetadata`

**Primary Key:**

* `ObjectKey` (String)

**Billing Mode:**

* On‑Demand (PAY_PER_REQUEST)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
from urllib.parse import unquote_plus
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = "S3FilesMetadata"
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            object_key = unquote_plus(record['s3']['object']['key'])

            response = s3_client.head_object(
                Bucket=bucket_name,
                Key=object_key
            )

            item = {
                # MUST MATCH DynamoDB PARTITION KEY NAME
                "FileName": object_key,

                "BucketName": bucket_name,
                "FileSize": response['ContentLength'],
                "ContentType": response.get('ContentType', 'unknown'),
                "LastModified": response['LastModified'].isoformat(),
                "UploadedAt": datetime.utcnow().isoformat()
            }

            table.put_item(Item=item)
            print(f"Metadata stored successfully for {object_key}")

        return {
            "statusCode": 200,
            "body": json.dumps("Metadata stored successfully")
        }

    except Exception as e:
        print("ERROR:", str(e))
        raise

```

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🪜 Step‑by‑Step Project Implementation Guide

This section provides a **complete, sequential walkthrough** of building the project from scratch, aligned with the architecture shown.

---

### 🪣 Step 1: Create an Amazon S3 Bucket

* Create an S3 bucket (example: `s3-file-metadata-bucket`)
* Region: Same as Lambda and DynamoDB
* Enable **Block Public Access** (recommended)
* (Optional) Enable **Versioning** for future audit requirements

**Purpose:** Acts as the file ingestion layer and event source.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (52)" src="https://github.com/user-attachments/assets/1b7816f4-5dd5-4ead-927c-bb9e9b8544d0" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (53)" src="https://github.com/user-attachments/assets/11c43b92-c10c-49e2-b628-3fac144fcf5d" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 🗄️ Step 2: Create DynamoDB Table

* Table Name: `S3FileMetadata`
* Partition Key: `ObjectKey` (String)
* Billing Mode: **On‑Demand (PAY_PER_REQUEST)**
* Encryption: Enabled by default

**Purpose:** Stores structured metadata for each uploaded object.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (54)" src="https://github.com/user-attachments/assets/bbf6cffd-579e-4c0f-b17f-aeebcf6d412b" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (55)" src="https://github.com/user-attachments/assets/28a0ec76-082a-4f5e-89a1-8b44f8821e3c" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 🔐 Step 3: Create IAM Role for Lambda

Create an IAM role with the following permissions:

* Read access to S3 objects
* Write access to the DynamoDB table
* Write access to CloudWatch Logs

**Purpose:** Ensures secure, least‑privilege access between AWS services.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (56)" src="https://github.com/user-attachments/assets/b9bd1883-bf1f-42a2-b7fe-4b1a081c3a5d" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (57)" src="https://github.com/user-attachments/assets/fd54120f-32d9-4bc3-a1df-a31cc50417f8" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (58)" src="https://github.com/user-attachments/assets/813c906e-228e-4513-b0ce-6e813e25e7a9" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### ⚡ Step 4: Create AWS Lambda Function

* Function Name: `S3MetadataToDynamoDB`
* Runtime: Python 3.x
* Memory: 128 MB
* Timeout: 30 seconds
* Execution Role: IAM role created in Step 3

**Purpose:** Processes S3 events and extracts metadata.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (59)" src="https://github.com/user-attachments/assets/b142313e-bb84-41b3-9ff3-9a540411328c" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1365" height="525" alt="Screenshot 2025-12-27 203506" src="https://github.com/user-attachments/assets/4c63713c-f4de-494e-8a89-d3528ab89b49" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 🧠 Step 5: Add Lambda Function Code

* Paste the provided Python code into the Lambda function
* Update the DynamoDB table name if required
* Save and deploy the function

**Purpose:** Implements metadata extraction and persistence logic.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (62)" src="https://github.com/user-attachments/assets/eea68215-4531-44cc-ae4b-debd22459e4f" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 🔔 Step 6: Configure S3 Event Notification

* Navigate to S3 bucket → Properties → Event notifications
* Event type: **ObjectCreated (All)**
* Destination: AWS Lambda
* Select the Lambda function created earlier
* (Optional) Add suffix filters like `.pdf`, `.jpg`

**Purpose:** Automatically triggers Lambda on file uploads.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (60)" src="https://github.com/user-attachments/assets/0e07618e-4f0d-496f-900e-7397fda98d9a" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1365" height="464" alt="Screenshot 2025-12-27 211250" src="https://github.com/user-attachments/assets/f0fe3380-997f-4966-a0af-e6f2e855b368" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 📤 Step 7: Upload File to S3 (Testing)

* Upload any file (PDF, image, text) to the S3 bucket
* Ensure upload completes successfully

**Purpose:** Validates end‑to‑end event flow.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (68)" src="https://github.com/user-attachments/assets/e0003edc-c4a7-4e8c-b74f-bc1323e05ff5" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 📊 Step 8: Verify Lambda Execution

* Open Amazon CloudWatch Logs
* Locate the Lambda log group
* Confirm successful execution without errors

**Purpose:** Ensures Lambda is triggered and runs correctly.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (65)" src="https://github.com/user-attachments/assets/486314f0-f7d3-489c-a87b-dd024823bcbc" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### ✅ Step 9: Verify Metadata in DynamoDB

* Open DynamoDB table
* View table items
* Confirm metadata fields are populated correctly

**Purpose:** Confirms successful metadata persistence.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (67)" src="https://github.com/user-attachments/assets/a788ad20-6fd5-456f-9c8d-62036b9ca8ef" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 📈 Step 10: Monitoring and Validation

* Monitor Lambda invocation metrics
* Check DynamoDB write capacity usage
* Enable CloudWatch alarms if required

**Purpose:** Ensures reliability and operational visibility.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (66)" src="https://github.com/user-attachments/assets/ff6dfb47-02e6-4a59-b01b-8b9691cda1ee" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🧪 Validation & Testing

* Upload any file to S3
* Confirm Lambda invocation in CloudWatch
* Validate item insertion in DynamoDB

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 📊 Monitoring & Logging

* CloudWatch Logs – Lambda execution
* CloudWatch Metrics – Errors & duration
* DynamoDB Metrics – Write usage

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (65)" src="https://github.com/user-attachments/assets/97731367-4f0d-4e7f-84ee-08efc0f9c165" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1366" height="768" alt="Screenshot (66)" src="https://github.com/user-attachments/assets/2a6718b8-a56f-48c8-a271-97655571cb2c" />

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 💰 Cost Efficiency

* ✔ Fully serverless
* ✔ Pay‑per‑use model
* ✔ No idle infrastructure cost




