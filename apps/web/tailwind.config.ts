import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        app: "#f6f7f3",
        ink: "#171a16",
        muted: "#6d746f",
        panel: "#fffdf8",
        soft: "#f0f3ee",
        line: "#d9ded6",
        strong: "#b7c0b6",
        brand: "#16845f",
        brandBlue: "#316a9e",
        signal: "#c9851a",
        risk: "#d4483b",
        graphite: "#343941",
        gainSoft: "#e6f3ec",
        riskSoft: "#fae8e4",
        signalSoft: "#f8efd9",
        compareSoft: "#e3eef7",
      },
      boxShadow: {
        panel: "0 20px 60px rgba(38, 49, 42, 0.12)",
        lift: "0 12px 30px rgba(38, 49, 42, 0.10)",
      },
    },
  },
  plugins: [],
} satisfies Config;
