import React, { createContext, useContext, useState, ReactNode } from 'react';

interface AppState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  notifications: any[];
}

interface AppContextType {
  state: AppState;
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  addNotification: (notification: any) => void;
  removeNotification: (id: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AppState>({
    sidebarOpen: true,
    theme: 'light',
    notifications: []
  });

  const toggleSidebar = () => {
    setState(prev => ({ ...prev, sidebarOpen: !prev.sidebarOpen }));
  };

  const setTheme = (theme: 'light' | 'dark') => {
    setState(prev => ({ ...prev, theme }));
  };

  const addNotification = (notification: any) => {
    setState(prev => ({
      ...prev,
      notifications: [...prev.notifications, notification]
    }));
  };

  const removeNotification = (id: string) => {
    setState(prev => ({
      ...prev,
      notifications: prev.notifications.filter(n => n.id !== id)
    }));
  };

  return (
    <AppContext.Provider value={{ state, toggleSidebar, setTheme, addNotification, removeNotification }}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) throw new Error('useApp must be used within AppProvider');
  return context;
};
