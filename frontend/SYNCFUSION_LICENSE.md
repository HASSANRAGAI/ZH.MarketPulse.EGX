# Syncfusion License Setup

This project uses Syncfusion UI components which require a license key.

## Why You're Seeing the License Warning

The message "This application was built using a trial version of Syncfusion® Essential Studio®" appears because:
1. No valid license key has been registered, OR
2. The license key in `.env.local` is still the placeholder value

## Getting a License Key

### Option 1: Free Community License (Recommended)
**Eligibility**: Individual developers and small businesses (< $1M USD annual revenue, < 5 developers)

1. Visit: https://www.syncfusion.com/products/communitylicense
2. Click "CLAIM FREE LICENSE"
3. Sign in or create a Syncfusion account
4. Complete the eligibility form
5. Once approved, go to your dashboard: https://www.syncfusion.com/account/manage-trials/downloads
6. Copy your license key (it's a very long string starting with something like `Mgo+DSMBMAY9C3t2VFhh...`)

### Option 2: Trial License
1. Visit: https://www.syncfusion.com/downloads
2. Sign up for a 30-day trial
3. After registration, visit: https://www.syncfusion.com/account/manage-trials/downloads
4. Copy your trial license key

### Option 3: Commercial License
Purchase from: https://www.syncfusion.com/sales/products

## Setting Up Your License

### Step 1: Get Your License Key
Follow one of the options above to obtain your license key. It should look like:
```
Mgo+DSMBMAY9C3t2VFhhQlJBfV5AQmBIYVp/TGpJfl96cVxMZVVBJAtUQF1hSn9Vd0xiWntfcHdQQmJY
```
(This is just an example - use your actual key)

### Step 2: Add to Environment File
1. Open `frontend/.env.local` in a text editor
2. Replace the placeholder with your actual key:

```env
NEXT_PUBLIC_SYNCFUSION_LICENSE_KEY=Mgo+DSMBMAY9C3t2VFhhQlJBfV5AQmBIYVp/TGpJfl96cVxMZVVBJAtUQF1hSn9Vd0xiWntfcHdQQmJY
```

**Important**: 
- Do NOT use quotes around the key
- Do NOT add spaces
- The key should be one continuous line

### Step 3: Restart Your Dev Server
```powershell
# Stop the current server (Ctrl+C)
# Then restart:
cd D:\Workspaces\AIProjects\ZH.MarketPulse.EGX\frontend
npm run dev
```

## Verifying Registration

1. Open your browser's Developer Console (F12)
2. Look for the message: `Syncfusion license key registered successfully.`
3. The license warning banner should disappear

If you still see the warning:
- Check that you copied the ENTIRE license key (they can be very long)
- Verify there are no extra spaces or line breaks in the `.env.local` file
- Make sure the file is named exactly `.env.local` (not `.env.local.txt`)
- Restart the dev server completely

## Troubleshooting

### "License key is not set in environment variables"
- Ensure `.env.local` exists in the `frontend` folder
- Check that the variable name is exactly `NEXT_PUBLIC_SYNCFUSION_LICENSE_KEY`
- Restart the dev server after adding the key

### License warning still appears
- Clear browser cache and hard reload (Ctrl+Shift+R)
- Check browser console for any error messages
- Verify your license key hasn't expired (trial keys expire after 30 days)

### Getting a new license
If your trial expired:
- Apply for the free Community License if eligible
- Or purchase a commercial license

## Security Notes

- The `.env.local` file is already in `.gitignore` to prevent committing your license key
- Never commit license keys to version control
- Keep your license key secure and don't share it publicly

## More Information

- Syncfusion Licensing Guide: https://help.syncfusion.com/common/essential-studio/licensing/overview
- Community License FAQ: https://www.syncfusion.com/products/communitylicense/faq

