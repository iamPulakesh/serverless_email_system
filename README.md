# 📧 Serverless Email System

This is a fully serverless project built on AWS to send emails using AWS SES, AWS SQS and logs stored in DynamoDB. The system is triggered by API Gateway and runs an AWS Lambda function to process the logic.
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

### Use Cases
1. Makes sure customers always get their order confirmations and shipping updates in e-commerce.
2. Helps new users receive their verification or welcome emails whenever they sign up, purchase a service or subscribe to a website.
3. Makes sure critical system alerts always reach the admins so issues get fixed asap.

## 📢 Note
This project runs in **SES sandbox mode** so both sender and receiver emails must be verified.



  
