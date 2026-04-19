```markdown
# 🔐 Secure Web App 2

> **Shift-Left Approach Implementation with CI/CD Pipeline**  
> A complete DevSecOps pipeline integrating SAST, Docker, and DAST — automated via Jenkins.

---

## 👤 Author
**Saleem Ali**  
Al-Nafi International College — AIOps Program  
April 2026

---

## 📌 Project Overview

This project implements the **Shift-Left Security Approach** by integrating automated
security scanning directly into a CI/CD pipeline. Vulnerabilities are detected and fixed
**early in the development lifecycle** — before reaching production.

```
Code → Jenkins → SonarQube SAST → Docker Build → Deploy → ZAP DAST → Report
```

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Jenkins | CI/CD pipeline automation |
| SonarQube 10.5 | SAST — static code analysis |
| OWASP ZAP | DAST — dynamic attack simulation |
| Docker | Application containerization |
| Python / Flask 3.0 | Web application |
| OpenJDK 17 | SonarQube runtime |
| OpenJDK 21 | Jenkins runtime |
| Kali Linux | Lab environment |

---

## 📁 Project Structure

```
secure-web-app-2/
├── app.py              ← Original Flask application
├── app_secure.py       ← Security-hardened version
├── requirements.txt    ← Python dependencies (Flask 3.0.0)
├── Dockerfile          ← Container build instructions
├── Jenkinsfile         ← CI/CD pipeline definition
├── README.md           ← This file
└── DOCUMENTATION.md    ← Full technical documentation
```

---

## ⚙️ Prerequisites

- Kali Linux (or any Debian-based Linux)
- Jenkins with OpenJDK 21
- SonarQube running on `http://localhost:9000` with OpenJDK 17
- OWASP ZAP running on `http://localhost:8090`
- Docker installed and running
- SonarScanner installed at `/opt/sonar-scanner/`

---

## 🚀 How to Run

### 1. Clone or navigate to the project
```bash
cd /root/Al-Razzak-Labs-2/DevSecOps/secure-web-app-2
```

### 2. Set permissions for Jenkins
```bash
sudo chmod o+x /root
sudo chmod -R o+rx /root/Al-Razzak-Labs-2
```

### 3. Create SonarQube project
- Go to `http://localhost:9000`
- Create project with key: `Secure-Web-App-2`
- Generate a **Global Analysis Token**

### 4. Run the Jenkins Pipeline
- Open Jenkins → `Secure-web-app-2` job
- Update `SONAR_TOKEN` in the pipeline environment block
- Click **Build Now**

### 5. View Results
| Report | URL |
|---|---|
| SonarQube SAST | `http://localhost:9000/dashboard?id=Secure-Web-App-2` |
| ZAP DAST Report | Jenkins sidebar → *ZAP DAST Report - Secure Web App 2* |

---

## 🔒 Security Hardening

Two versions of the app are included:

| Version | File | Security Status |
|---|---|---|
| Original | `app.py` | ❌ No SQL protection, no secret key |
| Hardened | `app_secure.py` | ✅ Parameterized queries, `secrets.token_hex(16)` |

To switch to the secure version:
```bash
cp app.py app_backup.py
cp app_secure.py app.py
```
Then re-run the Jenkins pipeline to compare scan results.

---

## 📐 Shift-Left Principle Applied

```
TRADITIONAL:  Code → Build → Deploy → Test → (vulnerability found late 😓)
SHIFT-LEFT:   Code → SAST → Build → Deploy → DAST → (caught early ✅)
```

---

## 📄 Full Documentation

See [`DOCUMENTATION.md`](./DOCUMENTATION.md) for the complete technical reference including
all troubleshooting steps, pipeline code, and detailed phase breakdowns.

---

*© 2026 Saleem Ali — Al-Nafi International College, AIOps Program*
```

***

## How to Create Both Files on Your Machine

```bash
cd /root/Al-Razzak-Labs-2/DevSecOps/secure-web-app-2

# Create README
nano README.md
# (paste the content above, then Ctrl+X → Y → Enter to save)

# Rename your documentation
nano DOCUMENTATION.md
# (paste the full documentation from earlier)
```

Your project now has **two perfectly structured files** just like a real professional GitHub repository, Saleem! 🎯 [coding-boot-camp.github](https://coding-boot-camp.github.io/full-stack/github/professional-readme-guide/)
