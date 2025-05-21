# 📧 Serverless Email Notification System (with Fault Tolerance)

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
| Monitoring       | Amazon CloudWatch   |
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
                                |    logic: email send,   |
                                |    error handling)      |
                                +-----+----------+--------+
                                      |          |
                        +-------------+          +---------------------+
                        |                                    |         
                        v                                    v         
          +------------------------+            +---------------------------+
          |    Amazon SES          |            |    Amazon DynamoDB        |
          | (Send Email Service)   |            | (Log email status)        |
          +------------------------+            +---------------------------+

                        |
                        v
          +-----------------------------+
          |   On Failure (e.g.          |
          |   unverified address)       |
          +-------------+---------------+
                        |
                        v
               +--------------------+
               |  Amazon SQS (DLQ)  |
               |  Dead Letter Queue |
               +--------------------+

                                |
                                v
                    +-------------------------+
                    |   Amazon CloudWatch     |
                    |   (Logs, Monitoring)    |
                    +-------------------------+
