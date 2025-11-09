

/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production'
const nextConfig = {
  reactStrictMode: true,
  productionBrowserSourceMaps: false,
  // Support reverse proxy deployment
  basePath: isProd ? '/sdmp/deep_analysis' : '',
  assetPrefix: isProd ? '/sdmp/deep_analysis' : '',
  trailingSlash: true,
  // Disable critters optimizeCss to avoid missing module during build
  experimental: {
    optimizeCss: false,
    scrollRestoration: true,
  }
};

module.exports = nextConfig;
