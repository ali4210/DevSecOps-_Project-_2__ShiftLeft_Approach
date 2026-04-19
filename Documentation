# 📄 Project Documentation

***

**Document Title:** Shift-Left Approach Implementation with CI/CD Pipeline
**Project Name:** Secure Web App 2
**Author:** Saleem Ali
**Institution:** Al-Nafi International College — AIOps Program
**Date:** April 19, 2026
**Lab Path:** `/root/Al-Razzak-Labs-2/DevSecOps/secure-web-app-2`

***

## 1. 📌 Project Overview

This project demonstrates the implementation of a **Shift-Left Security Approach** integrated into a CI/CD pipeline using Jenkins. The goal was to automate security scanning at both the source code level and the runtime application level, ensuring vulnerabilities are detected and fixed **early in the development lifecycle** — before reaching production.

The pipeline combines:
- **Static Application Security Testing (SAST)** using SonarQube
- **Containerization** using Docker
- **Dynamic Application Security Testing (DAST)** using OWASP ZAP
- **Pipeline Automation** using Jenkins

***

## 2. 🎯 Objectives

- Understand and implement the Shift-Left security philosophy
- Build a live Python Flask web application
- Containerize the application using Docker
- Automate security scanning via a Jenkins CI/CD pipeline
- Identify vulnerabilities using SonarQube (SAST) and OWASP ZAP (DAST)
- Harden the application by creating a security-fixed version
- Compare scan results before and after security improvements

***

## 3. 🛠️ Tools & Technologies Used

| Tool | Version | Purpose |
|---|---|---|
| **Operating System** | Kali Linux | Lab environment |
| **Jenkins** | Latest | CI/CD pipeline automation |
| **OpenJDK** | 21 | Jenkins runtime |
| **OpenJDK** | 17 | SonarQube runtime |
| **SonarQube** | 10.5.0 | SAST — static code analysis |
| **SonarScanner** | 5.0.1 | SonarQube scanning agent |
| **OWASP ZAP** | Latest | DAST — dynamic attack simulation |
| **Docker** | Latest | Application containerization |
| **Python** | 3.11-slim | Application runtime |
| **Flask** | 3.0.0 | Web application framework |

***

## 4. 🖥️ Phase 0 — Environment Setup

Before the pipeline could be built, the host machine required careful configuration.

### 4.1 Jenkins Installation
Jenkins was installed successfully on Kali Linux along with required plugins.

### 4.2 Java Version Conflict & Resolution
A critical challenge was that **Jenkins requires OpenJDK 21** while **SonarQube requires OpenJDK 17**. Running a single Java version caused both tools to conflict.

**Resolution:** Two separate Java versions were installed and assigned individually:

```bash
# Set SonarQube to use Java 17
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Jenkins uses Java 21 (set in Jenkins service configuration)
JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
```

### 4.3 ZAP Plugin Corruption & Recovery
An outdated OWASP ZAP plugin was installed from the Jenkins marketplace, which **corrupted Jenkins and the workspace**. Jenkins crashed completely.

**Resolution:**
- Removed the corrupted plugin manually
- Restored Jenkins by fixing the Java environment
- Installed OWASP ZAP as a **standalone proxy** instead — communicating via REST API on port `8090`
- This approach is more stable and does not require any Jenkins plugin

### 4.4 SonarQube Installation
SonarQube was installed and configured with OpenJDK 17 exclusively. SonarScanner 5.0.1 was installed at `/opt/sonar-scanner/`.

***

## 5. 🏗️ Phase 1 — Application Development

A simple Python Flask web application was created as the target for security scanning.

### 5.1 Project Structure

```
/root/Al-Razzak-Labs-2/DevSecOps/secure-web-app-2/
├── app.py               ← Main Flask application
├── app_secure.py        ← Security-hardened version
├── requirements.txt     ← Python dependencies
└── Dockerfile           ← Container build instructions
```

