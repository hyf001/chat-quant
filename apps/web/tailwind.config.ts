import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        app: "#f4f4f5",
        ink: "#18181b",
        muted: "#52525b",
        panel: "#ffffff",
        soft: "#fafafa",
        line: "#e4e4e7",
        strong: "#d4d4d8",
        brand: "#1f7a6d",
        brandBlue: "#3f3f46",
        signal: "#d97706",
        risk: "#dc2626",
      },
      boxShadow: {
        panel: "0 18px 48px rgba(23, 32, 27, 0.08)",
      },
    },
  },
  plugins: [],
} satisfies Config;
