'use client';
import { useEffect } from 'react';
import { registerLicense } from '@syncfusion/ej2-base';

export default function SyncfusionLicense() {
  useEffect(() => {
    const licenseKey = process.env.NEXT_PUBLIC_SYNCFUSION_LICENSE_KEY;

    if (!licenseKey) {
      console.error('❌ Syncfusion license key is missing!');
      console.error('Add NEXT_PUBLIC_SYNCFUSION_LICENSE_KEY to your .env.local file');
      return;
    }

    // Check if it's still the placeholder
    if (licenseKey.includes('your_syncfusion_license_key_here')) {
      console.error('❌ Syncfusion license key is still the placeholder value!');
      console.error('Replace it with your actual license key from https://www.syncfusion.com/account/manage-trials/downloads');
      return;
    }

    try {
      registerLicense(licenseKey);
      console.log('✅ Syncfusion license key registered successfully!');
      console.log('License key preview:', licenseKey.substring(0, 20) + '...');
    } catch (error) {
      console.error('❌ Failed to register Syncfusion license:', error);
    }
  }, []);

  return null;
}

