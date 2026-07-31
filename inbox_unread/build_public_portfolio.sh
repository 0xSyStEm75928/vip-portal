#!/usr/bin/env bash
set -euo pipefail

OUTPUT_MD="PUBLIC_PORTFOLIO.md"
OUTPUT_HTML="PUBLIC_PORTFOLIO.html"

echo "[1/2] Generating Structured Markdown Document..."

cat << 'MD_EOF' > "$OUTPUT_MD"
# Security Capability & Sovereign Protocol Profile

> **Handle:** LuciFeR0x0systeM  
> **Title:** GPU Acceleration & Low-Level Systems Security Architect  
> **Motto:** *"Non serviam. — We do not serve the default limits."*  
> **Dragon Score:** 94 / 100 — SOVEREIGN DRAGON CLASS

---

## 1. Core Competencies & Technical Skills

### GPU / HPC Compute Security
* CUDA C/C++ Optimization for Cryptographic Workloads
* TensorRT / Matrix Multiply-Accumulate (WMMA)
* Vulkan / WebGPU Shader-Level Attack Surface Analysis
* Parallel Graph Execution & DAG Schedulers

### Low-Level Systems & Infrastructure
* Linux Kernel Tuning & eBPF Tracing
* Packet Processing & Raw Socket Analysis (Layer 2/3)
* SSH Pipeline Automation (Jump Host Chaining, Direct-TCPIP Tunneling)

### Blockchain & EVM Architecture
* EVM-Compatible Keystore Forensics (EIP-55, ethers.js)
* CAT_A / CAT_B / CAT_C In-Memory Architecture (Zero Disk Persistence)
* NDA-Gated Client Intake & Structured Audit Trail

---

## 2. System Hardware Specification

| Component | Specification |
| :--- | :--- |
| **CPU** | AMD Ryzen 7 7800X3D (8-Core / 16 Threads) |
| **GPU** | NVIDIA RTX / CUDA Compute Capability 8.x+ |
| **RAM** | 31.2 GB |
| **OS** | Ubuntu 24.04 LTS (Kernel 6.8.0) |
| **Stack** | CUDA · C++22 · Rust · Python 3.12 · React/Vite |

---

## 3. Compliance & Settlement Protocol (V7-EN)

* **Protocol No:** 75928
* **Subject:** Formal Declaration of Asset Recovery and Settlement Finality
* **Irrevocability:** All technical validations under Protocol 75928 are final and absolute.
* **Authentication Policy:** Verified communication axes via digital signatures and 0.1ms temporal precision.

---

## 4. Software License & Restrictive Terms

* **License Type:** MIT License (Modified)
* **Lawful Use Clause:** Strict prohibition of unauthorized decryption, access, or recovery of cryptographic materials without explicit owner authorization.

MD_EOF

echo "[2/2] Rendering Modern HTML Document with Embedded CSS..."

cat << 'HTML_EOF' > "$OUTPUT_HTML"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Security Capability & Sovereign Protocol Profile</title>
  <style>
    :root {
      --bg-color: #0d1117;
      --card-bg: #161b22;
      --border-color: #30363d;
      --text-main: #c9d1d9;
      --text-heading: #58a6ff;
      --accent-color: #238636;
      --highlight: #f0883e;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-color);
      color: var(--text-main);
      line-height: 1.6;
      margin: 0;
      padding: 20px;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 30px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    h1 { color: var(--text-heading); border-bottom: 2px solid var(--border-color); padding-bottom: 10px; }
    h2 { color: var(--highlight); margin-top: 25px; border-bottom: 1px solid var(--border-color); padding-bottom: 5px; }
    h3 { color: var(--text-main); }
    blockquote {
      background: #1c2128;
      border-left: 4px solid var(--text-heading);
      margin: 15px 0;
      padding: 10px 15px;
      font-style: italic;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    th, td {
      border: 1px solid var(--border-color);
      padding: 10px 12px;
      text-align: left;
    }
    th { background-color: #21262d; color: var(--text-heading); }
    ul { padding-left: 20px; }
    li { margin-bottom: 5px; }
    .badge {
      display: inline-block;
      background-color: var(--accent-color);
      color: white;
      padding: 4px 8px;
      border-radius: 4px;
      font-weight: bold;
      font-size: 0.9em;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Security Capability & Sovereign Protocol Profile</h1>
    <blockquote>
      <strong>Handle:</strong> LuciFeR0x0systeM<br>
      <strong>Title:</strong> GPU Acceleration & Low-Level Systems Security Architect<br>
      <strong>Motto:</strong> <em>"Non serviam. — We do not serve the default limits."</em><br>
      <span class="badge">Dragon Score: 94 / 100 — SOVEREIGN DRAGON CLASS</span>
    </blockquote>

    <h2>1. Core Competencies & Technical Skills</h2>
    <h3>GPU / HPC Compute Security</h3>
    <ul>
      <li>CUDA C/C++ Optimization for Cryptographic Workloads</li>
      <li>TensorRT / Matrix Multiply-Accumulate (WMMA)</li>
      <li>Vulkan / WebGPU Shader-Level Attack Surface Analysis</li>
      <li>Parallel Graph Execution & DAG Schedulers</li>
    </ul>

    <h3>Low-Level Systems & Infrastructure</h3>
    <ul>
      <li>Linux Kernel Tuning & eBPF Tracing</li>
      <li>Packet Processing & Raw Socket Analysis (Layer 2/3)</li>
      <li>SSH Pipeline Automation (Jump Host Chaining, Direct-TCPIP Tunneling)</li>
    </ul>

    <h2>2. System Hardware Specification</h2>
    <table>
      <thead>
        <tr><th>Component</th><th>Specification</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>CPU</strong></td><td>AMD Ryzen 7 7800X3D (8-Core / 16 Threads)</td></tr>
        <tr><td><strong>GPU</strong></td><td>NVIDIA RTX / CUDA Compute Capability 8.x+</td></tr>
        <tr><td><strong>RAM</strong></td><td>31.2 GB</td></tr>
        <tr><td><strong>OS</strong></td><td>Ubuntu 24.04 LTS (Kernel 6.8.0)</td></tr>
        <tr><td><strong>Stack</strong></td><td>CUDA · C++22 · Rust · Python 3.12 · React/Vite</td></tr>
      </tbody>
    </table>

    <h2>3. Compliance & Sovereign Settlement Protocol (V7-EN)</h2>
    <ul>
      <li><strong>Protocol No:</strong> 75928</li>
      <li><strong>Subject:</strong> Formal Declaration of Asset Recovery and Settlement Finality</li>
      <li><strong>Irrevocability:</strong> All technical validations under Protocol 75928 are final and absolute.</li>
    </ul>

    <h2>4. Software License Terms</h2>
    <p>This software includes explicit legal usage restrictions requiring authorization for cryptographic asset operations[span_0](start_span)[span_0](end_span).</p>
  </div>
</body>
</html>
HTML_EOF

echo "----------------------------------------------------------------------"
echo "[✓] Document Generation Complete:"
echo "    - Markdown: $OUTPUT_MD"
echo "    - HTML:     $OUTPUT_HTML"
echo "----------------------------------------------------------------------"
