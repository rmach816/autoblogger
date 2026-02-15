import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';

// Security headers middleware
export const securityHeaders = helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
});

// CORS configuration
const corsOrigins = (() => {
  const raw = process.env['CORS_ORIGIN'];
  if (raw) {
    return raw
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
  }
  // Vite defaults to 5173; keep 3000 for older React dev servers.
  return ['http://localhost:5173', 'http://localhost:3000'];
})();

export const corsConfig = cors({
  origin: (origin, callback) => {
    // Allow non-browser clients (no Origin header).
    if (!origin) return callback(null, true);
    if (corsOrigins.includes(origin)) return callback(null, true);
    return callback(new Error(`CORS blocked for origin: ${origin}`));
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
});

// Rate limiting
export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many requests from this IP, please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

// API rate limiting (more restrictive for AI endpoints)
export const apiRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 20, // limit each IP to 20 API requests per windowMs
  message: {
    error: 'Too many API requests from this IP, please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});
