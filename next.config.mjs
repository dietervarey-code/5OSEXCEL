/** @type {import('next').NextConfig} */
const nextConfig = {
  // Univer is een zware client-side bundel (canvas-renderer).
  transpilePackages: ['@univerjs/presets'],
};

export default nextConfig;
