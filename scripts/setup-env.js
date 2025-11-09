#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const net = require('net');

const rootDir = path.join(__dirname, '..');
const envFile = path.join(rootDir, '.env');
const webEnvFile = path.join(rootDir, 'apps', 'web', '.env.local');

// Default ports
const DEFAULT_API_PORT = 8080;
const DEFAULT_WEB_PORT = 3000;

// Robust check: consider a port unavailable if a TCP connection succeeds
// This avoids false positives when another process bound the port with SO_REUSEPORT
function isPortAvailable(port) {
  const tryConnect = (host) => new Promise((resolve) => {
    const socket = net.connect({ port, host });
    let settled = false;

    const finish = (available) => {
      if (settled) return;
      settled = true;
      try { socket.destroy(); } catch (_) {}
      resolve(available);
    };

    socket.once('connect', () => finish(false)); // Something is listening
    socket.once('error', (err) => {
      // ECONNREFUSED => nothing listening on that host
      // ETIMEDOUT/EHOSTUNREACH => treat as available for localhost checks
      finish(true);
    });
    socket.setTimeout(500, () => finish(true));
  });

  // Check both IPv4 and IPv6 localhost
  return Promise.all([
    tryConnect('127.0.0.1'),
    tryConnect('::1').catch(() => true), // ignore if IPv6 not available
  ]).then((results) => results.every(Boolean));
}

// Find available port starting from default
async function findAvailablePort(startPort) {
  let port = startPort;
  while (!(await isPortAvailable(port))) {
    port++;
  }
  return port;
}

