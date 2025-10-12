import { MenuComponent, type MenuItemModel } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

const MenuApp = () => {
  const menuItems: MenuItemModel[] = [
    { text: 'File', items: [{ text: 'Open' }, { text: 'Save' }] },
    { text: 'Edit', items: [{ text: 'Cut' }, { text: 'Copy' }] },
    { text: 'Help' }
  ];

  return <MenuComponent items={menuItems} />;
};

export default MenuApp;