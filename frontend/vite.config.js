import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'


export default defineConfig({

  plugins: [
    react()
  ],

  define:{
        global:"globalThis",
        "process.env":{
            NODE_ENV:"development"
        }
  },


  server: {

    proxy: {

      "/api":
      {

        target:
          "http://127.0.0.1:5000",

        changeOrigin:true,

        secure:false

      },
            
      "/athena": 
       {

          target:
                  "http://127.0.0.1:5000",
          changeOrigin:
                  true,
              secure:
                  false
          },

      "/ask": 
       {
          target:
                  "http://127.0.0.1:5000",
          changeOrigin:
                  true,
            secure:
                  false
        }
    }

  }

})