# 📧 Serverless Email System

A fully serverless project built on AWS to send emails using AWS SES, AWS SQS and logs stored in DynamoDB. The system is triggered by API Gateway and runs an AWS Lambda function to process the logic.
---

## 🧰 Tech Stack

| Layer            | AWS Service         |
|------------------|---------------------|
| API Trigger      | Amazon API Gateway  |
| Compute Logic    | AWS Lambda          |
| Email Service    | Amazon SES          |
| Error Queue      | Amazon SQS + DLQ    |
| Logs Storage     | Amazon DynamoDB     |
| IAM Permissions  | AWS IAM             |


                                +-------------------------+
                                |     Client (Postman)    |
                                | or any API Test Tool    |
                                +-----------+-------------+
                                            |
                                            v
                                +-------------------------+
                                |   Amazon API Gateway    |
                                | (POST /send-email)      |
                                +-----------+-------------+
                                            |
                                            v
                                +-------------------------+
                                |       AWS Lambda        |
                                |   (Handles business     |
                                |    logics: email send,  |
                                |    error handling)      |
                                +-----+----------+--------+
                                      |          |
                        +-------------+          +---------------------+
                        |                                    |         
                        v                                    v         
          +------------------------+            +---------------------------+
          |       Amazon SES       |            |    Amazon DynamoDB        |
          |                        |            |   (Log email status)      |
          +------------------------+            +---------------------------+

                        |
                        v
          +-----------------------------+
          |         On Failure          |
          |                             |
          +-------------+---------------+
                        |
                        v
               +--------------------+
               |  Amazon SQS (DLQ)  |
               |                    |
               +--------------------+
---                        

## Flow of the system:
1. Postman sends a POST request to API Gateway.
2. API Gateway triggers the Lambda Function.
3. Lambda Function:
   - Attempts to send an email using Amazon SES.
   - On success it created logs info to DynamoDB.
   - On failure it pushes the failed event to Amazon SQS Dead Letter Queue (DLQ).

---  

## 🚀 4. How to Deploy

### Step 1: IAM Setup
- Create a role for Lambda with policies:
  - AmazonSESFullAccess
  - AmazonSQSFullAccess
  - AmazonDynamoDBFullAccess

### Step 2: Create Lambda Function
- Runtime: Python 3.12 or later
- Upload `lambda/lambda_function.py`
- Attach the IAM role

### Step 3: Create DynamoDB Table
- create a table and set the partition key as String.

### Step 4: Set up SES
- Verify email addresses (sender and recipient)

### Step 5: Set up SQS
- Create a Dead Letter Queue (DLQ)
- Attach it to Lambda

### Step 6: Set up API Gateway
- Create a REST API
- Add POST endpoint.
- Integrate with Lambda

### Step 7: Test
- Use Postman or cURL:
```sample json
{
  "to": "receiver@example.com",
  "subject": "Hello",
  "message": "This is a test email!"
}


---

### Use Cases
1. Makes sure customers always get their order confirmations and shipping updates in e-commerce.
2. Helps new users receive their verification or welcome emails whenever they sign up, purchase a service or subscribe to a website.
3. Makes sure critical system alerts always reach the admins so issues get fixed asap.

## 📢 Note
This project runs in **SES sandbox mode** so both sender and receiver emails must be verified.



  
