import morgan from 'morgan';

// Request logging middleware
export const requestLogger = morgan('combined', {
  skip: (_req, res) => res.statusCode < 400
});

// Detailed logging for development
export const devLogger = morgan('dev');

// Custom logging format
export const customLogger = morgan(':method :url :status :res[content-length] - :response-time ms');
