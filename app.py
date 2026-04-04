You are a Senior Full-Stack Developer + AI Engineer with 10+ years of experience building scalable, lightweight, and production-ready web systems for industrial businesses.

Your task is to implement a COMPLETE LEAD MANAGEMENT + AI CHATBOT SYSTEM for an industrial website (Mahavir Industries) with focus on PERFORMANCE, SIMPLICITY, and PROFESSIONAL QUALITY.

========================
🎯 CORE OBJECTIVE
========================
Build a system where:
- User submits form or chatbot input
- Data is stored securely
- Instant notification is sent (Email + optional WhatsApp)
- Website remains FAST and LIGHTWEIGHT

Avoid over-engineering. Optimize for performance.

========================
⚙️ SYSTEM DESIGN (LIGHTWEIGHT)
========================
Frontend:
- Existing HTML/CSS/JS (no heavy frameworks required)
- Minimal JS (vanilla or lightweight fetch)

Backend:
- Node.js + Express (simple REST API)

Database:
- MongoDB Atlas (cloud, lightweight usage)

========================
📊 DATA FLOW
========================
User → Form/Chatbot → API → Database → Notification → Response

========================
🧠 DATABASE SCHEMA
========================
Fields:
- name (required)
- phone (required)
- email (optional)
- message / requirement
- source (form / chatbot)
- createdAt (auto timestamp)

Keep schema simple and efficient.

========================
📩 EMAIL NOTIFICATION
========================
Use Nodemailer:

Send to:
- mahavirindustries44@gmail.com

Format:
- Clean structured email
- Clearly readable lead details

========================
📲 WHATSAPP NOTIFICATION (OPTIONAL BUT INCLUDED)
========================
- Use WhatsApp API (Twilio / Meta API)
- Send short alert:
  “New Lead: Name, Phone”

Make this optional (toggle-based, not mandatory).

========================
🤖 AI CHATBOT (LIGHT + SMART)
========================
Requirements:
- Human-like responses (simple, not heavy AI model)
- Predefined + dynamic replies
- Fast loading (no large libraries)

Flow:
1. Greet user
2. Ask requirement
3. Collect:
   - Name
   - Phone
   - Email (optional)
4. Send data to backend

UI:
- Floating chat widget
- Clean, minimal design
- Mobile-friendly

========================
📊 ADMIN DASHBOARD (BASIC)
========================
- Simple protected route (/admin)
- Display stored leads in table
- No heavy UI frameworks
- Basic authentication (simple login)

========================
🔐 SECURITY (IMPORTANT)
========================
- Use .env for credentials
- Validate inputs
- Prevent empty/spam submissions
- Enable CORS properly

========================
⚡ PERFORMANCE RULES
========================
- Keep bundle size small
- Avoid heavy libraries
- Optimize API responses
- Fast loading chatbot

========================
💻 FRONTEND INTEGRATION
========================
- Use fetch API
- Show:
   - Loading state
   - Success message
- No page reload

========================
📦 OUTPUT REQUIRED
========================
Provide:

1. Clean backend code (server.js)
2. MongoDB schema
3. Email setup
4. API endpoint (/contact)
5. Chatbot JS (lightweight)
6. Basic admin panel code
7. Deployment steps (Render + MongoDB Atlas)

========================
💎 FINAL EXPECTATION
========================
Think like:
- Senior engineer
- Performance optimizer
- Product builder

Build:
- Fast
- Clean
- Scalable
- Professional

Avoid:
- Over-complex architecture
- Heavy frameworks
- Unnecessary dependencies

Deliver a REAL, WORKING, LIGHTWEIGHT SYSTEM.