async function setupEnvironment() {
  console.log('Setting up environment...');
  
  try {
    // Ensure data directory exists
    const dataDir = path.join(rootDir, 'data');
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
      console.log('  Created data directory');
    }
    
    // Find available ports
    const apiPort = await findAvailablePort(DEFAULT_API_PORT);
    const webPort = await findAvailablePort(DEFAULT_WEB_PORT);
    
    if (apiPort !== DEFAULT_API_PORT) {
      console.log(`  API port ${DEFAULT_API_PORT} is busy, using ${apiPort}`);
    } else {
      console.log(`  API port: ${apiPort}`);
    }
    
    if (webPort !== DEFAULT_WEB_PORT) {
      console.log(`  Web port ${DEFAULT_WEB_PORT} is busy, using ${webPort}`);
    } else {
      console.log(`  Web port: ${webPort}`);
    }
    
    // Create root .env file
    const envExampleFile = path.join(rootDir, '.env.example');
    let envContent = '';
    let isNewFile = !fs.existsSync(envFile);

    if (isNewFile && fs.existsSync(envExampleFile)) {
      // First time setup: extract specific values from .env.example
      console.log(`  Creating .env from .env.example template...`);

      const exampleContent = fs.readFileSync(envExampleFile, 'utf8');

      // Extract EXPORT configuration values from .env.example
      const extractValue = (key) => {
        const match = exampleContent.match(new RegExp(`^${key}=(.*)$`, 'm'));
        return match ? match[1] : '';
      };

      const exportEmail = extractValue('EXPORT_DEFAULT_EMAIL');
      const exportTenantId = extractValue('EXPORT_TENANT_ID');
      const exportCacheRoot = extractValue('EXPORT_CACHE_ROOT');
      const thsTier = extractValue('THS_TIER') || 'dev';
      const biDomain = extractValue('BI_DOMAIN') || 'https://phonestat.hexin.cn/sdmp/easyfetch';
      const biContainerHost = extractValue('BI_CONTAINER_HOST') || 'http://easyfetch:9596';
      const sslCertFile = extractValue('SSL_CERT_FILE');
      const sslCertPassword = extractValue('SSL_CERT_PASSWORD');

      // Create .env with auto-configured values + Export required values
      envContent = `# Auto-generated environment configuration
API_PORT=${apiPort}
WEB_PORT=${webPort}
DATABASE_URL=sqlite:///${path.join(rootDir, 'data', 'cc.db')}

# =============================================================================
# ENVIRONMENT CONFIGURATION
# =============================================================================

# 运行环境 (dev: 开发环境, prod: 生产环境)
THS_TIER=${thsTier}

# =============================================================================
# DATA EXPORT CONFIGURATION
# =============================================================================

# 导出服务认证配置
# 注意：开发环境使用SSL证书认证，不需要配置以下参数
#      生产环境使用Header认证，需要配置以下参数
EXPORT_DEFAULT_EMAIL=${exportEmail}
EXPORT_TENANT_ID=${exportTenantId}

# 导出缓存根目录（留空则使用默认值）
EXPORT_CACHE_ROOT=${exportCacheRoot}

# =============================================================================
# BI SERVICE CONFIGURATION
# =============================================================================

# BI服务地址（开发环境使用）
BI_DOMAIN=${biDomain}

# BI容器服务地址（生产环境使用）
BI_CONTAINER_HOST=${biContainerHost}

# =============================================================================
# SSL CERTIFICATE CONFIGURATION (开发环境需要)
# =============================================================================

# SSL证书路径（开发环境必需）
SSL_CERT_FILE=${sslCertFile}
SSL_CERT_PASSWORD=${sslCertPassword}
`;

      fs.writeFileSync(envFile, envContent);
      console.log(`  Created .env with export configuration (please configure SSL certificate for dev environment)`);
    } else if (isNewFile) {
      // Fallback: create minimal .env if .env.example doesn't exist
      envContent = `# Auto-generated environment configuration
API_PORT=${apiPort}
WEB_PORT=${webPort}
DATABASE_URL=sqlite:///${path.join(rootDir, 'data', 'cc.db')}
`;
      fs.writeFileSync(envFile, envContent);
      console.log(`  Created .env (minimal configuration)`);
    } else {
      // Update existing .env file, only modify auto-configured values
      console.log(`  Updating .env with new ports...`);
      envContent = fs.readFileSync(envFile, 'utf8');

      const updateOrAddLine = (key, value) => {
        const safeKey = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const lineRe = new RegExp(`^${safeKey}=.*$`, 'm');
        if (lineRe.test(envContent)) {
          envContent = envContent.replace(lineRe, `${key}=${value}`);
        } else {
          if (!envContent.endsWith('\n')) envContent += '\n';
          envContent += `${key}=${value}\n`;
        }
      };

      updateOrAddLine('API_PORT', apiPort);
      updateOrAddLine('WEB_PORT', webPort);
      updateOrAddLine('DATABASE_URL', `sqlite:///${path.join(rootDir, 'data', 'cc.db')}`);

      fs.writeFileSync(envFile, envContent);
      console.log(`  Updated .env`);
    }
    
    // Create or update apps/web/.env.local to match chosen API port
    const desiredApiBase = `http://localhost:${apiPort}`;
    const desiredWsBase = `ws://localhost:${apiPort}`;

    const writeEnvLocal = (content) => {
      fs.writeFileSync(webEnvFile, content);
    };

    if (!fs.existsSync(webEnvFile)) {
      const webEnvContent = `# Auto-generated environment configuration\nNEXT_PUBLIC_API_BASE=${desiredApiBase}\nNEXT_PUBLIC_WS_BASE=${desiredWsBase}\n`;
      writeEnvLocal(webEnvContent);
      console.log(`  Created apps/web/.env.local`);
    } else {
      let contents = fs.readFileSync(webEnvFile, 'utf8');
      const origContents = contents;

      const setOrAdd = (key, value) => {
        const safeKey = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const lineRe = new RegExp(`^${safeKey}=.*$`, 'm');
        if (lineRe.test(contents)) {
          contents = contents.replace(lineRe, `${key}=${value}`);
        } else {
          if (!contents.endsWith('\n')) contents += '\n';
          contents += `${key}=${value}\n`;
        }
      };

      setOrAdd('NEXT_PUBLIC_API_BASE', desiredApiBase);
      setOrAdd('NEXT_PUBLIC_WS_BASE', desiredWsBase);

      // Deduplicate these keys, keeping the last occurrence
      const keysToDedup = ['NEXT_PUBLIC_API_BASE', 'NEXT_PUBLIC_WS_BASE'];
      const lines = contents.split(/\r?\n/);
      const seen = new Set();
      const result = [];
      for (let i = lines.length - 1; i >= 0; i--) {
        const line = lines[i];
        const kvMatch = line.match(/^([A-Z0-9_]+)=/);
        if (kvMatch && keysToDedup.includes(kvMatch[1])) {
          const key = kvMatch[1];
          if (seen.has(key)) continue; // skip older duplicates
          seen.add(key);
        }
        result.push(line);
      }
      contents = result.reverse().join('\n');

      if (contents !== origContents) {
        writeEnvLocal(contents);
        console.log('  Updated apps/web/.env.local to match API port');
      } else {
        console.log('  apps/web/.env.local already up to date');
      }
    }
    
    console.log('  Environment setup complete!');
    
    if (apiPort !== DEFAULT_API_PORT || webPort !== DEFAULT_WEB_PORT) {
      console.log('\n  Note: Using non-default ports');
      console.log(`     API: http://localhost:${apiPort}`);
      console.log(`     Web: http://localhost:${webPort}`);
    }
    
    // Return ports for use in other scripts
    return { apiPort, webPort };
  } catch (error) {
    console.error('\nFailed to setup environment');
    console.error('Error:', error.message);
    console.error('\nHow to fix:');
    console.error('   1. Check file permissions');
    console.error('   2. Ensure you have write access to the project directory');
    console.error('   3. Try running with elevated permissions if needed');
    process.exit(1);
  }
}

// If run directly
if (require.main === module) {
  setupEnvironment().catch(console.error);
}

module.exports = { setupEnvironment, findAvailablePort };
