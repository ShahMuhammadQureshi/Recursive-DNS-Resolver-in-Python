# 🧠 Recursive DNS Resolver in Python

This project implements a recursive DNS resolver in Python that simulates a multi-layered DNS hierarchy (Root → TLD → Authoritative) and performs actual DNS queries using Python’s `dnspython` library.

It supports resolution of multiple DNS record types and includes caching for improved performance.

---

## 🔧 Features

- 🌐 **Recursive Resolution**: Simulates DNS recursion across Root, TLD, and Authoritative servers.
- 📌 **Multi-record Support**: Handles A, AAAA, MX, NS, and TXT record types.
- 🧠 **Local Caching**: Saves query results to `dns_record.txt` to avoid redundant lookups.
- 🔄 **Real DNS Integration**: Uses real DNS resolvers (e.g., Google `8.8.8.8`, Cloudflare `1.1.1.1`) under the hood.
- 📊 **Hop Tracing**: Displays each resolution step/hop in the output.
- 💾 **JSON Cache**: Clean cache structure for easy readability and persistence.

---

## 📂 File Structure

📂 Project Folder/
├── resolver.py # Main Python script (your 4.py).
├── dns_record.txt # JSON-based cache file.
└── README.md # Project documentation.
---

## ▶️ How to Run

1. **Install the required library**:

```bash
pip install dnspython
Run the script:

bash
Copy
Edit
python resolver.py
Enter a domain when prompted, e.g.:

text
Copy
Edit
Enter the domain to query: google.com
