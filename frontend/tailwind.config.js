import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        gold: '#d4af37',
        dark: '#1f2937',
      }
    }
  },
  plugins: [],
} satisfies Config
