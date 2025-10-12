import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import HeaderApp from './components/HeaderApp.tsx'
import { registerLicense } from '@syncfusion/ej2-base';

// Registering Syncfusion license key
registerLicense('Ngo9BigBOggjGyl/Vkd+XU9FcVRDX3xKf0x/TGpQb19xflBPallYVBYiSV9jS3tSdkRiWHdecXRUQ2BVWU91Xg==');

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <HeaderApp />
      <App />
  </StrictMode>,
)
