/*
 * app.js
 *
 * Node.js + Express server for the AVRT™ licensing application.
 *
 * This server serves static files from the `public` directory and provides a
 * single checkout route for redirecting to Stripe-hosted payment pages
 * defined in environment variables. To add or modify pricing tiers, edit
 * the `tierEnvMapping` object below and update the corresponding keys in
 * your `.env` file.
 */

const express = require('express');
const path = require('path');
require('dotenv').config();

const app = express();

// Serve static assets from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Map tier slugs to environment variable keys. When adding a new tier,
// ensure both the key here and a corresponding value in your `.env` file.
const tierEnvMapping = {
  creator: 'STRIPE_LINK_CREATOR',
  starter: 'STRIPE_LINK_STARTER',
  builder: 'STRIPE_LINK_BUILDER',
  growth: 'STRIPE_LINK_GROWTH',
  professional: 'STRIPE_LINK_PROFESSIONAL',
  business: 'STRIPE_LINK_BUSINESS',
  enterprise: 'STRIPE_LINK_ENTERPRISE',
  premium: 'STRIPE_LINK_PREMIUM',
  strategic_shield: 'STRIPE_LINK_STRATEGIC_SHIELD',
  strategic_shield_plus: 'STRIPE_LINK_STRATEGIC_SHIELD_PLUS',
  strategic_shield_pro: 'STRIPE_LINK_STRATEGIC_SHIELD_PRO',
  strategic_shield_enterprise: 'STRIPE_LINK_STRATEGIC_SHIELD_ENTERPRISE'
};

/**
 * Checkout route: redirects the user to the Stripe-hosted payment page
 * corresponding to the requested tier. Tier names are case-insensitive
 * and use underscores in place of spaces or hyphens.
 */
app.get('/checkout/:tier', (req, res) => {
  const tierSlug = req.params.tier.toLowerCase();
  const envKey = tierEnvMapping[tierSlug];

  // Unknown tier
  if (!envKey) {
    return res.status(404).send(`<h1>404 Not Found</h1><p>Unknown tier: ${tierSlug}</p>`);
  }

  const stripeUrl = process.env[envKey];

  // Tier exists but environment variable is missing
  if (!stripeUrl) {
    return res
      .status(500)
      .send(
        `<h1>500 Server Error</h1><p>The Stripe link for ${tierSlug} is not configured. Please set ${envKey} in your environment.</p>`
      );
  }

  // Redirect to the configured Stripe hosted payment link
  return res.redirect(stripeUrl);
});

// Catch-all route for handling 404s (e.g., unknown routes)
app.use((req, res) => {
  res.status(404).send('<h1>404 Not Found</h1>');
});

// Start the server on the port specified in the environment or default to 3000
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`AVRT licensing app listening on port ${PORT}`);
});