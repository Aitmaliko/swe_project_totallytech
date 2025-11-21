// // /** @type {import('tailwindcss').Config} */
// // export default {
// //   content: [
// //     "./index.html",
// //     "./src/**/*.{js,ts,jsx,tsx}",
// //   ],
// //   theme: {
// //     extend: {},
// //   },
// //   plugins: [],
// // }



// /** @type {import('tailwindcss').Config} */
// import defaultTheme from 'tailwindcss/defaultTheme';

// export default {
//   content: [
//     "./index.html",
//     "./src/**/*.{js,ts,jsx,tsx}",
//   ],
//   theme: {
//     extend: {
//       colors: {
//         // Neutral, not-too-bright violet theme
//         brand: {
//           50:  '#f5f3ff',
//           100: '#ebe7ff',
//           200: '#d7ceff',
//           300: '#c4b5fd',
//           400: '#a78bfa',
//           500: '#8b5cf6', // main primary
//           600: '#7c3aed',
//           700: '#6d28d9',
//           800: '#5b21b6',
//           900: '#4c1d95',
//         },
//       },
//       fontFamily: {
//         // Body font
//         sans: ['Inter', ...defaultTheme.fontFamily.sans],
//         // Heading font
//         heading: ['Poppins', ...defaultTheme.fontFamily.sans],
//       },
//       borderRadius: {
//         // Slightly softer, more rounded than default
//         lg: "1rem",
//         xl: "1.5rem",
//         "2xl": "1.75rem",
//       },
//       boxShadow: {
//         // Soft, neutral card shadow
//         soft: "0 18px 45px rgba(15, 23, 42, 0.08)",
//       },
//     },
//   },
//   plugins: [],
// };


/** @type {import('tailwindcss').Config} */
import defaultTheme from 'tailwindcss/defaultTheme';

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // NEW
        beige: '#faf6ef',

        // Neutral, not-too-bright violet theme
        brand: {
          50:  '#f5f3ff',
          100: '#ebe7ff',
          200: '#d7ceff',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
        },
      },
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
        heading: ['Poppins', ...defaultTheme.fontFamily.sans],
      },
      borderRadius: {
        lg: "1rem",
        xl: "1.5rem",
        "2xl": "1.75rem",
      },
      boxShadow: {
        soft: "0 18px 45px rgba(15, 23, 42, 0.08)",
      },
    },
  },
  plugins: [],
};
