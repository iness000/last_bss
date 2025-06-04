import { Link, useLocation } from 'react-router-dom';
import { Battery, GaugeCircle, Users, MapPin, RotateCcw, Settings, LogOut } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../../context/AuthContext';
import { cn } from '../../utils/cn';

type SidebarProps = {
  isOpen: boolean;
  isMobile: boolean;
  closeSidebar: () => void;
};

const Sidebar = ({ isOpen, isMobile, closeSidebar }: SidebarProps) => {
  const location = useLocation();
  const { logout } = useAuth();

  const sidebarVariants = {
    open: { x: 0, transition: { type: "spring", stiffness: 300, damping: 30 } },
    closed: { x: "-100%", transition: { type: "spring", stiffness: 300, damping: 30 } }
  };

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: <GaugeCircle size={20} /> },
    { name: 'User Management', path: '/users', icon: <Users size={20} /> },
    { name: 'Station Management', path: '/stations', icon: <MapPin size={20} /> },
    { name: 'Battery Management', path: '/batteries', icon: <Battery size={20} /> },
    { name: 'Swap Activity', path: '/swaps', icon: <RotateCcw size={20} /> },
  ];

  const handleLogout = () => {
    logout();
  };

  const overlay = isMobile && isOpen && (
    <div 
      className="fixed inset-0 bg-black/50 z-20" 
      onClick={closeSidebar}
    />
  );

  return (
    <>
      {overlay}
      <AnimatePresence>
        {(isOpen || !isMobile) && (
          <motion.div
            initial={isMobile ? "closed" : false}
            animate="open"
            exit="closed"
            variants={sidebarVariants}
            className={cn(
              "w-64 bg-white border-r border-gray-200 flex flex-col",
              isMobile ? "fixed inset-y-0 left-0 z-30" : "relative"
            )}
          >
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center space-x-3">
                <Battery size={28} className="text-primary-700" />
                <h1 className="text-xl font-bold text-gray-900">BatterySwap</h1>
              </div>
            </div>

            <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={cn(
                    "flex items-center space-x-3 px-4 py-3 rounded-lg transition-all",
                    "hover:bg-gray-100",
                    location.pathname === item.path
                      ? "bg-primary-50 text-primary-700 font-medium"
                      : "text-gray-700"
                  )}
                  onClick={isMobile ? closeSidebar : undefined}
                >
                  <span className={location.pathname === item.path ? "text-primary-700" : "text-gray-500"}>
                    {item.icon}
                  </span>
                  <span>{item.name}</span>
                </Link>
              ))}
            </nav>

            <div className="p-4 border-t border-gray-200">
              <Link
                to="/settings"
                className="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors hover:bg-gray-100 text-gray-700"
              >
                <Settings size={20} className="text-gray-500" />
                <span>Settings</span>
              </Link>
              <button
                onClick={handleLogout}
                className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors hover:bg-gray-100 text-gray-700"
              >
                <LogOut size={20} className="text-gray-500" />
                <span>Logout</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default Sidebar;