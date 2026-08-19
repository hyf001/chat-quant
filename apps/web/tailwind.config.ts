import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";

export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        app: "#f6f7f3",
        ink: "#171a16",
        mutedText: "#6d746f",
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
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      boxShadow: {
        panel: "0 20px 60px rgba(38, 49, 42, 0.12)",
        lift: "0 12px 30px rgba(38, 49, 42, 0.10)",
      },
    },
  },
  plugins: [animate],
} satisfies Config;
