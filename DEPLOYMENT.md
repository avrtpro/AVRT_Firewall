# 🚀 AVRT™ Firewall — Deployment Guide

**Version:** 1.0.0
**Last Updated:** 2025-11-08
**Maintainer:** Jason Proper, BGBH Threads LLC
**License:** CC BY-NC 4.0

---

## 📋 Pre-Deployment Checklist

- [ ] Node.js v16+ installed
- [ ] Stripe account configured with 12 pricing tier links
- [ ] Environment variables prepared
- [ ] Git repository access confirmed
- [ ] Domain/hosting platform selected

---

## 🔧 Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/avrtpro/AVRT_Firewall.git
cd AVRT_Firewall
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Stripe payment links:

```env
PORT=3000
STRIPE_LINK_CREATOR=https://buy.stripe.com/8wMaGE3kV0f61jW6oo
STRIPE_LINK_STARTER=https://buy.stripe.com/your_starter_link
# ... configure all 12 tiers
```

### 4. Start Development Server

```bash
npm run dev
```

Visit `http://localhost:3000` to view the licensing interface.

---

## ☁️ Platform Deployment

### **GitHub Pages** (Static Only)

For static hosting, you'll need to build the frontend separately. The current app requires a Node.js server for Stripe redirects.

### **Replit** ✅ RECOMMENDED

1. Import repository: `https://github.com/avrtpro/AVRT_Firewall`
2. Add **Secrets** (Environment Variables):
   - Add all `STRIPE_LINK_*` variables
   - Set `PORT=3000`
3. Run command: `npm start`
4. Deploy with **Replit Autoscale** for production

### **Vercel** ✅ RECOMMENDED

1. Import GitHub repository
2. Set **Framework Preset**: Other
3. Set **Build Command**: `echo "No build required"`
4. Set **Output Directory**: `public`
5. Add **Environment Variables** for all Stripe links
6. Deploy

**Note:** Vercel requires Serverless Functions for Express routes. Use Vercel's Node.js runtime.

### **Heroku**

```bash
heroku create avrt-licensing-app
heroku config:set STRIPE_LINK_CREATOR=https://buy.stripe.com/...
# ... set all environment variables
git push heroku main
```

### **Railway**

1. Connect GitHub repository
2. Add environment variables in Dashboard
3. Railway auto-detects Node.js and deploys

### **Render**

1. Create new Web Service
2. Connect GitHub repository
3. Set **Build Command**: `npm install`
4. Set **Start Command**: `npm start`
5. Add environment variables
6. Deploy

---

## 🔐 Security Best Practices

### Environment Variables

- **NEVER** commit `.env` to version control
- Use platform-specific secret managers
- Rotate Stripe links if exposed

### HTTPS

- Always use HTTPS in production
- Most platforms (Vercel, Replit, Render) provide free SSL

### Rate Limiting

Consider adding rate limiting for production:

```bash
npm install express-rate-limit
```

### CORS Configuration

If integrating with external frontends, configure CORS properly.

---

## 📊 Monitoring & Analytics

### Recommended Tools

- **Stripe Dashboard**: Track subscriptions and revenue
- **Google Analytics**: Monitor page views
- **Sentry**: Error tracking
- **Uptime Robot**: Monitor availability

---

## 🧪 Testing Deployment

### Health Check

```bash
curl https://your-deployment-url.com/
# Should return the AVRT licensing page
```

### Tier Redirect Test

```bash
curl -I https://your-deployment-url.com/checkout/creator
# Should return 302 redirect to Stripe
```

---

## 🆘 Troubleshooting

### Port Already in Use

```bash
# Find and kill process using port 3000
lsof -ti:3000 | xargs kill
```

### Missing Environment Variables

Check logs for errors like:
```
The Stripe link for creator is not configured
```

Solution: Verify all `STRIPE_LINK_*` variables are set.

### 404 on Checkout Routes

Ensure `app.js` is running and Express routes are registered correctly.

---

## 📞 Support

**Official Contact:** info@avrt.pro
**Website:** https://avrt.pro
**Documentation:** https://gamma.app/docs/AVRT-One-The-Voice-Firewall-for-Safer-AI-kcauc69tnwmgvy5
**Licensing Tiers:** https://buy.stripe.com/8wMaGE3kV0f61jW6oo

---

## 📄 License

© 2025 Jason Proper, BGBH Threads LLC. All Rights Reserved.
Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

**Legal Representation:** Falcon Rappaport & Berkman LLP

---

**✅ DEPLOYMENT READY**
**🔒 THT™ PROTOCOL ACTIVE**
**🛡️ SPIEL™ SAFETY VALIDATED**
