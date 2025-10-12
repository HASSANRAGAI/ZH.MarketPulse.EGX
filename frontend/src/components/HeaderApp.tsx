import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import MenuApp from './MenuApp.tsx'
import * as React from "react";

const HeaderApp = () => {
  return (
    <AppBarComponent colorMode="Primary">
      <span className="regular">My App Header</span>
      <div className="e-appbar-spacer" />
      <MenuApp />
      <div className="e-appbar-spacer" />
      <ButtonComponent cssClass='e-inherit login'>Login</ButtonComponent>
    </AppBarComponent>
  );
};

export default HeaderApp;