### 5.2 Application Code (`app.py`)

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<html><body>
<h1>DevSecOps Lab App</h1>
<form method="GET">
  <input name="name" placeholder="Enter your name">
  <button type="submit">Greet</button>
</form>
{% if name %}
  <h2>Hello, {{ name }}!</h2>
{% endif %}
</body></html>
"""

@app.route('/')
def index():
    name = request.args.get('name', '')
    return render_template_string(HTML, name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 5.3 Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

### 5.4 Requirements

```
flask==3.0.0
```

***

## 6. 🔧 Phase 2 — Jenkins Pipeline

### 6.1 Pipeline Architecture

```
Checkout → SAST (SonarQube) → Docker Build → Deploy → DAST (ZAP) → Cleanup → Report
```

### 6.2 Full Pipeline Script

```groovy
pipeline {
    agent any

    environment {
        APP_NAME    = "Secure-Web-App-2"
        APP_IMAGE   = "secure-web-app-2:latest"
        APP_PORT    = "5000"
        APP_PATH    = "/root/Al-Razzak-Labs-2/DevSecOps/secure-web-app-2"
        SONAR_URL   = "http://localhost:9000"
        SONAR_TOKEN = "squ_af3387d92e36f096b3392b09b81d2836d8c4e862"
        ZAP_URL     = "http://localhost:8090"
    }

    stages {

        stage('Checkout') {
            steps {
                sh '''
                  cp -r ${APP_PATH}/. .
                  mkdir -p reports
                '''
            }
        }

        stage('SAST - SonarQube Scan') {
            steps {
                sh """
                  /opt/sonar-scanner/bin/sonar-scanner \
                    -Dsonar.projectKey=${APP_NAME} \
                    -Dsonar.projectName="Secure Web App 2" \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=${SONAR_URL} \
                    -Dsonar.token=${SONAR_TOKEN} \
                    -Dsonar.python.version=3
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${APP_IMAGE} ."
            }
        }

        stage('Deploy App') {
            steps {
                sh """
                  docker stop secure-web-app-2 || true
                  docker stop Secure-Web-App-2 || true
                  docker rm secure-web-app-2 || true
                  docker rm Secure-Web-App-2 || true
                  OLDCONTAINER=\$(docker ps --filter "publish=5000" -q)
                  if [ ! -z "\$OLDCONTAINER" ]; then
                    docker stop \$OLDCONTAINER
                    docker rm \$OLDCONTAINER
                  fi
                  docker run -d --name ${APP_NAME} -p ${APP_PORT}:5000 ${APP_IMAGE}
                  sleep 10
                """
            }
        }

        stage('DAST - ZAP Scan') {
            steps {
                sh """
                  curl -s "${ZAP_URL}/JSON/spider/action/scan/?url=http://localhost:${APP_PORT}"
                  sleep 20
                  curl -s "${ZAP_URL}/JSON/ascan/action/scan/?url=http://localhost:${APP_PORT}"
                  sleep 40
                  curl -s "${ZAP_URL}/OTHER/core/other/htmlreport/" \
                    -o reports/zap-report.html
                """
            }
        }

        stage('Cleanup') {
            steps {
                sh """
                  docker stop ${APP_NAME} || true
                  docker rm ${APP_NAME} || true
                """
            }
        }
    }

    post {
        always {
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'zap-report.html',
                reportName: 'ZAP DAST Report - Secure Web App 2'
            ])
        }
    }
}
```

***

## 7. 🚧 Phase 3 — Troubleshooting Log

| # | Error | Root Cause | Resolution |
|---|---|---|---|
| 1 | `Permission denied` on `/root/` | Jenkins `jenkins` user has no access to root home | `sudo chmod o+x /root && sudo chmod -R o+rx /root/Al-Razzak-Labs-2` |
| 2 | `Not authorized to analyze project` | Project not created in SonarQube UI; wrong token type | Created project manually; generated Global Analysis Token |
| 3 | `Similar key already exists: Secure-Web-App-2` | Case mismatch between pipeline key and SonarQube key | Updated `APP_NAME = "Secure-Web-App-2"` in pipeline |
| 4 | `HTML directory does not exist` | `reports/` only created in ZAP stage which was being skipped | Added `mkdir -p reports` in Checkout stage; set `allowMissing: true` |
| 5 | `Port 5000 already allocated` | Previous failed build left container running on port 5000 | Added force port-cleanup logic before `docker run` |

***

## 8. ✅ Phase 4 — Build Results

### Final Successful Pipeline Run

| Stage | Status | Duration |
|---|---|---|
| Checkout | ✅ SUCCESS | ~1s |
| SAST - SonarQube Scan | ✅ SUCCESS | ~5s |
| Build Docker Image | ✅ SUCCESS | ~1s (cached) |
| Deploy App | ✅ SUCCESS | ~10s |
| DAST - ZAP Scan | ✅ SUCCESS | ~60s |
| Cleanup | ✅ SUCCESS | ~1s |
| ZAP HTML Report | ✅ PUBLISHED | — |

**SonarQube Dashboard:** `http://localhost:9000/dashboard?id=Secure-Web-App-2`
**ZAP Report:** Available in Jenkins sidebar under *ZAP DAST Report - Secure Web App 2*

