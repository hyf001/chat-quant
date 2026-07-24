import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        app: "#f5f7fb",
        ink: "#17201b",
        muted: "#667085",
        panel: "#ffffff",
        soft: "#f8fafc",
        line: "#d9ded4",
        strong: "#c5d0df",
        brand: "#1f7a6d",
        brandBlue: "#2451a6",
        signal: "#e3b341",
        risk: "#b9574f",
      },
      boxShadow: {
        panel: "0 18px 48px rgba(23, 32, 27, 0.08)",
      },
    },
  },
  plugins: [],
} satisfies Config;
