# VTHomeFix — Full Website + Backend

Complete website for **VTHomeFix** (by Vinay Tiwari) — painting, carpentry, tiles fitting, and electrical services across Vasai, Virar, Nalasopara, Mira Road, Bhayandar, and Borivali, Mumbai.

---

## 📁 What's Inside

- **Django backend** — stores bookings, enquiries, and portfolio photos in a real database
- **Single-page frontend** — home, services, booking, contact pages (no reload needed)
- **AI Chatbot "Shivam"** — trained on all your services, pricing, and areas
- **Django Admin Panel** — manage bookings, enquiries, and photos at `/django-admin/`
- **SEO-ready** — schema markup, sitemap.xml, robots.txt, meta tags for local search

---

## 🔑 Admin Login (Your Dashboard)

URL: `https://yourdomain.com/django-admin/`

```
Username: vinay
Password: VTHomeFix@2025
```

**⚠️ Change this password immediately after first login** (Admin panel → click your username top-right → Change Password).

From here you can:
- View/manage all **Bookings** (mark as Confirmed, In Progress, Completed)
- View/reply to **Enquiries**
- View/manage **Worker Applications** — people applying to join your team as painters, carpenters, tile-fitters, electricians, etc. (mark as Reviewing, Contacted, Hired, Not Suitable)
- **Upload portfolio photos** — they instantly appear on your homepage gallery
- See basic visit analytics

---

## 🚀 STEP-BY-STEP: Going Live

### Step 1 — Push code to GitHub
1. Create a free account at [github.com](https://github.com) if you don't have one
2. Create a new repository called `vthomefix`
3. Upload all these files to it (or ask me and I'll give you git commands)

### Step 2 — Deploy the backend (Railway — easiest, free tier available)
1. Go to [railway.app](https://railway.app) → Sign up with GitHub
2. Click **New Project → Deploy from GitHub repo** → select `vthomefix`
3. Railway auto-detects Django and deploys it
4. Click **+ New → Database → PostgreSQL** to add a real database (free tier)
5. In your Django service → **Variables** tab, add:
   ```
   DJANGO_SECRET_KEY = (generate any random 50-character string)
   DEBUG = False
   ```
6. Once deployed, open **Settings → Networking → Generate Domain** — you'll get a URL like `vthomefix.up.railway.app`
7. Run migrations: in Railway, open the service **Shell** tab and run:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```
   (set your own username/password here)

**Alternative: Render.com** works almost identically and also has a free tier — same steps apply.

### Step 3 — Buy your domain name
1. Go to **GoDaddy**, **Namecheap**, or **Hostinger**
2. Search for `vthomefix.com` or `vthomefix.in` (~₹700–₹1,200/year)
3. Buy it

### Step 4 — Connect domain to Railway
1. In Railway → your service → **Settings → Networking → Custom Domain**
2. Enter `vthomefix.com` and `www.vthomefix.com`
3. Railway gives you a CNAME record — copy it
4. Go to your domain registrar's **DNS settings** and paste that CNAME record
5. Wait 10–60 minutes for DNS to propagate
6. Your site is now live at `https://vthomefix.com` 🎉

### Step 5 — Update settings for production
Once your domain is live, edit `vthomefix/settings.py`:
```python
ALLOWED_HOSTS = ['vthomefix.com', 'www.vthomefix.com']  # remove the '*' wildcard
```
And in `templates/index.html`, the canonical URLs are already set to `vthomefix.com`.

---

## 📈 HOW TO RANK #1 ON GOOGLE (Virar to Borivali)

Getting found "on top" when someone searches **"painter near me"** or **"electrician Vasai"** takes both technical setup (already done in this site) AND ongoing local marketing. Here's exactly what to do, in priority order:

### 1. Google Business Profile (MOST IMPORTANT — do this first, it's free)
This is what actually shows your business on Google Maps and the local 3-pack at the top of search results.
1. Go to [google.com/business](https://www.google.com/business)
2. Create a profile: Business name **"VTHomeFix"**, Category: "Painting contractor" (add Carpenter, Electrician, Tile contractor as additional categories)
3. Add address (Vasai), phone (9503833197), website (vthomefix.com), hours
4. Google will mail/call a verification code — complete verification
5. **Upload 15-20 real photos** of actual work (replace the placeholders!)
6. Post weekly updates (a finished job, a tip, an offer)

### 2. Get Reviews (massively boosts local ranking)
- After every job, ask the customer: *"Could you leave us a quick Google review?"*
- Send them the direct link from your Google Business Profile dashboard
- Aim for 20+ reviews in the first 2 months — this alone can push you above competitors

### 3. Local Keywords Already Built Into This Site
The site is already optimized for: *painter Vasai, painter Virar, carpenter Vasai, electrician Vasai, tiles fitting Mumbai, home renovation Virar, painter Borivali, painter Mira Road, painter Bhayandar, painter Nalasopara*. Once live, submit your sitemap:
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Add property → enter `vthomefix.com`
3. Verify ownership (Google gives you a simple HTML tag or DNS method)
4. Submit sitemap: `https://vthomefix.com/sitemap.xml`
5. Google will start crawling and indexing your site within days

### 4. List on Other Local Directories (backlinks help ranking)
Create free listings on:
- **JustDial**
- **Sulekha**
- **UrbanClap/Urban Company** (if they accept individual contractors)
- **IndiaMART**
- **Facebook Business Page** + **Instagram Business Page**
Use the exact same Name, Address, Phone everywhere — consistency matters a lot for local SEO.

### 5. WhatsApp Business + Status Updates
Convert your number to **WhatsApp Business** (free app) — add your services as a catalog, set auto-replies, and post work photos to your Status regularly. People in your area will see and remember you.

### 6. Local Word-of-Mouth Boost
- Print small flyers / visiting cards with the website QR code, leave them at hardware stores, real estate agents, and housing society offices in Vasai-Virar-Borivali corridor
- Ask satisfied customers to share your number in their society WhatsApp groups

**Realistic timeline:** With Google Business Profile + 15-20 reviews + sitemap submitted, most local service businesses start appearing in the top 3-5 local results within **4-8 weeks**. Paid Google Ads (₹300-500/day budget) can get you to position #1 immediately if you want faster results while organic SEO builds up — let me know if you want help setting that up too.

---

## 🔐 Security Notes
- Customer data (bookings/enquiries) is stored in a real PostgreSQL database, not in the browser
- Admin panel requires login — only you can see customer data
- CSRF protection is enabled on all forms
- Change the default admin password immediately
- Never share your `DJANGO_SECRET_KEY` or admin password

## 🤖 About the Chatbot "Shivam"
Shivam uses the Claude AI API (already wired in, no extra cost to you within this environment) and is pre-trained with all your services, areas, and pricing info. It answers customer questions 24/7 and encourages them to call or book.

## 📞 Need Help?
If you get stuck on any deployment step, just describe what you see and I'll help you fix it.
