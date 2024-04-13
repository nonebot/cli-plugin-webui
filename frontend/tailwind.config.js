import daisyui from 'daisyui'

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {}
  },
  plugins: [daisyui],
  daisyui: {
    themes: [
      {
        light: {
          ...require('daisyui/src/theming/themes')['light'],
          primary: '#EA5353'
        },
        dark: {
          ...require('daisyui/src/theming/themes')['dark'],
          primary: '#EA5353'
        }
      }
    ]
  }
}