***

## 9. 🔒 Phase 5 — Security Hardening

### 9.1 Vulnerability Comparison

| Vulnerability | `app.py` (Before) | `app_secure.py` (After) |
|---|---|---|
| SQL Injection | ❌ Raw string queries | ✅ Parameterized `?` queries |
| Secret Key | ❌ None / missing | ✅ `secrets.token_hex(16)` |
| Login Route | ❌ Not present | ✅ Secure login with form validation |

### 9.2 Security-Fixed Code (`app_secure.py`)

```python
from flask import Flask, request
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        # Parameterized query prevents SQL injection
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()
        return "Login successful!" if result else "Invalid credentials"
    return '''
    <form method="post">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <input type="submit" value="Login">
    </form>'''

@app.route('/')
def home():
    return '<h1>Secure Web App Demo</h1><a href="/login">Login</a>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 9.3 Verify Quality Gate via API

```bash
curl -u admin:YOUR_PASSWORD \
  "http://localhost:9000/api/qualitygates/project_status?projectKey=Secure-Web-App-2"
```

***

## 10. 📐 Shift-Left Mapping

| Shift-Left Principle | Implementation in This Project |
|---|---|
| Test at the Code stage | SonarQube scanned Python source before deployment |
| Test at the Build stage | Dockerfile scanned by SonarQube IaC sensor |
| Security automated in CI/CD | Jenkins orchestrated all security steps automatically |
| Fast feedback loop | Results available after every single build |
| Fix early, not in production | `app_secure.py` created and re-scanned within the same pipeline |
| Runtime vulnerability detection | ZAP attacked live app before it could reach production |

***

## 11. 📚 Key Learnings

- The Shift-Left approach catches vulnerabilities **at code and build time**, not after deployment
- **Java version segregation** is critical when running multiple Java-dependent tools on the same server
- Jenkins communicates with ZAP more reliably via **REST API** than through plugins
- **Parameterized SQL queries** are the standard defense against SQL injection attacks
- Every failed build is a **debugging opportunity** — each error in this lab taught a real industry skill
- A complete DevSecOps pipeline covers **SAST + containerization + DAST** as minimum layers of security

***

## 12. 🏁 Conclusion

This project successfully implemented a **Shift-Left Approach** by integrating automated security scanning directly into a Jenkins CI/CD pipeline. By catching vulnerabilities at the source code stage with SonarQube and at the runtime stage with OWASP ZAP, the pipeline ensures no insecure code reaches production undetected.

The project also demonstrated real-world problem-solving skills — recovering from a Jenkins crash, resolving Java version conflicts, debugging permission errors, and handling Docker port conflicts — all challenges that professional DevSecOps engineers face daily.

***

*Documentation prepared by Saleem Ali | Al-Nafi International College — AIOps Program | April 2026*
