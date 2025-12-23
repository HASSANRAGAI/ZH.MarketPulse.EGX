'use client';

import { useState, useRef } from 'react';
import { MenuComponent, MenuItemModel } from '@syncfusion/ej2-react-navigations';
import { DropDownListComponent, ChangeEventArgs as ddlChange } from '@syncfusion/ej2-react-dropdowns';
import '../styles/appmenu.scss';
import { Browser, select } from '@syncfusion/ej2-base';

interface AppMenuState {
  showItemOnClick: boolean;
  hamburgerMode: boolean;
}

// Inline simple data to avoid extra files; can be moved to JSON later
const hamburgerData: MenuItemModel[] = [
  { text: 'EGX', items: [{ text: 'Stocks' }, { text: 'Fair Values' }, { text: 'IPOs' }] },
  { text: 'News' },
  { text: 'Analytics', items: [{ text: 'Sectors' }, { text: 'Heatmap' }] },
  { text: 'About' }
];

const AppMenu = () => {
  const [state, setState] = useState<AppMenuState>({ showItemOnClick: true, hamburgerMode: false });

  const menuCreated = (): void => {
    if (Browser.isDevice) {
      select('.property-section')?.remove();
      select('#layoutcontainer')?.removeAttribute('class');
      select('#layoutcontainer')?.removeAttribute('id');
      (select('#menu') as HTMLElement).style.height = '363px';
    }
  };

  return (

                  <MenuComponent id="menu" items={hamburgerData} showItemOnClick={state.showItemOnClick} hamburgerMode={state.hamburgerMode} created={menuCreated} />
  );
};

export default AppMenu;
