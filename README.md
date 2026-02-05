# CMPE 273 – Week 1 Lab 1
Your First Distributed System

## How to Run Locally

### Service A (Echo Service)

cd cmpe273-week1-lab1/python-http  
python3 service_a.py  

Service A runs on http://127.0.0.1:8080

---

### Service B (Client Service)

cd cmpe273-week1-lab1/python-http  
python3 service_b.py  

Service B runs on http://127.0.0.1:8081

---

## Success Proof

### Service B calling Service A

curl "http://127.0.0.1:8081/call-echo?msg=hello"

Expected output:

{
  "service_b": "ok",
  "service_a_response": {
    "echo": "hello"
  }
}

Screenshot proof:

success.png

---

## Failure Proof

### Service A stopped, Service B still running

curl -i "http://127.0.0.1:8081/call-echo?msg=hello"

Expected output:

HTTP/1.1 503  
{"error":"Service A unavailable"}

Screenshot proof:

failure.png

---

## What Makes This Distributed?

This system is distributed because it consists of two separate services running as independent processes that communicate with each other over the network using HTTP. Since the services are decoupled, one service can fail without bringing down the other. When Service A is unavailable, Service B continues running and handles the failure gracefully using timeouts and appropriate error responses.
